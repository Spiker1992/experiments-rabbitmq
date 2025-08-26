# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
from examples.rabbitmq_utils import publish_bulk_messages
from examples.retry_failed_messaged_8.constants import QUEUE_NAME, channel, connection

# Send a message
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body='Hello RabbitMQ!')
print("[x] Sent 'Hello RabbitMQ!'")

# Close the connection
connection.close()
