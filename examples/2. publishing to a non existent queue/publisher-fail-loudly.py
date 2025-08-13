# Reference: https://www.rabbitmq.com/docs/publishers#amqp-0-9-1
# Reference: https://www.rabbitmq.com/docs/confirms
# Publisher sends a message to a RabbitMQ queue
#
# run `docker exec rabbitmq rabbitmqctl list_queues` to see messages in the queue
# 
# After deleting the queue, by sending `delete_queue` message, new messages that you send
# will fail loudly due to confirm delivery being enabled and mandatory set to True.
import pika


# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='hello')
channel.confirm_delivery() # Enable publisher confirms - this will raise an exception if the message cannot be delivered

# Infinite loop to prompt user for messages and publish to queue
try:
    while True:
        message = input("Enter a message to publish (Ctrl+C to exit): ")
        if message == "delete_queue":
            channel.queue_delete(queue='hello')
            print("Queue 'hello' deleted. You can now publish messages to a non-existent queue.")
        else:
            channel.basic_publish(
                exchange='', 
                routing_key='hello', 
                body=message, 
                mandatory=True # mandatory=True ensures that the message is returned if the queue does not exist
            )
            print(f"[x] Published '{message}'")
except KeyboardInterrupt:
    print("\nExiting publisher...")
finally:
    connection.close()
