import pika, sys, os
import time
import random
from examples.deadletter_exchange_6.constants import QUEUE_NAME, channel

def main():
    def callback(ch, method, properties, body):
        print(f"Received {body.decode()}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # nack the message so it goes to the dead letter exchange

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