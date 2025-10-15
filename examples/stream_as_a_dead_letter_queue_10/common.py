import pika
from config import RABBITMQ_HOST

# It is recommended that all quorum queues have a dead letter configuration of some sort to
#  ensure messages aren't dropped and lost unintentionally. Using a single stream for a low
#  priority dead letter policy is a good, low resource way to ensure dropped messages are
#  retained for some time after.
# https://www.rabbitmq.com/docs/quorum-queues#poison-message-handling

QUEUE_NAME_QUORUM = "stream_as_a_dead_letter_queue_10_quorum"
STREAM_NAME = "stream_as_a_dead_letter_queue_10_stream" 


connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# https://www.rabbitmq.com/docs/streams#declaring
channel.queue_declare(queue=STREAM_NAME, durable=True, exclusive=False, auto_delete=False, arguments={"x-queue-type": "stream"})
channel.exchange_declare(exchange='dead_letter_exchange', exchange_type='fanout')
channel.queue_bind(queue=STREAM_NAME, exchange='dead_letter_exchange')

# Create a queue
channel.queue_declare(
    queue=QUEUE_NAME_QUORUM, 
    durable=True, 
    arguments={
        "x-queue-type": "quorum",
        "x-dead-letter-exchange": "dead_letter_exchange"
    }
)