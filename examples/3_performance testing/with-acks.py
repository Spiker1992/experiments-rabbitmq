# 1882 messages sent, 1881.97 msg/sec (avg)
# 3792 messages sent, 1895.81 msg/sec (avg)
# 5593 messages sent, 1863.95 msg/sec (avg)
# 7489 messages sent, 1871.91 msg/sec (avg)
# 9314 messages sent, 1862.51 msg/sec (avg)
# 11207 messages sent, 1867.54 msg/sec (avg)
# 13090 messages sent, 1869.62 msg/sec (avg)
import pika
import time

# Hardcoded queue name
QUEUE_NAME = "test_queue_with_acks_classic"
MESSAGE_COUNT = 100000

# Connect to RabbitMQ (default localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue (non-durable, non-persistent)
channel.queue_declare(queue=QUEUE_NAME, durable=True)
channel.confirm_delivery() # Enable publisher confirms - this will raise an exception if the message cannot be delivered
# Start timer
start_time = time.time()
last_report_time = start_time
messages_sent = 0

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

connection.close()
