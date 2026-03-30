import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import StandardScaler

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam

from src.config.paths import DATA_DIR  # ✅ central config

print("\n================================================")
print("STEP 7 : ANOMALY DETECTION (AUTOENCODER)")
print("================================================\n")

# ------------------------------------------------
# PATHS (FIXED)
# ------------------------------------------------

input_file = os.path.join(DATA_DIR, "processed", "session_features.csv")
output_file = os.path.join(DATA_DIR, "processed", "session_anomalies.csv")

print("📥 Input:", input_file)
print("📤 Output:", output_file)

# ------------------------------------------------
# FILE CHECK
# ------------------------------------------------

if not os.path.exists(input_file):
    print("❌ File not found:", input_file)
    exit()

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

df = pd.read_csv(input_file)

if df.empty:
    print("⚠️ No data available")
    exit()

print(f"\n📊 Rows loaded: {len(df)}")

# ------------------------------------------------
# FEATURE SELECTION (SAFE)
# ------------------------------------------------

feature_cols = [
    "session_length",
    "pages_visited",
    "unique_domains",
    "domain_switches",
    "session_complexity",
    "ram_per_page",
    "session_intensity"
]

# Keep only available columns
feature_cols = [col for col in feature_cols if col in df.columns]

features = df[feature_cols].fillna(0)

print("\n📋 Features used:", feature_cols)

# ------------------------------------------------
# SCALING
# ------------------------------------------------

scaler = StandardScaler()
X = scaler.fit_transform(features)

# ------------------------------------------------
# AUTOENCODER MODEL
# ------------------------------------------------

input_dim = X.shape[1]

input_layer = Input(shape=(input_dim,))

# Encoder
encoder = Dense(8, activation="relu")(input_layer)
encoder = Dense(4, activation="relu")(encoder)

# Decoder
decoder = Dense(8, activation="relu")(encoder)
decoder = Dense(input_dim, activation="linear")(decoder)

autoencoder = Model(inputs=input_layer, outputs=decoder)

autoencoder.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="mse"
)

print("\n🤖 Training autoencoder...\n")

history = autoencoder.fit(
    X,
    X,
    epochs=50,
    batch_size=32,
    shuffle=True,
    validation_split=0.1,
    verbose=0
)

print("✅ Training completed")

# ------------------------------------------------
# RECONSTRUCTION ERROR
# ------------------------------------------------

reconstructions = autoencoder.predict(X, verbose=0)

mse = np.mean(np.power(X - reconstructions, 2), axis=1)

df["anomaly_score"] = mse

# ------------------------------------------------
# THRESHOLD (IMPROVED)
# ------------------------------------------------

threshold = np.percentile(mse, 95)

print("\n🚨 Anomaly threshold:", round(threshold, 6))

df["is_anomaly"] = df["anomaly_score"] > threshold

# ------------------------------------------------
# ANALYSIS OUTPUT
# ------------------------------------------------

anomalies = df[df["is_anomaly"]]

print("\n🔥 TOP ANOMALIES:\n")
print(anomalies.sort_values("anomaly_score", ascending=False).head(10))

print("\n📊 ANOMALY SUMMARY:\n")
print(df["is_anomaly"].value_counts())

print("\n📊 Avg anomaly score:", round(df["anomaly_score"].mean(), 6))
print("📊 Max anomaly score:", round(df["anomaly_score"].max(), 6))

# ------------------------------------------------
# SAVE
# ------------------------------------------------

os.makedirs(os.path.dirname(output_file), exist_ok=True)

df.to_csv(output_file, index=False)

print("\n================================================")
print("✅ ANOMALY DATASET SAVED")
print("================================================")

print("📁 Output file:", output_file)
print(f"🚨 Total anomalies detected: {len(anomalies)}")

print("\n================================================")
print("🚀 STEP 7 COMPLETED")
print("================================================")