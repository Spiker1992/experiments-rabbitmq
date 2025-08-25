# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
from examples.rabbitmq_utils import publish_bulk_messages
from examples.deadletter_exchange_6.constants import QUEUE_NAME, channel

MESSAGE_COUNT = 10

# Send a message
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body='Hello RabbitMQ!')
print("[x] Sent 'Hello RabbitMQ!'")

publish_bulk_messages(channel, QUEUE_NAME, MESSAGE_COUNT, verbose=True)

# Close the connection
connection.close()
