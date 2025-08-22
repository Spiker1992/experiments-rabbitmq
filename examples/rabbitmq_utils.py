import time
import pika

DELIVERY_MODE_PERSISTENT = 2

def publish_bulk_messages(channel, queue_name, message_count, verbose=True):
    start_time = time.time()
    last_report_time = start_time
    messages_sent = 0
    if verbose:
        print("Starting message publishing...")
    for i in range(message_count):
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=f"Message {i+1}",
            properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT),
            mandatory=True
        )
        messages_sent += 1
        current_time = time.time()
        if verbose and current_time - last_report_time >= 1:
            mps = messages_sent / (current_time - start_time)
            print(f"{messages_sent} messages sent, {mps:.2f} msg/sec (avg)")
            last_report_time = current_time
    end_time = time.time()
    elapsed = end_time - start_time
    if verbose:
        print(f"Sent {message_count} messages to '{queue_name}' in {elapsed:.4f} seconds")
