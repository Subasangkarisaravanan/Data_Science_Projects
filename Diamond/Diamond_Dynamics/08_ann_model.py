# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 08_ann_model.py
# STEP 10 – ARTIFICIAL NEURAL NETWORK (FINAL CLEAN VERSION)
# ==========================================================

import os
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ----------------------------------------------------------
# Reproducibility
# ----------------------------------------------------------
np.random.seed(42)
tf.random.set_seed(42)

# ----------------------------------------------------------
# Setup folders
# ----------------------------------------------------------
os.makedirs("plots", exist_ok=True)
os.makedirs("models", exist_ok=True)

print("\n" + "=" * 80)
print("STEP 10: ANN MODEL TRAINING (FINAL CLEAN VERSION)")
print("=" * 80)

# ----------------------------------------------------------
# Load Scaled Data
# ----------------------------------------------------------
X_train = pd.read_csv("data/X_train_scaled.csv").values
X_test = pd.read_csv("data/X_test_scaled.csv").values

y_train = pd.read_csv("data/y_train.csv").values.ravel()
y_test = pd.read_csv("data/y_test.csv").values.ravel()

n_features = X_train.shape[1]
print("\nNumber of Input Features:", n_features)

# ----------------------------------------------------------
# Build ANN Architecture
# ----------------------------------------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(n_features,)),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Dense(16, activation='relu'),

    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='mse'
)

# ----------------------------------------------------------
# Early Stopping
# ----------------------------------------------------------
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

# ----------------------------------------------------------
# Train Model
# ----------------------------------------------------------
history = model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=1
)

# ----------------------------------------------------------
# Evaluate Model
# ----------------------------------------------------------
y_pred = model.predict(X_test).flatten()

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

n = X_test.shape[0]
p = X_test.shape[1]
adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

print("\nANN Performance:")
print(f"MAE: {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R2 Score: {r2:.4f}")
print(f"Adjusted R2: {adjusted_r2:.4f}")

# ----------------------------------------------------------
# Save Model (FIXED WARNING – Native Keras Format)
# ----------------------------------------------------------
model.save("models/ann_model_final.keras")

print("\nModel saved in native Keras format (.keras)")

# ----------------------------------------------------------
# Plot Training Curve
# ----------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title("ANN Training vs Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.tight_layout()
plt.savefig("plots/ann_training_curve.png")
plt.show()

print("\nSTEP 10 COMPLETED SUCCESSFULLY!")
print("=" * 80)