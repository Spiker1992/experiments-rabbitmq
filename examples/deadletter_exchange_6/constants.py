import pika
from config import RABBITMQ_HOST

QUEUE_NAME = "deadletter_exchange_6"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Declare dead letter exchange and dead letter queue
channel.exchange_declare(exchange='dead_letter_exchange')
channel.queue_declare(queue='dead_letter_queue')
channel.queue_bind(exchange='dead_letter_exchange', queue='dead_letter_queue', routing_key=QUEUE_NAME)

# we declare the main queue with dead letter exchange parameters
# routing key is optional, if not provided the original routing key will be used
# in our case the original routing key is QUEUE_NAME
channel.queue_declare(queue=QUEUE_NAME, arguments={
    "x-dead-letter-exchange": "dead_letter_exchange",
    # "x-dead-letter-routing-key": "my_routing_key"
})