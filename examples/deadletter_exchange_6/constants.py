import pika

QUEUE_NAME = "deadletter_exchange_6"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)  

channel.exchange_declare(exchange='dlx')
channel.queue_declare(queue='dlq')
channel.queue_bind(exchange='dlx', queue='dlq', routing_key='dlq')

channel.queue_declare(queue=QUEUE_NAME, arguments={
    "x-dead-letter-exchange": "dlx",
    "x-dead-letter-routing-key": "dlq"
})