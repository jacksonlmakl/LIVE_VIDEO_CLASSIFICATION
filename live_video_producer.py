import cv2
from kafka import KafkaProducer

# Kafka setup
kafka_topic = 'frame_topic'
kafka_server = 'localhost:9092'  # Change this to your Kafka server address
producer = KafkaProducer(bootstrap_servers=[kafka_server])

# Define a video capture object
vid = cv2.VideoCapture(0)

# Initialize variables
prev_frame = None
frame_count = 0
significant_change_threshold = 1500  # Adjust based on testing
sharpness_threshold = 35.0  # Adjust based on testing for motion blur detection

def is_sharp(image, threshold):
    """Return True if the image is sharp enough, False otherwise."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    if fm > threshold:
        print(fm)
        return True
    else:
        return False

start_capture = False
while True:
    # Capture the video frame by frame
    ret, frame = vid.read()

    # Check if frame is grabbed
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to grayscale and blur it to reduce noise
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if prev_frame is None:
        prev_frame = gray_frame
        continue

    # Calculate the absolute difference and apply threshold
    frame_delta = cv2.absdiff(prev_frame, gray_frame)
    thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours on the thresholded image to detect significant changes
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Evaluate if any contour is large enough to be considered a significant change
    significant_change_detected = any(cv2.contourArea(contour) > significant_change_threshold for contour in contours)

    if significant_change_detected or frame_count == 0:
        start_capture = True
    if start_capture == True:
        if is_sharp(frame, sharpness_threshold):
            print("FRAME SENT")
            # Convert the frame to a byte array and send it to Kafka
            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send(kafka_topic, buffer.tobytes())
            frame_count += 1
            start_capture = False

    # Update the previous frame
    prev_frame = gray_frame

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # 'q' button is set as the quitting button
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the capture object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

