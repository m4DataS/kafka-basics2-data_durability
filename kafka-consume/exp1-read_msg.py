from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'demo-topic',                  # must match producer topic
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # start from beginning if no offsets
    group_id='group1',           # any string
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Listening for messages...")
for message in consumer:
    print(f"Received: {message.value}")
