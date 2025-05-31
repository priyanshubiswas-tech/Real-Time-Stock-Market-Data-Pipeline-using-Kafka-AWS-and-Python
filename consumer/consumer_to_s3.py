from kafka import KafkaConsumer
import json, boto3, csv, os
from datetime import datetime

consumer = KafkaConsumer(
    'stock-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

s3 = boto3.client('s3')
bucket_name = 'your-s3-bucket-name'
local_file = 'stock_data.csv'

if not os.path.exists(local_file):
    with open(local_file, 'w', newline='') as f:
        csv.writer(f).writerow(['ticker', 'price', 'timestamp'])

for message in consumer:
    data = message.value
    with open(local_file, 'a', newline='') as f:
        csv.writer(f).writerow([data['ticker'], data['price'], datetime.fromtimestamp(data['timestamp'])])
    s3.upload_file(local_file, bucket_name, f'stock_data/{datetime.now().isoformat()}.csv')
    print("Uploaded:", data)
