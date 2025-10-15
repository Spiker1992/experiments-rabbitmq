## Using stream as a dead letter exchange

1. shut down existing container if necessary:
```
docker stop rabbitmq
docker rm rabbitmq
```
2. docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
3. Inspect queues (optional):
```
docker exec rabbitmq rabbitmqctl list_queues | cat
```

```
python3 -m examples.stream_as_a_dead_letter_queue_10.consumer
python3 -m examples.stream_as_a_dead_letter_queue_10.publisher
```