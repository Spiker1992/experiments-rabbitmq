import pika
from config import RABBITMQ_HOST

QUEUE_NAME_CLASSIC = "priority_messages_9_classic"
QUEUE_NAME_QUORUM = "priority_messages_9_quorum"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME_CLASSIC, durable=True, arguments={"x-max-priority": 10})
channel.queue_declare(queue=QUEUE_NAME_QUORUM, durable=True, arguments={"x-queue-type": "quorum"})