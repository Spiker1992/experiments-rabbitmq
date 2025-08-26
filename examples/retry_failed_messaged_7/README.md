1. shut down existing container if necessary:
```
docker stop rabbitmq
docker rm rabbitmq
```
2. docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
3. open 2 cli windows side by side. 1 will be a publisher and the other 1 are consumers
4. in the publisher window run `python3 -m examples.retry_failed_messaged_7.publisher`. 
5. now run `docker exec rabbitmq rabbitmqctl list_queues` - this will show current queue
```
docker exec rabbitmq rabbitmqctl list_queues
Listing queues for vhost / ...
name    messages
retry_failed_messaged_7 0
```
6. in the consumer windows run `python3 -m examples.retry_failed_messaged_7.consumer`
7. Example output
```json
{'content_type': None, 'content_encoding': None, 'headers': {'x-delivery-count': 3L}, 'delivery_mode': None, 'priority': None, 'correlation_id': None, 'reply_to': None, 'expiration': None, 'message_id': None, 'timestamp': None, 'type': None, 'user_id': None, 'app_id': None, 'cluster_id': None}
{'consumer_tag': 'ctag1.693fe9cd7eea4fa68ca243ddce571142', 'delivery_tag': 4, 'redelivered': True, 'exchange': '', 'routing_key': 'retry_failed_messaged_7'}
```

Please note that `x-delivery-count` keep being incremented. To start with, in the first message this header doesn't exist but added after first nack.

Other thing to note is the `redelivered` flag. It present in both Classic and Quorum queues. This flag is set to True after first redelivery.


# Key things to note

- this needs to be a quorum queue. in a classic queue we can publish a message with our own header.
- we can set delivery limit on the queue itself