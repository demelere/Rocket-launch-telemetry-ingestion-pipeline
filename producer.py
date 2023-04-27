from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

with open('dummy_sensor_data.json') as f:
    data = json.load(f)
    for entry in data:
        producer.send('sensor_data', json.dumps(entry).encode('utf-8'))
