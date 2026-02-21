from kafka.admin import KafkaAdminClient, NewTopic

# Connect to Kafka
admin = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id="admin-client"
)

### Creates 1 topic : exp3-key
# Define a new topic with 3 partitions and replication factor 1
topic = NewTopic(
    name="demo-topic",
    num_partitions=3,
    replication_factor=3
)

# Create the topic
admin.create_topics([topic])

print("Topic created with 3 partitions!")
