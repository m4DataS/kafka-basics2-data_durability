from kafka import KafkaProducer
import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092','localhost:9093','localhost:9094'],
    acks='all',                # Wait for all ISR to ack
    retries=5,                  # Retry if cluster cannot accept
    linger_ms=10,               # Small delay to batch messages
    max_in_flight_requests_per_connection=1,
    key_serializer=str.encode,
    value_serializer=str.encode
)

messages = ["av3", "bv3", "cv3", "dv3", "ev3"]

for msg in messages:
    try:
        future = producer.send("durable-topic", key=msg, value=msg)
        record_metadata = future.get(timeout=10)
        print(f"Sent {msg} to partition {record_metadata.partition}")
    except Exception as e:
        print(f"Failed to send {msg}: {e}")
        # Could buffer locally or retry manually

producer.flush()
producer.close()