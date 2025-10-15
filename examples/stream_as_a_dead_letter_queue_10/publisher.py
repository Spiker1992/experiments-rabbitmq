# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
from examples.stream_as_a_dead_letter_queue_10.common import QUEUE_NAME_QUORUM, channel, connection

# Send a message
channel.basic_publish(exchange='', routing_key=QUEUE_NAME_QUORUM, body='Hello RabbitMQ!')
print("[x] Sent 'Hello RabbitMQ!'")

# Close the connection
connection.close()
