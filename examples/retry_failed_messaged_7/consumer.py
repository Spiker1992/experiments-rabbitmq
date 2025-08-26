import pika, sys, os
import time
import random
from examples.retry_failed_messaged_7.constants import QUEUE_NAME, channel

def main():
    def callback(ch, method, properties, body):
        print(properties.__dict__)
        print(method.__dict__)

        ch.basic_nack(delivery_tag=method.delivery_tag) 

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