# Notes

General recommendation is to not use priority queue. This functionality is available for basic cases. Instead have seperate queues for each priority and manage consumption via adjusting number of consumers per queue.

## Classic Queues
- https://www.rabbitmq.com/docs/priority - general docs on what priority queues are
- https://www.cloudamqp.com/blog/message-priority-in-rabbitmq.html - digested version of above
- https://www.rabbitmq.com/docs/consumer-priority - RabbitMQ has consumer priority too - but this is different to message priority

### Usage
1. Define queue as being a priority queue by setting `x-max-priority` argument, when declaring a queue
2. Set message priority when sending a message, between 0 and the `x-max-priority` value

## Quorum Queues

1. Set message priority when sending a message

- https://www.rabbitmq.com/docs/quorum-queues#feature-matrix - quorum queues also suport message priority, from RabbitMQ 4.0. But, they are enabled by default and support two priority levels only.

> Quorum queues internally only support two priorities: high and normal. Messages without a priority set will be mapped to normal as will priorities 0 - 4. Messages with a priority higher than 4 will be mapped to high.

Q: if we have only two modes, what impact of having a message with priority 0 vs priority 1? Will they be treated the same? 

If we only have two modes then I expect for messages to be either normal or high. So in this case messages will be treated as equal.

# Usage

`python3 -m examples.priority_messages_9.quorum-publisher`
`python3 -m examples.priority_messages_9.quorum-consumer`