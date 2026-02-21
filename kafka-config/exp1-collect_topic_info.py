from kafka.admin import KafkaAdminClient

# Connect to Kafka
admin = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id="admin-client"
)

# List all topics
topics = admin.list_topics()
print("Existing topics:", topics)

# Describe each topic to get partitions and replication info
for topic_name in topics:
    topic_info = admin.describe_topics([topic_name])
    for info in topic_info:
        print(f"\nTopic: {info['topic']}")
        print(f"Partitions: {len(info['partitions'])}")
        for p in info['partitions']:
            print(f"  Partition {p['partition']}: Leader={p['leader']}, Replicas={p['replicas']}, ISR={p['isr']}")