# kafka-basics2-data_durability
Demonstrates Kafka replication, ISR, and min.insync.replicas behavior with multi-broker Docker setup. Includes Python producers and consumers illustrating durable message delivery, broker failures, retries, and naive queuing to showcase real-world streaming service resilience.
This repository contains hands-on experiments demonstrating **multi-broker Kafka behavior**, **min.insync.replicas**, and **producer strategies for broker failures**.  
It’s designed as both a **learning resource** and a **portfolio showcase** for data engineering with Kafka.

## 🎯 Project Goal

The goal of this project is to explore Kafka broker behavior, replication, and message durability through hands-on experiments. It demonstrates how topics, partitions, and ISR work, how min.insync.replicas protects data, and how producers can handle temporary broker failures to ensure reliable message delivery.

---

## ⚙️ How to Replicate the Experiments

### 1. Setup Kafka with Docker

Create a `docker-compose.yml`. You can use the one in this repo `docker-compose.yml` or create your own with similar services:

```yaml
version: '3.8'

services:
  zookeeper-pe:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: zookeeper-pe
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka1:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka1-pe
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper-pe:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092,PLAINTEXT_INTERNAL://kafka1:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_INTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT_INTERNAL
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
    depends_on:
      - zookeeper-pe

  kafka2:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka2-pe
    ports:
      - "9093:9093"
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: zookeeper-pe:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9093,PLAINTEXT_INTERNAL://kafka2:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_INTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT_INTERNAL
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
    depends_on:
      - zookeeper-pe

  kafka3:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka3-pe
    ports:
      - "9094:9094"
    environment:
      KAFKA_BROKER_ID: 3
      KAFKA_ZOOKEEPER_CONNECT: zookeeper-pe:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9094,PLAINTEXT_INTERNAL://kafka3:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_INTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT_INTERNAL
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
    depends_on:
      - zookeeper-pe
```

Then run the containers:

```bash
docker-compose up -d
```

Kafka will be available on localhost:9092 and Zookeeper on localhost:2181.

### 2. Setup Python Environment

Create a virtual environment and install the required dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
# .venv\Scripts\activate    # Windows
```

requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Run the Experiments

Each experiment is in its own folder or script:

| Experiment                                | Description                                                   |
|-------------------------------------------|---------------------------------------------------------------|
| exp1- Discover Brokers                    | Create a topic with 3 partitions and replication factor 3; inspect replicas and ISR changes.|
| exp2.P1- Min In-Sync Replicas & Durability| Demonstrate min.insync.replicas, producer behavior when brokers fail, and ISR updates.         |
| exp2.P2- Naive Producer Retry Example     | Show a Python producer queuing messages and retrying when brokers are temporarily unavailable. |


### 4. Notes for Running

- Start Kafka and Zookeeper containers first.
- Activate the Python virtual environment.
- Run each script in order to see the concepts in action.
- You can open multiple consumers to observe group behavior, partition assignment, and key-based ordering.
- Use `docker logs kafka` or `docker exec -it kafka bash` to inspect Kafka internals (e.g., topic partitions, replicas).