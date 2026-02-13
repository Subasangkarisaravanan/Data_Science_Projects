# ==========================================================
# 💎 DIAMOND DYNAMICS – STREAMLIT DEPLOYMENT APP
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf

# ----------------------------------------------------------
# Page Config
# ----------------------------------------------------------
st.set_page_config(page_title="Diamond Dynamics", layout="centered")

st.title("💎 Diamond Dynamics")
st.subheader("Diamond Price Prediction & Market Segmentation")

# ----------------------------------------------------------
# Load Models & Artifacts
# ----------------------------------------------------------
xgb_model = joblib.load("models/XGBoost.pkl")
scaler = joblib.load("models/regression_scaler.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

kmeans_model = joblib.load("models/kmeans_model.pkl")
clustering_scaler = joblib.load("models/clustering_scaler.pkl")

# ----------------------------------------------------------
# User Inputs
# ----------------------------------------------------------

st.sidebar.header("Enter Diamond Features")

carat = st.sidebar.number_input("Carat", min_value=0.1, max_value=5.0, value=1.0)
depth = st.sidebar.number_input("Depth", min_value=50.0, max_value=70.0, value=61.5)
table = st.sidebar.number_input("Table", min_value=50.0, max_value=70.0, value=57.0)

color = st.sidebar.selectbox(
    "Color",
    ["D", "E", "F", "G", "H", "I", "J"]
)

clarity = st.sidebar.selectbox(
    "Clarity",
    ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2"]
)

# ----------------------------------------------------------
# One-Hot Encoding (Manual Alignment)
# ----------------------------------------------------------

input_dict = {
    "carat": carat,
    "depth": depth,
    "table": table
}

# Initialize dummy columns
for col in feature_columns:
    if col not in input_dict:
        input_dict[col] = 0

# Handle color dummies
if f"color_{color}" in feature_columns:
    input_dict[f"color_{color}"] = 1

# Handle clarity dummies
if f"clarity_{clarity}" in feature_columns:
    input_dict[f"clarity_{clarity}"] = 1

# Create DataFrame
input_df = pd.DataFrame([input_dict])

# Ensure correct column order
input_df = input_df[feature_columns]

# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------

if st.button("Predict Price"):

    # Scale input
    scaled_input = scaler.transform(input_df)

    # Predict log price
    log_price_pred = xgb_model.predict(scaled_input)[0]

    # Convert back to USD
    price_usd = np.expm1(log_price_pred)

    st.success(f"Predicted Diamond Price: ${price_usd:,.2f}")

    # ------------------------------------------------------
    # Market Segmentation Prediction
    # ------------------------------------------------------

    cluster_input = pd.DataFrame(
        [[carat, depth, table, log_price_pred]],
        columns=["carat", "depth", "table", "price"]
    )

    cluster_scaled = clustering_scaler.transform(cluster_input)
    cluster_label = kmeans_model.predict(cluster_scaled)[0]

    segment_map = {
        0: "Premium Segment",
        1: "Mid-Range Segment",
        2: "Luxury Segment",
        3: "Budget Segment"
    }

    segment_name = segment_map.get(cluster_label, "Segment")

    st.info(f"Market Segment: {segment_name}")