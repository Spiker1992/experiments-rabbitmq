# Reference: https://www.rabbitmq.com/tutorials/tutorial-one-python
# Consumer consumes any messages from the queue and prints them to the console.
import pika, sys, os
from config import RABBITMQ_HOST
import time
import random
from examples.five_message_prefetching.constants import QUEUE_NAME

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)  
    channel.queue_declare(queue=QUEUE_NAME)

    def callback(ch, method, properties, body):
        print(f"Received {body.decode()}")
        delay = random.uniform(2, 8)  # Random delay between 2 and 8 seconds
        print(f"Processing message for {delay:.2f} seconds...")
        time.sleep(delay)

        ch.basic_ack(delivery_tag=method.delivery_tag) # have to ack manually because of prefetch_count=1. Without this RabbitQKM will keep sending the same message over and over again.

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