## Message Priority in RabbitMQ: Classic vs Quorum Queues (with runnable examples)

This directory demonstrates how message priority works in RabbitMQ using both classic queues and quorum queues. It also highlights important caveats you should consider before adopting priority.

Key takeaway: for most production systems, prefer separate queues per priority level and control processing with consumer concurrency. Message priority can be useful for simple, bounded use cases but has trade-offs.

Useful docs:
- https://www.rabbitmq.com/docs/priority (message priority)
- https://www.cloudamqp.com/blog/message-priority-in-rabbitmq.html (overview)
- https://www.rabbitmq.com/docs/consumer-priority (consumer priority — different feature)
- https://www.rabbitmq.com/docs/quorum-queues#feature-matrix (feature comparison between classic and quorum)
- https://www.rabbitmq.com/docs/quorum-queues#priorities (priorities with quorum queues)


## What “message priority” means

When a queue supports priority, the broker prefers delivering higher-priority messages before lower-priority ones. Ordering is not strictly FIFO across the entire queue; it is FIFO within the same priority level. Priority does not preempt a message already delivered to a consumer.


## Project layout

- `constants.py`: declares two queues and opens a shared connection/channel
  - `priority_messages_9_classic`: classic queue with `x-max-priority: 10`
  - `priority_messages_9_quorum`: quorum queue (`x-queue-type: quorum`)
- `classic-publisher.py` and `classic-consumer.py`: classic queue example
- `quorum-publisher.py`, `quorum-publisher-low-priority.py`, and `quorum-consumer.py`: quorum queue examples


## Classic queues: true multi-level priority

Classic queues support N priority levels via the `x-max-priority` argument at declaration time. In this example, `x-max-priority` is set to 10.

How it works here:
- The publisher sends 5 messages with priority 1 and 3 messages with priority 2.
- The consumer receives the 3 higher-priority messages first, then the 5 lower-priority messages.

Run it:
```
python3 -m examples.priority_messages_9.classic-publisher
python3 -m examples.priority_messages_9.classic-consumer
```

What you’ll observe:
- Despite being published interleaved, delivery favors priority 2 messages, then priority 1.


## Quorum queues: two-tier priority only

RabbitMQ 4.0 introduced priority for quorum queues, but only two tiers are supported internally: normal and high.

Mapping:
- Priorities 0–4 → normal
- Priorities ≥5 → high
- Messages without an explicit priority are normal

This repo includes two quorum examples to make that behavior visible.

1) `quorum-publisher.py` (mix of normal and high)
- Sends 5 messages with priority 1 (normal) and 3 with priority 10 (high)
- Expect a delivery pattern that alternates to avoid starvation (commonly approximated as 2 high to 1 low when high is available), but exact interleaving is an implementation detail. You will still see high delivered before low when both are present, with fairness toward low.

2) `quorum-publisher-low-priority.py` (all normal)
- Sends 5 messages with priority 1 and 3 with priority 2. Both map to normal (<5), so delivery is effectively FIFO among all eight messages.

Run it:
```
python3 -m examples.priority_messages_9.quorum-consumer
python3 -m examples.priority_messages_9.quorum-publisher
# or
python3 -m examples.priority_messages_9.quorum-publisher-low-priority
```

What you’ll observe:
- With `quorum-publisher.py`: high-priority messages are delivered preferentially while maintaining some fairness for low-priority messages.
- With `quorum-publisher-low-priority.py`: all messages behave the same (all normal), so order is FIFO.


## Operational notes and caveats

- Prefer separate queues per priority: It’s simpler to reason about throughput, scaling, and backlogs by dedicating a queue to each priority and adjusting consumer counts per queue.
- Priority is not preemption: Messages already delivered to a consumer won’t be “taken back” if higher-priority messages arrive later.
- Ordering guarantees: FIFO applies within the same priority. Across priorities, higher-priority messages may “overtake” lower-priority ones.
- Starvation: Classic queues can starve low-priority messages if the high-priority stream never ends. Quorum queues adopt fairness to mitigate this but still prefer high when present.
- Throughput and memory: Priority queues can be more resource-intensive than non-priority queues due to additional indexing and internal data structures (especially classic queues with many levels).
- Consumer priority is different: “Consumer priority” controls which consumers of the same queue get messages first, not message ordering inside the queue.
- Acknowledgements and prefetch: Prefetch and ack strategy affect how quickly newly-arrived high-priority messages become visible for delivery.


## Quick start 

1) Start a consumer (classic or quorum):
```
python3 -m examples.priority_messages_9.classic-consumer
# or
python3 -m examples.priority_messages_9.quorum-consumer
```

2) Publish messages:
```
python3 -m examples.priority_messages_9.classic-publisher
# or
python3 -m examples.priority_messages_9.quorum-publisher
# or
python3 -m examples.priority_messages_9.quorum-publisher-low-priority
```

3) Inspect queues (optional):
```
docker exec rabbitmq rabbitmqctl list_queues | cat
```


## When to use message priority

Use it for small, bounded scenarios where a small fraction of messages must jump the line and you are comfortable with the resource/complexity overhead. Otherwise, model priorities as separate queues and scale consumers independently.