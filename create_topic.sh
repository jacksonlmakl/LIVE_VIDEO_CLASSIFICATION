#!/bin/bash

# Kafka bootstrap server address (Update this with your Kafka server address)
BOOTSTRAP_SERVER="localhost:9092"

# Topic name
TOPIC_NAME="frame_topic"

# Number of partitions (optional, adjust as needed)
PARTITIONS=1

# Replication factor (optional, adjust based on your cluster setup, typically 1 for single-node clusters)
REPLICATION_FACTOR=1

# Create topic
~/kafka_2.13-3.6.1/bin/kafka-topics.sh --create --topic $TOPIC_NAME \
                --bootstrap-server $BOOTSTRAP_SERVER \
                --partitions $PARTITIONS \
                --replication-factor $REPLICATION_FACTOR

echo "Topic $TOPIC_NAME created successfully."
