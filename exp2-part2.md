# Naive Example: Producer Handling Temporary Broker Failures

This example demonstrates how a streaming producer can **queue messages and retry** when Kafka brokers are temporarily unavailable, preserving message durability.

---

## 1 Run the Producer

```text
Failed to send av3: Not enough replicas, attempt 1/3
Failed to send av3: Not enough replicas, attempt 2/3
Failed to send av3: Not enough replicas, attempt 3/3
Queuing av3 for retry after waiting 30 seconds
Failed to send bv3: Not enough replicas, attempt 1/3
Failed to send bv3: Not enough replicas, attempt 2/3
Failed to send bv3: Not enough replicas, attempt 3/3
Queuing bv3 for retry after waiting 30 seconds
Failed to send cv3: Not enough replicas, attempt 1/3
Failed to send cv3: Not enough replicas, attempt 2/3
Failed to send cv3: Not enough replicas, attempt 3/3
Queuing cv3 for retry after waiting 30 seconds
Failed to send dv3: Not enough replicas, attempt 1/3
Failed to send dv3: Not enough replicas, attempt 2/3
Failed to send dv3: Not enough replicas, attempt 3/3
Queuing dv3 for retry after waiting 30 seconds
Failed to send ev3: Not enough replicas, attempt 1/3
Failed to send ev3: Not enough replicas, attempt 2/3
Failed to send ev3: Not enough replicas, attempt 3/3
Queuing ev3 for retry after waiting 30 seconds

Waiting 30 seconds before retrying queued messages...
```

## 2 Check Topic : after restarting One of the Killed Brokers

```text
Topic: durable-topic
Partitions: 3
  Partition 0: Leader=1, Replicas=[2, 1, 3], ISR=[1, 2]
  Partition 2: Leader=1, Replicas=[1, 3, 2], ISR=[1, 2]
  Partition 1: Leader=1, Replicas=[3, 2, 1], ISR=[1, 2]
```

## 3 Producer : after restarting One of the Killed Brokers

```text
Waiting 30 seconds before retrying queued messages...
Sent av3
Sent bv3
Sent cv3
Sent dv3
Sent ev3
All done!
```

## 4 Consumer : after restarting One of the Killed Brokers

```text
Received: av3
Received: bv3
Received: cv3
Received: dv3
Received: ev3
```

## Key Observations

- Messages failed initially due to NotEnoughReplicasError (min.insync.replicas not satisfied).
- The producer queued messages locally and retried after a delay.
- Once a broker became available, all messages were successfully sent.
- This illustrates how a real streaming producer service should handle temporary Kafka failures to prevent data loss.

## Limitations

In real-world scenarios, streaming services or cloud-based producers typically handle broker unavailability automatically or through built-in mechanisms, such as internal message queues, retry policies, or durable buffers, rather than relying on custom Python code. These systems ensure that messages are not lost even when temporary Kafka failures occur, providing resilience without manual intervention.
