# =====================================================
# STREAMLIT APP: FOREST COVER TYPE PREDICTION
# VISUAL STUDIO READY
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -----------------------------------------------------
# LOAD SAVED MODEL & FEATURES
# -----------------------------------------------------

MODEL_PATH = "models/final_random_forest_model.pkl"
FEATURES_PATH = "models/model_features.pkl"

model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURES_PATH)

# -----------------------------------------------------
# TARGET LABEL INVERSE MAPPING
# -----------------------------------------------------

cover_type_mapping = {
    0: "Aspen",
    1: "Cottonwood / Willow",
    2: "Douglas-fir",
    3: "Krummholz",
    4: "Lodgepole Pine",
    5: "Ponderosa Pine",
    6: "Spruce / Fir"
}

# -----------------------------------------------------
# STREAMLIT PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Forest Cover Type Predictor",
    layout="centered"
)

st.title("🌲 Forest Cover Type Prediction")
st.write(
    "Enter geographical and environmental features below to predict "
    "the **forest cover type**."
)

st.markdown("---")

# -----------------------------------------------------
# INPUT FORM
# -----------------------------------------------------

st.subheader("🔢 Input Feature Values")

user_input = {}

for feature in feature_names:

    # Binary wilderness columns
    if feature.startswith("Wilderness_Area"):
        user_input[feature] = st.selectbox(
            label=feature,
            options=[0, 1],
            index=0
        )

    # Numeric features
    else:
        user_input[feature] = st.number_input(
            label=feature,
            value=0.0,
            step=1.0
        )

# -----------------------------------------------------
# PREDICTION
# -----------------------------------------------------

st.markdown("---")

if st.button("🔍 Predict Forest Cover Type"):

    input_df = pd.DataFrame([user_input])

    prediction = model.predict(input_df)[0]
    predicted_label = cover_type_mapping[prediction]

    st.success(
        f"🌳 **Predicted Forest Cover Type:** {predicted_label}"
    )

    st.info(
        "Prediction generated using a trained Random Forest model "
        "with optimized hyperparameters."
    )

# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------

st.markdown("---")
st.caption("EcoType Project | Forest Cover Type Prediction using Machine Learning")