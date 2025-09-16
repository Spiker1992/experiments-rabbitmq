# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
import pika
from config import RABBITMQ_HOST
import time
from examples.rabbitmq_utils import publish_bulk_messages

QUEUE_NAME = "round_robbin"
MESSAGE_COUNT = 10

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue=QUEUE_NAME)

# Send a message
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body='Hello RabbitMQ!')
print("[x] Sent 'Hello RabbitMQ!'")

publish_bulk_messages(channel, QUEUE_NAME, MESSAGE_COUNT, verbose=True)

# Close the connection
connection.close()
