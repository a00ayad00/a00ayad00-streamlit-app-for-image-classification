
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import streamlit as st
import boto3
import os

# Define class labels
class_labels = ['Formal Men', 'Formal Women', 'Others', 'Saudi Men', 'Saudi Women']


AccessKeyID = st.secrets['AccessKeyID']
SecretAccessKey = st.secrets['SecretAccessKey']


def download():
    if not os.path.exists('model.keras'):
        s3 = boto3.client('s3', aws_access_key_id=AccessKeyID , aws_secret_access_key=SecretAccessKey)
        s3.download_file('saudi-clothes-classification', 'models/pretrained/model.keras','model.keras')

    global model
    model = load_model('model.keras')


def predict(data):
    # Preprocess the image
    image = load_img(data, target_size=(224, 224))  # Resize as per model's input shape
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = image_array / 255.0  # Normalize to [0, 1]

    # Make prediction
    prediction = model.predict(image_array, verbose=0)
    predicted_class = class_labels[np.argmax(prediction)]
    confidence = np.max(prediction) * 100

    return predicted_class, confidence