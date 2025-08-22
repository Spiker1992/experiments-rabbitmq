# Reference: https://www.rabbitmq.com/tutorials/tutorial-one-python
# Publisher sends a message to a RabbitMQ queue
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
import pika
import time

QUEUE_NAME = "round_robbin"
MESSAGE_COUNT = 10

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue=QUEUE_NAME)

# Send a message
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body='Hello RabbitMQ!')
print("[x] Sent 'Hello RabbitMQ!'")

start_time = time.time()
last_report_time = start_time
messages_sent = 0
print("Starting message publishing...")
for i in range(MESSAGE_COUNT):
	channel.basic_publish(
		exchange='',
		routing_key=QUEUE_NAME,
		body=f"Message {i+1}",
		properties=pika.BasicProperties(delivery_mode=2),
        mandatory=True # mandatory=True ensures that the message is returned if the queue does not exist
	)
	messages_sent += 1
	current_time = time.time()
	if current_time - last_report_time >= 1:
		elapsed = current_time - last_report_time
		mps = messages_sent / (current_time - start_time)
		print(f"{messages_sent} messages sent, {mps:.2f} msg/sec (avg)")
		last_report_time = current_time
# End timer
end_time = time.time()
elapsed = end_time - start_time

print(f"Sent {MESSAGE_COUNT} messages to '{QUEUE_NAME}' in {elapsed:.4f} seconds")

# Close the connection
connection.close()
