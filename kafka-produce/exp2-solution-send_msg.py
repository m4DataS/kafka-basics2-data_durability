# naive_durable_producer.py
import time
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError, NotEnoughReplicasError

# Configuration
BROKERS = ["localhost:9092","localhost:9093","localhost:9094"]
TOPIC = "durable-topic"
MAX_TRIES = 3         # immediate retry attempts
WAIT_TIME = 30        # seconds to wait before retrying after failure

# Example messages to send
messages = ["av3", "bv3", "cv3", "dv3", "ev3"]

# Create Kafka producer with acks=all for durability
producer = KafkaProducer(
    bootstrap_servers=BROKERS,
    acks='all',
    retries=0,  # we'll handle retries manually
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Local queue for messages that failed to send
message_queue = []

# Function to send a message with retries
def send_message(msg):
    tries = 0
    while tries < MAX_TRIES:
        try:
            future = producer.send(TOPIC, value=msg)
            future.get(timeout=10)  # wait for ack
            print(f"Sent {msg}")
            return True
        except NotEnoughReplicasError as e:
            tries += 1
            print(f"Failed to send {msg}: Not enough replicas, attempt {tries}/{MAX_TRIES}")
        except KafkaError as e:
            tries += 1
            print(f"Failed to send {msg}: {e}, attempt {tries}/{MAX_TRIES}")

    # If all tries fail, queue the message for later
    print(f"Queuing {msg} for retry after waiting {WAIT_TIME} seconds")
    message_queue.append(msg)
    return False

# First pass: try sending all messages
for msg in messages:
    send_message(msg)

# Wait and retry queued messages
if message_queue:
    print(f"\nWaiting {WAIT_TIME} seconds before retrying queued messages...")
    time.sleep(WAIT_TIME)

    for msg in list(message_queue):  # copy of the list to iterate safely
        if send_message(msg):
            message_queue.remove(msg)

# Close producer
producer.flush()
producer.close()
print("All done!")