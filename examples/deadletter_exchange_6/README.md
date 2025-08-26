1. shut down existing container if necessary:
```
docker stop rabbitmq
docker rm rabbitmq
```
2. docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
3. open 2 cli windows side by side. 1 will be a publisher and the other 1 are consumers
4. in the publisher window run `python3 -m examples.deadletter_exchange_6.publisher`. 
5. now run `docker exec rabbitmq rabbitmqctl list_queues` - this will show current queue
```
docker exec rabbitmq rabbitmqctl list_queues
Timeout: 60.0 seconds ...
Listing queues for vhost / ...
name    messages
deadletter_exchange_6   11
dlq     0
```
6. in the consumer windows run `python3 -m examples.deadletter_exchange_6.consumer`
7. run `docker exec rabbitmq rabbitmqctl list_queues` one more time
```
docker exec rabbitmq rabbitmqctl list_queues
Timeout: 60.0 seconds ...
Listing queues for vhost / ...
name    messages
deadletter_exchange_6   0
dlq     11
```

Messages are now in the deadletter queue



# Key things to note

- we need to declare a dead letter exchange, a queue and bind queue to the exchange using a routing key.
- when declaring a queue we need to define dead letter settings (exchange + routing key) via arguments
- if routing key not used the queue name, where message failed, is used instead
- when consuming messages we need to trigger a negative acknowledgement for message to be sent to a dead letter queue