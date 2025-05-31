bin/kafka-topics.sh --create \
--topic stock-data \
--bootstrap-server localhost:9092 \
--partitions 1 --replication-factor 1
