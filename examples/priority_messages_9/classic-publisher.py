# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
import pika
from examples.rabbitmq_utils import publish_bulk_messages
from examples.priority_messages_9.constants import QUEUE_NAME_CLASSIC, channel, connection

HIGH_PRIORITY = 2
LOW_PRIORITY = 1


# Send a message
for i in range(5):
    properties = pika.BasicProperties(priority=LOW_PRIORITY)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME_CLASSIC, body='low priority message!', properties=properties)
    print("[x] Sent a low priority message")

for i in range(3):
    properties = pika.BasicProperties(priority=HIGH_PRIORITY)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME_CLASSIC, body='high priority message!', properties=properties)
    print("[x] Sent a high priority message")

# expected output 
# [x] Sent a high prority message 
# [x] Sent a high prority message 
# [x] Sent a high prority message 
# [x] Sent a low prority message
# [x] Sent a low prority message
# [x] Sent a low prority message
# [x] Sent a low prority message
# [x] Sent a low prority message

# actual output
# Received high priority message!
# Received high priority message!
# Received high priority message!
# Received low priority message!
# Received low priority message!
# Received low priority message!
# Received low priority message!
# Received low priority message!

# Close the connection
connection.close()
