import pika
from config import RABBITMQ_HOST

QUEUE_NAME = "retry_failed_messaged_8"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True)