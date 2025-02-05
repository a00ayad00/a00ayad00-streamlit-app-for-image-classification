import streamlit as st
import os
from model import download, predict

download()

# Streamlit UI
def main():
    st.set_page_config(page_title="Outfit Classifier - Renad Almajed Group", layout="centered")
    
    # Header
    st.title("Renad Almajed Group")
    st.subheader("Outfit Classification Model")
    st.markdown("Upload an image, and our AI model will classify it into one of the following categories:")
    st.markdown("- Formal Men\n- Formal Women\n- Others\n- Saudi Men\n- Saudi Women")
    st.logo(image='logo-1-1.png', size="large", link='https://www.rmg-sa.com/en/')
    

    genre = st.radio(
        label = "What would you like to try?",
        options = ["Try existing samples for quick overview", "Choose your own sample", "Open your camera"]
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
    elif genre == "Open your camera":

        on = st.toggle("Camera switch")
        if on:
            st.write("Camera status: on!")

            picture = st.camera_input("Take a picture", disabled = not on)

            if picture:
                predicted_class, confidence = predict(picture)
                st.image(picture, caption="Camera is open", width=240)
                st.success(f"Prediction: {predicted_class}")
                st.info(f"Confidence: {confidence:.2f}%")

        elif not on:    
            st.write("Camera status: off")


if __name__ == "__main__":
    main()