# 📈 Real-Time Stock Market Data Pipeline using Kafka, AWS, and Python

This project demonstrates a real-time streaming pipeline that simulates stock market data, processes it with Kafka, stores it in AWS S3, and queries it using AWS Athena.

---

## 🎯 What You Will Learn

👉 Build a real-time simulation app using Python
👉 Understand Kafka fundamentals (Broker, Producer, Consumer, Zookeeper)
👉 Install and configure Kafka on an EC2 instance
👉 Write Kafka Producer and Consumer using Python
👉 Stream and store data to AWS S3
👉 Query real-time data using AWS Athena

---

## 🏗 Architecture Diagram

```
+-------------+       +-------------+       +-------------+       +-------------+
| Stock Data  | --->  | Kafka       | --->  | Consumer    | --->  | S3 Bucket    |
| Simulator   |       | (Broker)    |       | (Python)    |       | (CSV/Parquet)|
+-------------+       +-------------+       +-------------+       +-------------+
                                                                 |
                                                                 v
                                                          +-------------+
                                                          | AWS Athena  |
                                                          +-------------+
```

---

## 📁 Folder Structure

```
real-time-stock-data-pipeline/
🌀
├── kafka/
│   ├── kafka_installation.md         # Kafka + Zookeeper setup guide
│   ├── start_kafka.sh                # Script to start Kafka and Zookeeper
│   └── create_topic.sh               # Script to create Kafka topic
│
├── producer/
│   └── producer.py                   # Simulates stock data and sends to Kafka
│
├── consumer/
│   └── consumer_to_s3.py             # Consumes Kafka data and uploads to S3
│
├── aws/
│   ├── s3_bucket_setup.md            # How to create an S3 bucket
│   ├── athena_query.sql              # SQL to create Athena table
│   └── iam_policy.json               # IAM policy for S3 and Athena access
│
├── data/
│   └── stock_data.csv                # Sample CSV for local testing
│
├── scripts/
│   ├── requirements.txt              # Python dependencies
│   └── setup_env.sh                  # Optional env setup script
│
├── docs/
│   └── architecture_diagram.png      # Visual overview of the architecture
│
├── .gitignore                        # Ignore __pycache__, .env, etc.
├── README.md                         # This documentation
└── LICENSE                           # Project license (MIT)
```

---

## ✨ Deliverables

| Category       | Description                                                               |
| -------------- | ------------------------------------------------------------------------- |
| 💻 Code        | Python scripts for producer (stock simulation) and consumer (S3 uploader) |
| ⚙ Kafka        | Scripts to install Kafka, start services, and create topics               |
| ☁ AWS Config   | Athena SQL query, S3 setup guide, IAM policy                              |
| 🧪 Sample Data | Sample `CSV` for testing without Kafka/S3                                 |
| 📄 Docs        | README, architecture diagram, and optional setup guides                   |
| 📦 Scripts     | Dependency file (`requirements.txt`) and environment setup script         |

---

## 🚀 Getting Started

### 1. Kafka Installation on EC2

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install default-jdk -y

wget https://downloads.apache.org/kafka/3.0.0/kafka_2.13-3.0.0.tgz
tar -xvzf kafka_2.13-3.0.0.tgz
cd kafka_2.13-3.0.0

# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka Broker
bin/kafka-server-start.sh config/server.properties
```

### 2. Create Kafka Topic

```bash
bin/kafka-topics.sh --create \
--topic stock-data \
--bootstrap-server localhost:9092 \
--partitions 1 --replication-factor 1
```

---

## 🧬 Python Code

### ➔ `producer/producer.py`

```python
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
```

### ➔ `consumer/consumer_to_s3.py`

```python
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
```

---

## ☁️ AWS Integration

### ➔ S3 Setup

* Create a new S3 bucket
* Name it `your-s3-bucket-name`
* Allow write permissions via IAM

### ➔ IAM Policy (`aws/iam_policy.json`)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::your-s3-bucket-name/*"]
    }
  ]
}
```

### ➔ Athena Table Creation (`aws/athena_query.sql`)

```sql
CREATE EXTERNAL TABLE stock_data (
  ticker string,
  price double,
  timestamp string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"'
)
LOCATION 's3://your-s3-bucket-name/stock_data/'
TBLPROPERTIES ('has_encrypted_data'='false');
```

---

## 📦 Requirements

### ➔ `scripts/requirements.txt`

```
kafka-python
boto3
```

### ➔ (Optional) Virtual Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r scripts/requirements.txt
```

---

## 📜 References

* [Kafka Documentation](https://kafka.apache.org/documentation/)
* [Kafka-Python Client](https://kafka-python.readthedocs.io/en/master/)
* [AWS S3 Docs](https://docs.aws.amazon.com/s3/)
* [AWS Athena Docs](https://docs.aws.amazon.com/athena/)

---

## 🧠 Future Improvements

* Stream data using Apache Avro or Parquet for better efficiency
* Integrate AWS Glue for schema discovery
* Visualize data using Amazon QuickSight or Streamlit
* Add monitoring/logging with Prometheus + Grafana
* Dockerize the whole system for reproducibility

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
