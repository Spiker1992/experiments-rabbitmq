1. shut down existing container if necessary:
```
docker stop rabbitmq
docker rm rabbitmq
```
2. docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
3. open 3 cli windows side by side. 1 will be a publisher and the other 2 are consumers
4. in the consumer windows run `python3 -m examples.4_messages_distribution.consumer`
5. in the publisher window run `python3 -m examples.4_messages_distribution.publisher`. 

This should send messages to RabbitMQ, which then will get consumed by consumers.