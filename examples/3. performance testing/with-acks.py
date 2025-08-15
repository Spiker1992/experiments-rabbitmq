# 2995 messages sent, 2994.37 msg/sec (avg)
# 6243 messages sent, 3120.81 msg/sec (avg)
# 9474 messages sent, 3157.36 msg/sec (avg)
# 12679 messages sent, 3160.82 msg/sec (avg)
# 15757 messages sent, 3144.23 msg/sec (avg)
# 18533 messages sent, 3082.95 msg/sec (avg)
# 21719 messages sent, 3097.60 msg/sec (avg)
# 24986 messages sent, 3118.70 msg/sec (avg)
# 28205 messages sent, 3129.82 msg/sec (avg)
# 31225 messages sent, 3118.81 msg/sec (avg)
# 34388 messages sent, 3122.72 msg/sec (avg)
# 37656 messages sent, 3134.79 msg/sec (avg)
# 40484 messages sent, 3111.14 msg/sec (avg)
# 43633 messages sent, 3112.65 msg/sec (avg)
# 46550 messages sent, 3099.56 msg/sec (avg)
# 49066 messages sent, 3063.10 msg/sec (avg)
# 52292 messages sent, 3072.66 msg/sec (avg)
# 55573 messages sent, 3084.18 msg/sec (avg)
# 58740 messages sent, 3088.51 msg/sec (avg)
# 61797 messages sent, 3086.91 msg/sec (avg)
# 64692 messages sent, 3077.78 msg/sec (avg)
# 67872 messages sent, 3082.39 msg/sec (avg)
# 71204 messages sent, 3093.22 msg/sec (avg)
# 74453 messages sent, 3099.69 msg/sec (avg)
# 77704 messages sent, 3105.74 msg/sec (avg)
# 80440 messages sent, 3091.52 msg/sec (avg)
# 83594 messages sent, 3093.83 msg/sec (avg)
# 86762 messages sent, 3096.44 msg/sec (avg)
# 89977 messages sent, 3100.53 msg/sec (avg)
# 93207 messages sent, 3104.81 msg/sec (avg)
# 96392 messages sent, 3107.36 msg/sec (avg)
# 99292 messages sent, 3100.87 msg/sec (avg)
# Sent 100000 messages to 'test_queue_with_acks' in 32.2458 seconds
import pika
import time

# Hardcoded queue name
QUEUE_NAME = "test_queue_with_acks"
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
