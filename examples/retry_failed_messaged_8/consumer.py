import pika, sys, os
import time
import random
from examples.retry_failed_messaged_8.constants import QUEUE_NAME, channel

def main():
    def callback(ch, method, properties, body):
        print(properties.__dict__)
        print(method.__dict__)
        headers = properties.headers or {}
        retry = headers.get("x-delivery-count", 0) if headers else 0

        if retry < 3:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            new_headers = headers
            new_headers["x-delivery-count"] = new_headers.get("x-delivery-count", 0) + 1
            ch.basic_publish(
                exchange=method.exchange,
                routing_key=method.routing_key,
                body=body,
                properties=pika.BasicProperties(
                    headers=new_headers
                )
            ) 

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)