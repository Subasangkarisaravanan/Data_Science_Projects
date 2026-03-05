import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import StandardScaler

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam

print("\n================================================")
print("STEP 7 : ANOMALY DETECTION (AUTOENCODER)")
print("================================================\n")

# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

input_file = os.path.join(DATA_DIR, "session_features.csv")
output_file = os.path.join(DATA_DIR, "session_anomalies.csv")

print("Input file:")
print(input_file)

# ------------------------------------------------
# Load dataset
# ------------------------------------------------

df = pd.read_csv(input_file)

print("\nRows loaded:", len(df))

# ------------------------------------------------
# Features for anomaly detection
# ------------------------------------------------

features = df[[
    "session_length",
    "pages_visited",
    "unique_domains",
    "domain_switches",
    "session_complexity",
    "ram_per_page",
    "session_intensity"
]]

# ------------------------------------------------
# Scaling
# ------------------------------------------------

scaler = StandardScaler()
X = scaler.fit_transform(features)

# ------------------------------------------------
# Autoencoder architecture
# ------------------------------------------------

input_dim = X.shape[1]

input_layer = Input(shape=(input_dim,))

encoder = Dense(8, activation="relu")(input_layer)
encoder = Dense(4, activation="relu")(encoder)

decoder = Dense(8, activation="relu")(encoder)
decoder = Dense(input_dim, activation="linear")(decoder)

autoencoder = Model(inputs=input_layer, outputs=decoder)

autoencoder.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="mse"
)

print("\nTraining autoencoder...\n")

autoencoder.fit(
    X,
    X,
    epochs=50,
    batch_size=32,
    shuffle=True,
    verbose=0
)

# ------------------------------------------------
# Reconstruction error
# ------------------------------------------------

reconstructions = autoencoder.predict(X)

mse = np.mean(np.power(X - reconstructions, 2), axis=1)

df["anomaly_score"] = mse

# ------------------------------------------------
# Threshold
# ------------------------------------------------

threshold = np.percentile(mse, 95)

print("Anomaly threshold:", threshold)

df["is_anomaly"] = df["anomaly_score"] > threshold

# ------------------------------------------------
# Show anomalies
# ------------------------------------------------

anomalies = df[df["is_anomaly"]]

print("\nTop anomalous sessions:\n")

print(anomalies.sort_values("anomaly_score", ascending=False).head())

# ------------------------------------------------
# Save dataset
# ------------------------------------------------

df.to_csv(output_file, index=False)

print("\n================================================")
print("ANOMALY DATASET SAVED")
print("================================================")

print("Output file:")
print(output_file)

print("\nTotal anomalies detected:", len(anomalies))

print("\n================================================")
print("STEP 7 COMPLETED")
print("================================================")