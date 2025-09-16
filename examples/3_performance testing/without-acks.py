# 9634 messages sent, 9629.65 msg/sec (avg)
# 20078 messages sent, 10035.66 msg/sec (avg)
# 30755 messages sent, 10249.36 msg/sec (avg)
# 42265 messages sent, 10564.44 msg/sec (avg)
# 53078 messages sent, 10613.83 msg/sec (avg)
# 62442 messages sent, 10404.93 msg/sec (avg)
# 72148 messages sent, 10304.95 msg/sec (avg)
# 83093 messages sent, 10384.84 msg/sec (avg)
# 93982 messages sent, 10440.83 msg/sec (avg)
# Sent 100000 messages to 'test_queue' in 9.5170 seconds (no acks)
import pika
from config import RABBITMQ_HOST
import time

# Hardcoded queue name
QUEUE_NAME = "test_queue"
MESSAGE_COUNT = 100000

# Connect to RabbitMQ (default localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Declare queue (non-durable, non-persistent)
channel.queue_declare(queue=QUEUE_NAME, durable=False)

# Start timer
start_time = time.time()
last_report_time = start_time
messages_sent = 0

for i in range(MESSAGE_COUNT):
	channel.basic_publish(
		exchange='',
		routing_key=QUEUE_NAME,
		body=f"Message {i+1}",
		properties=pika.BasicProperties(delivery_mode=1)  # non-persistent
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

print(f"Sent {MESSAGE_COUNT} messages to '{QUEUE_NAME}' in {elapsed:.4f} seconds (no acks)")

connection.close()
