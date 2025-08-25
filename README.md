# Experiments with RabbitMQ and Pika (Python)


# Requirements
To run this project you will need access to Docker Desktop. 

Once docker is installed and this repository is on your local machine, run the following commands to set things up:
- Docker `docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management`
- Packages `pip install -r requirements.txt

## Example Running command against RabbitMQ

```
docker exec rabbitmq rabbitmqctl list_queues
```

# What is covered

1. Basic publishing example
2. What happens when publishing to an non existent queue?
3. What performance might you expect from RabbitMQ?
4. How RabbitMQ distributes messages
5. What is prefetching?
6. How does dead letter queue works?

## This that will be added
[] How can I retry processing a message?
[] How message prioritisation works?
[] Can I delay a message delievery?
[] Can message confirms be non blocking?
[] How message persistance works?
[] Poison message, what is it?
[] Making RabbitMQ fault tolorant with Quorum queues

### delivery methods
[] fanout
[] topic
[] streams

### exchanges 
[] consistent hashing exchange
[] random routing exchange
[] internal event exchange 
[] delayed message exchange 

### implementing real world examples?
[] burst of traffic? aka uber/ticket master example?