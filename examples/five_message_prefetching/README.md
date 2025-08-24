1. shut down existing container if necessary:
```
docker stop rabbitmq
docker rm rabbitmq
```
2. docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
3. open 3 cli windows side by side. 1 will be a publisher and the other 2 are consumers
4. in the consumer windows run `python3 -m examples.five_message_prefetching.consumer`
5. in the publisher window run `python3 -m examples.five_message_prefetching.publisher`. 
5.1 This should send messages to RabbitMQ, which then will get consumed by consumers.

Example outcome:
- Consumer 1
```
python3 -m examples.five_message_prefetching.consumer
Waiting for messages. To exit press CTRL+C
Received Hello RabbitMQ!
Processing message for 2.35 seconds...
Received Message 2
Processing message for 5.67 seconds...
Received Message 5
Processing message for 3.81 seconds...
Received Message 7
Processing message for 7.00 seconds...
Received Message 10
Processing message for 4.43 seconds...
```

- Consumer 2
```
python3 -m examples.five_message_prefetching.consumer
Waiting for messages. To exit press CTRL+C
Received Message 1
Processing message for 2.48 seconds...
Received Message 3
Processing message for 2.22 seconds...
Received Message 4
Processing message for 5.81 seconds...
Received Message 6
Processing message for 5.40 seconds...
Received Message 8
Processing message for 2.92 seconds...
Received Message 9
Processing message for 5.59 seconds...
```

Consumer 2 handled 6 tasks vs 4 tasks by Consumer 1