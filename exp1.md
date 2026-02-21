# Experiment 1 : discover Brokers

1. Create topic with 3 partitions and replication factor 3 from `kafka-config/exp1-create_topic.py`
2. Describe topic to check replicas and ISR via script `kafka-config/exp1-collect_topic_info.py`

## Observed ISR Changes

1. Initial State (All Brokers Active)

```text
Partition 0: Leader=3, Replicas=[3,1,2], ISR=[3,2,1]
Partition 1: Leader=3, Replicas=[1,2,3], ISR=[3,2,1]
Partition 2: Leader=3, Replicas=[2,3,1], ISR=[3,1,2]
```

- All replicas are in sync
- Cluster fully healthy

1. Broker 3 Deactivated
Kill broker 3 using Docker desktop UI

```text
Partition 0: Leader=1, Replicas=[3,1,2], ISR=[2,1]
Partition 1: Leader=1, Replicas=[1,2,3], ISR=[2,1]
Partition 2: Leader=2, Replicas=[2,3,1], ISR=[1,2]
```

- Leader moves to another in-sync replica
- ISR shrinks, excluding broker 3
- Demonstrates failover and resilience

1. Broker 3 Reactivated
Restart it using Docker desktop UI

```text
Partition 0: ISR=[2,1,3]
Partition 1: ISR=[2,1,3]
Partition 2: ISR=[1,2,3]
```

- Broker 3 catches up
- ISR grows back to include all brokers
- Cluster fully recovered

## Key Observations

- Replicas = static broker assignment for the partition → never changes automatically
- ISR = dynamic list of in-sync, live replicas → changes when brokers fail or recover
- Kafka ensures high availability and no data loss as long as replication factor ≥ 2

## Experiment 2 : dig deeper in Brokers management
