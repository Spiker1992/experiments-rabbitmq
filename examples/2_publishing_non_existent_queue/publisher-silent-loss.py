# Reference: https://www.rabbitmq.com/docs/publishers#amqp-0-9-1
# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
# 
# After connection is opened we can delete the queue
# with `docker exec rabbitmq rabbitmqctl delete_queue hello`
#
# After deleting the queue, messages are silently dropped
import pika
from config import RABBITMQ_HOST

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='hello')


# Infinite loop to prompt user for messages and publish to queue
try:
    while True:
        message = input("Enter a message to publish (Ctrl+C to exit): ")
        if message == "delete_queue":
            channel.queue_delete(queue='hello')
            print("Queue 'hello' deleted. You can now publish messages to a non-existent queue.")
        else:
            channel.basic_publish(exchange='', routing_key='hello', body=message)
            print(f"[x] Sent '{message}'")
except KeyboardInterrupt:
    print("\nExiting publisher...")
finally:
    connection.close()
