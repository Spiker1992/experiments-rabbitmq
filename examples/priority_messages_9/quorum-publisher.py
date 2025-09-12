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

for i in range(3):
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME_QUORUM, body='Hello RabbitMQ!')
    print("[x] Sent a high priority message", priority=HIGH_PRIORITY)

# expected output 
# [x] Sent a low prority message (first one)
# [x] Sent a high prority message (next two high priority are pushed to consumer)
# [x] Sent a high prority message (this follows the 2 high for 1 low messages)
# [x] Sent a low prority message (this is the next low priority message due to 2:1 ratio)
# [x] Sent a high prority message (last high priority message)
# [x] Sent a low prority message (the rest of the low priority messages)
# [x] Sent a low prority message
# [x] Sent a low prority message


# Close the connection
connection.close()
