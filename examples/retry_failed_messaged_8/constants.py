import pika

QUEUE_NAME = "retry_failed_messaged_8"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True)