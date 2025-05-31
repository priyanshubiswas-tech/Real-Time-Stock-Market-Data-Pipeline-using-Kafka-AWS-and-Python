from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

tickers = ['AAPL', 'GOOG', 'TSLA', 'MSFT']

while True:
    data = {
        'ticker': random.choice(tickers),
        'price': round(random.uniform(100, 1500), 2),
        'timestamp': time.time()
    }
    producer.send('stock-data', value=data)
    print("Produced:", data)
    time.sleep(1)
