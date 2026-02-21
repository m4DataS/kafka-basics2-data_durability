# Kafka Durability & Min In-Sync Replicas Experiment

This experiment demonstrates how Kafka enforces `min.insync.replicas` and how producers behave when brokers fail.

---

## 00 Initial Topic Configuration

```text
Topic: durable-topic
Partitions: 3
  Partition 0: Leader=1, Replicas=[2, 1, 3], ISR=[1, 3, 2]
  Partition 2: Leader=1, Replicas=[1, 3, 2], ISR=[1, 3, 2]
  Partition 1: Leader=1, Replicas=[3, 2, 1], ISR=[1, 3, 2]
```

## Producer sends messages

```text
Sent a to partition 1
Sent b to partition 2
Sent c to partition 1
Sent d to partition 2
Sent e to partition 2
```

## 2 Consumer receive messages

```text
Listening for messages...
Received: a
Received: c
Received: b
Received: d
Received: e
```

## 3 Kill a broker

```text
Topic: durable-topic
Partitions: 3
  Partition 0: Leader=1, Replicas=[2, 1, 3], ISR=[1, 2]
  Partition 2: Leader=1, Replicas=[1, 3, 2], ISR=[1, 2]
  Partition 1: Leader=1, Replicas=[3, 2, 1], ISR=[1, 2]
```

## 4 Producer send more messages

```text
Sent av2 to partition 0
Sent bv2 to partition 0
Sent cv2 to partition 1
Sent dv2 to partition 0
Sent ev2 to partition 2
```

## 5 Consumer receive more messages

```text
Received: av2
Received: bv2
Received: cv2
Received: dv2
Received: ev2
```

## 6 Kill another broker : only 1 broker left, min ISR not reached

```text
Topic: durable-topic
Partitions: 3
  Partition 0: Leader=1, Replicas=[2, 1, 3], ISR=[1]
  Partition 2: Leader=1, Replicas=[1, 3, 2], ISR=[1]
  Partition 1: Leader=1, Replicas=[3, 2, 1], ISR=[1]
```

## 7 Producer tries to send more messages

```text
Failed to send av3: [Error 19] NotEnoughReplicasError: None
Failed to send bv3: [Error 19] NotEnoughReplicasError: None
Failed to send cv3: [Error 19] NotEnoughReplicasError: None
Failed to send dv3: [Error 19] NotEnoughReplicasError: None
Failed to send ev3: [Error 19] NotEnoughReplicasError: None
```

## 8 Conclusion

- Kafka enforces `min.insync.replicas` to ensure data durability
- Producers must wait for ISR to acknowledge writes
- When ISR is too small, min.insync.replicas is not satisfied, producers get `NotEnoughReplicasError` : messages cannot be sent .
- Producers should be configured to handle these erros:
  - Queue messages locally
  - Retry automatically
  - Wait until the cluster has enough available brokers
- When ISR is too small, producers get `NotEnoughReplicasError`
- This ensures no data loss in case of broker failures
