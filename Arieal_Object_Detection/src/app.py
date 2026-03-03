import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from ultralytics import YOLO
import os

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="Aerial Object AI System", layout="wide")

st.title("🛰 Aerial Object Classification & Detection System")
st.write("Detect whether the object is a Bird or Drone using Classification and YOLOv8 Detection.")

# ==========================
# LOAD MODELS
# ==========================
@st.cache_resource
def load_classification_model():
    model = tf.keras.models.load_model(
        "models/mobilenet_best.h5",
        compile=False
    )
    return model

@st.cache_resource
def load_detection_model():
    model = YOLO("src/runs/detect/yolov8_bird_drone2/weights/best.pt")
    return model

classification_model = load_classification_model()
detection_model = load_detection_model()

# ==========================
# IMAGE UPLOAD
# ==========================
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    col1, col2 = st.columns(2)

    # ==========================
    # CLASSIFICATION
    # ==========================
    with col1:
        st.subheader("📌 Classification Result")

        img_resized = image.resize((224, 224))
        img_array = np.array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = classification_model.predict(img_array)[0][0]

        class_name = "Drone" if prediction > 0.5 else "Bird"
        confidence = prediction if prediction > 0.5 else 1 - prediction

        st.success(f"Prediction: {class_name}")
        st.write(f"Confidence: {confidence:.4f}")

    # ==========================
    # DETECTION
    # ==========================
    with col2:
        st.subheader("🎯 Object Detection (YOLOv8)")

        if st.button("Run Detection"):

            results = detection_model.predict(image, conf=0.25)

            result_image = results[0].plot()
            result_image = Image.fromarray(result_image)

            st.image(result_image, caption="Detection Result", use_column_width=True)

            boxes = results[0].boxes
            if boxes is not None:
                st.write("Detected Objects:")
                for box in boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = detection_model.names[cls_id]
                    st.write(f"- {label} ({conf:.2f})")

st.markdown("---")
st.markdown("Developed for Aerial Object Classification & Detection Project")