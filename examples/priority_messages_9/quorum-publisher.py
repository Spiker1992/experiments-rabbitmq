# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
import pika
from examples.rabbitmq_utils import publish_bulk_messages
from examples.priority_messages_9.constants import QUEUE_NAME_QUORUM, channel, connection

HIGH_PRIORITY = 10
LOW_PRIORITY = 1


# Send a message
for i in range(5):
    properties = pika.BasicProperties(priority=LOW_PRIORITY)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME_QUORUM, body='low priority message!', properties=properties)
    print("[x] Sent a low priority message")

for i in range(3):
    properties = pika.BasicProperties(priority=HIGH_PRIORITY)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME_QUORUM, body='high priority message!', properties=properties)
    print("[x] Sent a high priority message")

# expected output 
# [x] Sent a low prority message (first one)
# [x] Sent a high prority message (next two high priority are pushed to consumer)
# [x] Sent a high prority message (this follows the 2 high for 1 low messages)
# [x] Sent a low prority message (this is the next low priority message due to 2:1 ratio)
# [x] Sent a high prority message (last high priority message)
# [x] Sent a low prority message (the rest of the low priority messages)
# [x] Sent a low prority message
# [x] Sent a low prority message

# actual output
# Received low priority message!
# Received high priority message!
# Received high priority message!
# Received low priority message!
# Received high priority message!
# Received low priority message!
# Received low priority message!
# Received low priority message!

# Close the connection
connection.close()
