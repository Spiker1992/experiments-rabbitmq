import sys, os
from examples.priority_messages_9.constants import QUEUE_NAME_CLASSIC, channel

def main():
    def callback(ch, method, properties, body):
        print(f"Received {body.decode()}")

    channel.basic_consume(queue=QUEUE_NAME_CLASSIC, on_message_callback=callback, auto_ack=True)

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