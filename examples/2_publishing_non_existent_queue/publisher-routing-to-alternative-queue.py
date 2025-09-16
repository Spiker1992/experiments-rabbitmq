# Reference: https://www.rabbitmq.com/docs/publishers#amqp-0-9-1
# Reference: https://www.rabbitmq.com/docs/confirms
# Reference: https://www.rabbitmq.com/docs/ae#define-using-arguments

# Publisher sends a message to a RabbitMQ queue
#
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
# 
# After deleting the queue, by sending `delete_queue` message, new messages that you send
# will be forwarded to an alternate exchange, which will then route them to a different queue.
#
# NOTE: This way of defining an alternate exchange is discouraged. Consider using a policy instead
import pika
from config import RABBITMQ_HOST


# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()


# Declare exchange and a queue
channel.exchange_declare(
    exchange='main_exchange',
    exchange_type='direct',
    arguments={'alternate-exchange': 'alt_exchange'}
)
channel.queue_declare(queue='hello')
channel.queue_bind(queue='hello', exchange='main_exchange', routing_key='hello')

# Alternate exchange will capture unroutable messages
channel.exchange_declare(
    exchange='alt_exchange',
    exchange_type='fanout'
)
channel.queue_declare(queue='unroutable')
channel.queue_bind(queue='unroutable', exchange='alt_exchange')

channel.confirm_delivery() # Enable publisher confirms

# Infinite loop to prompt user for messages and publish to queue
try:
    while True:
        message = input("Enter a message to publish (Ctrl+C to exit): ")
        if message == "delete_queue":
            channel.queue_delete(queue='hello')
            print("Queue 'hello' deleted. You can now publish messages to a non-existent queue.")
        else:
            channel.basic_publish(
                exchange='main_exchange',
                routing_key='hello',
                body=message,
            )
            print(f"[x] Published '{message}'")
except KeyboardInterrupt:
    print("\nExiting publisher...")
finally:
    connection.close()
