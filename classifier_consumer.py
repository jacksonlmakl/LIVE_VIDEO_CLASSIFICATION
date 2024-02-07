from kafka import KafkaConsumer
from PIL import Image
import io
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Kafka consumer setup
topic_name = 'frame_topic'
bootstrap_servers = 'localhost:9092'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[bootstrap_servers],
    auto_offset_reset='earliest',  # Start reading at the earliest message
    enable_auto_commit=True,
    group_id='image-caption-group'  # Consumer group ID
)

# Consume frames from Kafka and transcribe
for message in consumer:
    try:
        # Assuming the message value is the image in bytes
        raw_image = Image.open(io.BytesIO(message.value)).convert('RGB')

        # Perform conditional image captioning
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)

        print(caption)
    except Exception as e:
        print(f"Error processing message: {e}")

