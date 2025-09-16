import os

# Centralized RabbitMQ host configuration
# Override with environment variable RABBITMQ_HOST if needed
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")


