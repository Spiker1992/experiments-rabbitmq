# Reference: https://www.rabbitmq.com/tutorials/tutorial-one-python
# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
import pika
from config import RABBITMQ_HOST

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='hello')

# Send a message
channel.basic_publish(exchange='', routing_key='hello', body='Hello RabbitMQ!')
print("[x] Sent 'Hello RabbitMQ!'")

# Close the connection
connection.close()
