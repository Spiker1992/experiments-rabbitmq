# experiments-rabbitmq


# Requirements
- Docker `docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management`
- Packages `pip install -r requirements.txt

## Example Running command against RabbitMQ

```
docker exec rabbitmq rabbitmqctl list_queues
```