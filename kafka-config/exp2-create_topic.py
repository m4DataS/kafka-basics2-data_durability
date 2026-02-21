from kafka.admin import KafkaAdminClient, NewTopic

# Connect to Kafka
admin = KafkaAdminClient(
    bootstrap_servers=["localhost:9092","localhost:9093","localhost:9094"],
    client_id="admin-client"
)

# Define a new topic with 3 partitions, replication factor 3, and min.insync.replicas=2
topic = NewTopic(
    name="durable-topic",
    num_partitions=3,
    replication_factor=3,
    topic_configs={
        "min.insync.replicas": "2"
    }
)

# Create the topic
try:
    admin.create_topics([topic])
    print("Topic 'durable-topic' created with 3 partitions, replication factor 3, min.insync.replicas=2!")
except Exception as e:
    print(f"Error creating topic: {e}")

# Close the admin client
admin.close()