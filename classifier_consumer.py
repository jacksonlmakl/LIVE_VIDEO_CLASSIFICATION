
from kafka import KafkaConsumer
from PIL import Image
import io
import time
import openai
from transformers import BlipProcessor, BlipForConditionalGeneration
import json

# Initialize BLIP model for image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# OpenAI API setup for GPT-4 Turbo
openai.api_key = json.loads(open("keys.json"))['openai']

# Function to generate cohesive caption with GPT-4 Turbo using chat completions
def generate_cohesive_caption(captions):
    conversation = [
        {"role": "system", "content": "You are a highly intelligent AI trained to summarize captions."},
        {"role": "system", "content": "You will receive multiple captions, some may be duplicates or very similar."},
        {"role": "system", "content": "Your job is to read these captions, and output a master caption for the scene."},
        {"role": "user", "content": "Summarize these captions into a cohesive caption describing whats happening:\n" + "\n".join(captions)}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    return response.choices[0].message.content

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

# Initialize variables for batching captions
last_time = time.time()
captions = []

for message in consumer:
    try:
        # Assuming the message value is the image in bytes
        raw_image = Image.open(io.BytesIO(message.value)).convert('RGB')

        # Perform conditional image captioning
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        captions.append(caption)

        # Every 5 seconds, generate a cohesive caption
        if time.time() - last_time >= 5:
            if captions:
                cohesive_caption = generate_cohesive_caption(captions)
                print(cohesive_caption)
                captions = []  # Reset the captions list for the next interval
            last_time = time.time()

    except Exception as e:
        print(f"Error processing message: {e}")
