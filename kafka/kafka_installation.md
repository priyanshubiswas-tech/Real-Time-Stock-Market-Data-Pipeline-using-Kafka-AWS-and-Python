sudo apt update && sudo apt upgrade -y
sudo apt install default-jdk -y

wget https://downloads.apache.org/kafka/3.0.0/kafka_2.13-3.0.0.tgz
tar -xvzf kafka_2.13-3.0.0.tgz
cd kafka_2.13-3.0.0

# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka Broker
bin/kafka-server-start.sh config/server.properties
