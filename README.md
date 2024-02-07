# Live Video Classification

This project aims to classify live video feeds by sending frames from a producer, which captures and processes video frames in real-time, to a consumer, which then generates captions for these frames using a machine learning model. The project is split into two main components: `live_video_producer.py` for capturing and sending video frames, and `classifier_consumer.py` for receiving frames and generating captions.

## Setup and Requirements

Before running the scripts, ensure you have the following requirements installed:

- Python 3.6 or later
- OpenCV-Python
- Kafka-Python
- PyTorch
- Transformers library
- PIL (Python Imaging Library)

Additionally, you will need a running Kafka server. Kafka can be downloaded from [the Apache Kafka website](https://kafka.apache.org/downloads).

### Installation

Install the required Python packages using pip:

```sh
pip install opencv-python kafka-python torch transformers pillow
```

## Configuration

### Kafka Server

Make sure your Kafka server is running and accessible. By default, the scripts are configured to connect to Kafka at `localhost:9092`. You can change this address in both scripts if your Kafka server is running on a different host or port.

### live_video_producer.py

This script captures video frames from the default video capturing device (usually the webcam), processes these frames to detect significant changes and sharpness, and sends them to a Kafka topic if the conditions are met.

- **Kafka Topic**: Change the `kafka_topic` variable if you wish to use a different topic name.
- **Significant Change Threshold**: Adjust the `significant_change_threshold` variable based on your requirements for what constitutes a significant change in the video frame.
- **Sharpness Threshold**: Adjust the `sharpness_threshold` variable to filter out blurry frames.

### classifier_consumer.py

This script listens to the specified Kafka topic, receives video frames, and uses a pretrained BLIP (Bidirectional and Autoregressive Image Processing) model to generate captions for these frames.

- **Kafka Topic**: Ensure this matches the topic used in `live_video_producer.py`.
- **Model**: By default, the script uses the `"Salesforce/blip-image-captioning-large"` model. You can change this to a different model supported by the BLIP architecture.

## Running the Project

1. **Start the Kafka Server**: Refer to the Kafka documentation for instructions on starting your Kafka server.

2. **Run the Producer Script**: Execute the `live_video_producer.py` script to start capturing video frames and sending them to Kafka.

   ```sh
   python live_video_producer.py
   ```

3. **Run the Consumer Script**: In a separate terminal, start the `classifier_consumer.py` script to receive video frames and generate captions.

   ```sh
   python classifier_consumer.py
   ```

## How It Works

- **live_video_producer.py** captures video frames using OpenCV, checks for significant changes and sharpness, and sends qualifying frames to a Kafka topic.
- **classifier_consumer.py** listens for new messages on the Kafka topic, processes each frame using the BLIP model to generate a caption, and prints the caption to the console.

## Limitations and Considerations

- The effectiveness of frame change detection and sharpness can significantly vary depending on the video quality and the environment. You may need to adjust the thresholds based on your specific use case.
- Processing and captioning each frame can be resource-intensive. Ensure your system meets the hardware requirements for running deep learning models.
- Real-time performance depends on the processing power of the producer and consumer systems, as well as the latency between them.

