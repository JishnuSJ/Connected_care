import os
import numpy as np
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from django.conf import settings
# Define paths to the training data directory and the saved model
BASE_DIR = settings.BASE_DIR  
train_data_dir = os.path.join(BASE_DIR, 'train')
model_path = os.path.join(BASE_DIR, 'r1000.h5')

# Load the trained model
model = load_model(model_path)

# Define a function to preprocess the uploaded image
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))  # Resize to match the input size of the model
    img = img_to_array(img) / 255.0  # Convert to numpy array and normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Define the function to automatically populate class labels
def get_class_labels(data_dir):
    class_labels = sorted(os.listdir(data_dir))
    return class_labels

# Get class labels from training data folders
class_labels = get_class_labels(train_data_dir)

# Define the predict_disease function
import numpy as np
import numpy as np

def predict_disease(image_path):
    try:
        # Preprocess the uploaded image
        processed_image = preprocess_image(image_path)

        # Make predictions using the model
        predictions = model.predict(processed_image)

        # Get the predicted class label and confidence score
        predicted_class_index = np.argmax(predictions)
        prediction_label = class_labels[predicted_class_index]
        confidence_score = predictions[0][predicted_class_index]  # probability of predicted class

        # Disease descriptions for your specific classes
        disease_descriptions = {
            "covid19": "The detected image shows signs consistent with COVID-19. Please consult a doctor for further confirmation.",
            "Normal": "No abnormalities detected in the provided image. Everything appears normal.",
            "pneumonia": "Signs of pneumonia detected. It's advisable to seek medical attention for further evaluation.",
            "tuberculosis": "The image suggests possible indications of tuberculosis. Please consult a healthcare provider for diagnostic confirmation."
        }

        # Compose the response string
        response = f"Predicted Disease: **{prediction_label}**\n"
        response += disease_descriptions.get(prediction_label, "Unknown condition detected. Please consult a specialist.")

        return response

    except Exception as e:
        print("Error:", e)
        return "Error processing the image. Please try again with a valid input."
