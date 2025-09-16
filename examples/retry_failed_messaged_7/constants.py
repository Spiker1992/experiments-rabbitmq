import pika
from config import RABBITMQ_HOST

QUEUE_NAME = "retry_failed_messaged_7"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True, arguments={
    "x-delivery-limit": 3,  # max delivery attempts
    "x-queue-type": "quorum"
})