import sys, os
from examples.stream_as_a_dead_letter_queue_10.common import QUEUE_NAME_QUORUM, channel

def main():
    def callback(ch, method, properties, body):
        print(f"Received {body.decode()}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue=QUEUE_NAME_QUORUM, on_message_callback=callback, auto_ack=False)

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