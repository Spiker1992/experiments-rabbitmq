# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
from examples.rabbitmq_utils import publish_bulk_messages
from examples.priority_messages_9.constants import QUEUE_NAME_QUORUM, channel, connection

HIGH_PRIORITY = 10
LOW_PRIORITY = 1


# Send a message
for i in range(5):
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME_QUORUM, body='Hello RabbitMQ!', priority=LOW_PRIORITY)
    print("[x] Sent a low prority message")

channel.basic_publish(exchange='', routing_key=QUEUE_NAME_QUORUM, body='Hello RabbitMQ!')
print("[x] Sent a high priority message", priority=HIGH_PRIORITY)

# expected out

# Close the connection
connection.close()
