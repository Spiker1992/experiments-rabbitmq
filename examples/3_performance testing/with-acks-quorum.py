
# 909 messages sent, 908.69 msg/sec (avg)
# 1831 messages sent, 915.28 msg/sec (avg)
# 2720 messages sent, 902.36 msg/sec (avg)
# 3641 messages sent, 905.97 msg/sec (avg)
# 4490 messages sent, 893.01 msg/sec (avg)
# 5424 messages sent, 899.73 msg/sec (avg)
# 6331 messages sent, 900.40 msg/sec (avg)
# 7253 messages sent, 903.07 msg/sec (avg)
# 8168 messages sent, 904.36 msg/sec (avg)
# 9002 messages sent, 897.31 msg/sec (avg)
# 9840 messages sent, 891.90 msg/sec (avg)
import pika
from config import RABBITMQ_HOST
import time

# Hardcoded queue name
QUEUE_NAME = "test_queue_with_acks_quorum"
MESSAGE_COUNT = 100000

# Connect to RabbitMQ (default localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

 # Declare quorum queue
channel.queue_declare(
	queue=QUEUE_NAME,
	durable=True,
	arguments={"x-queue-type": "quorum"}
)
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
