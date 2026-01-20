# src/step22_app.py

import streamlit as st
import numpy as np
import joblib
import os

# ---------------------------------
# Load model & encoder safely
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "best_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "..", "models", "label_encoder.pkl")

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="EcoType - Forest Cover Prediction",
    layout="centered"
)

st.title("🌲 EcoType: Forest Cover Type Prediction")
st.write(
    "Predict the forest cover type using environmental and cartographic features."
)

st.markdown("---")

# ---------------------------------
# User Input Section
# ---------------------------------
st.header("Enter Feature Values")

Elevation = st.number_input(
    "Elevation (meters)", min_value=1800, max_value=4000, value=2900, step=10
)

Aspect = st.number_input(
    "Aspect (0–360 degrees)", min_value=0, max_value=360, value=120
)

Slope = st.number_input(
    "Slope (degrees)", min_value=0, max_value=60, value=10
)

Horizontal_Distance_To_Hydrology = st.number_input(
    "Horizontal Distance to Hydrology (meters)", min_value=0, max_value=8000, value=1000
)

Vertical_Distance_To_Hydrology = st.number_input(
    "Vertical Distance to Hydrology (meters)", min_value=-500, max_value=500, value=50
)

Horizontal_Distance_To_Roadways = st.number_input(
    "Horizontal Distance to Roadways (meters)", min_value=0, max_value=8000, value=2000
)

Hillshade_9am = st.number_input(
    "Hillshade at 9 AM", min_value=0, max_value=255, value=220
)

Hillshade_Noon = st.number_input(
    "Hillshade at Noon", min_value=0, max_value=255, value=230
)

Hillshade_3pm = st.number_input(
    "Hillshade at 3 PM", min_value=0, max_value=255, value=120
)

Horizontal_Distance_To_Fire_Points = st.number_input(
    "Horizontal Distance to Fire Points (meters)", min_value=0, max_value=8000, value=3000
)

Wilderness_Area = st.selectbox(
    "Wilderness Area", options=[1, 2, 3, 4]
)

Soil_Type = st.selectbox(
    "Soil Type", options=list(range(1, 41))
)

# Derived features (must match training)
Hydrology_Ratio = Horizontal_Distance_To_Hydrology / (abs(Vertical_Distance_To_Hydrology) + 1)
Hillshade_Diff = Hillshade_Noon - Hillshade_9am

st.markdown("---")

# ---------------------------------
# Prediction
# ---------------------------------
if st.button("Predict Forest Cover Type"):

    input_data = np.array([[
        Elevation,
        Aspect,
        Slope,
        Horizontal_Distance_To_Hydrology,
        Vertical_Distance_To_Hydrology,
        Horizontal_Distance_To_Roadways,
        Hillshade_9am,
        Hillshade_Noon,
        Hillshade_3pm,
        Horizontal_Distance_To_Fire_Points,
        Wilderness_Area,
        Soil_Type,
        Hydrology_Ratio,
        Hillshade_Diff
    ]])

    prediction = model.predict(input_data)
    predicted_label = label_encoder.inverse_transform(prediction)

    st.success(f"🌳 Predicted Forest Cover Type: **{predicted_label[0]}**")