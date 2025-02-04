import streamlit as st
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import boto3
from dotenv import load_dotenv
import os

load_dotenv()
AccessKeyID = os.environ['AccessKeyID']
SecretAccessKey = os.environ['SecretAccessKey']

if not os.path.exists('model.keras'):
    s3 = boto3.client('s3', aws_access_key_id=AccessKeyID , aws_secret_access_key=SecretAccessKey)
    s3.download_file('saudi-clothes-classification', 'models/pretrained/model.keras','model.keras')

# Load the saved Keras model
model = load_model('model.keras')

# Define class labels
class_labels = ['Formal Men', 'Formal Women', 'Others', 'Saudi Men', 'Saudi Women']

def predict(uploaded_file):
    # Preprocess the image
    image = load_img(uploaded_file, target_size=(224, 224))  # Resize as per model's input shape
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = image_array / 255.0  # Normalize to [0, 1]

    # Make prediction
    prediction = model.predict(image_array, verbose=0)
    predicted_class = class_labels[np.argmax(prediction)]
    confidence = np.max(prediction) * 100

    return predicted_class, confidence

# Streamlit UI
def main():
    st.set_page_config(page_title="Outfit Classifier - Renad Almajed Group", layout="centered")
    
    # Header
    st.title("Renad Almajed Group")
    st.subheader("Outfit Classification Model")
    st.markdown("Upload an image, and our AI model will classify it into one of the following categories:")
    st.markdown("- Formal Men\n- Formal Women\n- Others\n- Saudi Men\n- Saudi Women")
    st.logo(image='logo-1-1.png', size="large", link='https://www.rmg-sa.com/en/')
    

    genre = st.selectbox(
        label = "What would you like to try?",
        options = ["Try existing samples for quick overview", "Choose your own sample"]
    )
    
    if genre == "Try existing samples for quick overview":
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            file1 = r'./ex_images/resised_SaudiMen.jpg'
            st.image(file1)
            if st.button("Predict 1", type="primary"):
                predicted_class, confidence = predict(file1)
                file = file1

        with col2:
            file2 = r'./ex_images/resised_FormalMen.jpg'
            st.image(file2)
            if st.button("Predict 2", type="primary"):
                predicted_class, confidence = predict(file2)
                file = file2

        with col3:
            file3 = r'./ex_images/resised_FormalWomen.jpg'
            st.image(file3)
            if st.button("Predict 3", type="primary"):
                predicted_class, confidence = predict(file3)
                file = file3

        with col4:
            file4 = r'./ex_images/resised_others.jpeg'
            st.image(file4)
            if st.button("Predict 4", type="primary"):
                predicted_class, confidence = predict(file4)
                file = file4

        with col5:
            file5 = r'./ex_images/resised_SaudiWomen.jpg'
            st.image(file5)
            if st.button("Predict 5", type="primary"):
                predicted_class, confidence = predict(file5)
                file = file5

        try:
            if confidence: st.image(file, caption="Sample Image", width=440)
            st.success(f"Prediction: {predicted_class}")
            st.info(f"Confidence: {confidence:.2f}%")
        except Exception as e:
            pass
        

    elif genre == "Choose your own sample":
        # File uploader
        with st.form("my-form", clear_on_submit=True):
            uploaded_file = st.file_uploader("Upload an outfit image in one of the following formats: .jpg, .jpeg or .png", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            submitted = st.form_submit_button("Predict")
        if uploaded_file is not None:
            if isinstance(uploaded_file, str):
                predicted_class, confidence = predict(uploaded_file)
                st.image(uploaded_file, caption=os.path.split(uploaded_file.name)[1], width=240)
                st.success(f"Prediction: {predicted_class}")
                st.info(f"Confidence: {confidence:.2f}%")
            elif isinstance(uploaded_file, list):
                    for i in uploaded_file:
                        try:
                            predicted_class, confidence = predict(i)
                            st.image(i, caption=os.path.split(i.name)[1], width=240)
                            st.success(f"Prediction: {predicted_class}")
                            st.info(f"Confidence: {confidence:.2f}%")
                        except Exception as e:
                            pass        
    

if __name__ == "__main__":
    main()