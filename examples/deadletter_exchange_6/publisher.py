# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
import pika
import time
from examples.rabbitmq_utils import publish_bulk_messages
from examples.deadletter_exchange_6.constants import QUEUE_NAME

MESSAGE_COUNT = 10

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue with dead letter exchange settings
channel.exchange_declare(exchange='dlx')
channel.queue_declare(queue='dlq')
channel.queue_bind(exchange='dlx', queue='dlq', routing_key='dlq')

channel.queue_declare(queue=QUEUE_NAME, arguments={
    "x-dead-letter-exchange": "dlx",
    "x-dead-letter-routing-key": "dlq"
})

# Send a message
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body='Hello RabbitMQ!')
print("[x] Sent 'Hello RabbitMQ!'")

publish_bulk_messages(channel, QUEUE_NAME, MESSAGE_COUNT, verbose=True)

# Close the connection
connection.close()
