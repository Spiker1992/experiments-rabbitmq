# 10285 messages sent, 10283.85 msg/sec (avg)
# 20496 messages sent, 10247.09 msg/sec (avg)
# 30216 messages sent, 10071.38 msg/sec (avg)
# 40224 messages sent, 10055.41 msg/sec (avg)
# 50745 messages sent, 10148.47 msg/sec (avg)
# 61505 messages sent, 10250.35 msg/sec (avg)
# 72421 messages sent, 10345.39 msg/sec (avg)
# 82072 messages sent, 10258.42 msg/sec (avg)
# 92003 messages sent, 10221.97 msg/sec (avg)
# Sent 100000 messages to 'test_queue_durable' in 9.7737 seconds
import pika
import time

# Hardcoded queue name
QUEUE_NAME = "test_queue_durable"
MESSAGE_COUNT = 100000

# Connect to RabbitMQ (default localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue (non-durable, non-persistent)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# Start timer
start_time = time.time()
last_report_time = start_time
messages_sent = 0

for i in range(MESSAGE_COUNT):
	channel.basic_publish(
		exchange='',
		routing_key=QUEUE_NAME,
		body=f"Message {i+1}",
		properties=pika.BasicProperties(delivery_mode=2)  # persistent
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
