import cv2
import numpy as np
import tensorflow as tf

model = tf.saved_model.load('converted_savedmodel/model.savedmodel/saved_model.pb')

# Load labels
with open('converted_savedmodel/labels.txt', 'r') as f:
    class_names = f.read().splitlines()

# Function to preprocess the image
def preprocess_image(image):
    # Assuming your model expects 224x224 images
    image = cv2.resize(image, (224, 224))
    image = image / 255.0  # Normalize pixel values
    return image

# Capture video from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Preprocess the frame
    image = preprocess_image(frame)
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Make prediction
    predictions = model.predict(image)
    predicted_class = np.argmax(predictions[0])

    # Display prediction on the frame
    cv2.putText(frame, class_names[predicted_class], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
