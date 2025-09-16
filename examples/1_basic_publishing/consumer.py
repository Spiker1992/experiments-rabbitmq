# Reference: https://www.rabbitmq.com/tutorials/tutorial-one-python
# Consumer consumes any messages from the queue and prints them to the console.
import pika, sys, os
from config import RABBITMQ_HOST

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f"Received {body.decode()}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

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