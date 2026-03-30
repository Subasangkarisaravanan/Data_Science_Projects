import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

from src.config.paths import SESSION_HISTORY  # ✅ correct path

print("\n================================================")
print("STEP X : LSTM SEQUENCE MODEL")
print("================================================\n")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

if not os.path.exists(SESSION_HISTORY):
    print("❌ File not found:", SESSION_HISTORY)
    exit()

df = pd.read_csv(SESSION_HISTORY)

if df.empty:
    print("⚠️ No data available")
    exit()

print(f"📊 Rows loaded: {len(df)}")

# ------------------------------------------------
# SORT DATA
# ------------------------------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df.dropna(subset=["timestamp"], inplace=True)

df = df.sort_values("timestamp")

# ------------------------------------------------
# ENCODE CATEGORY
# ------------------------------------------------

encoder = LabelEncoder()
df["category_encoded"] = encoder.fit_transform(df["category"])

encoded = df["category_encoded"].values

print("\n📋 Categories:", list(encoder.classes_))

# ------------------------------------------------
# CREATE SEQUENCES
# ------------------------------------------------

SEQ = 5

X, y = [], []

for i in range(len(encoded) - SEQ):
    X.append(encoded[i:i+SEQ])
    y.append(encoded[i+SEQ])

X = np.array(X).reshape(-1, SEQ, 1)
y = to_categorical(y)

print(f"\n📊 Total sequences: {len(X)}")

# ------------------------------------------------
# TRAIN TEST SPLIT (IMPORTANT 🔥)
# ------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# ------------------------------------------------
# MODEL
# ------------------------------------------------

model = Sequential([
    LSTM(64, input_shape=(SEQ, 1)),
    Dense(32, activation='relu'),
    Dense(y.shape[1], activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\n🤖 Training model...\n")

history = model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=1
)

# ------------------------------------------------
# EVALUATION
# ------------------------------------------------

loss, acc = model.evaluate(X_test, y_test, verbose=0)

print("\n📊 Test Accuracy:", round(acc, 4))

# ------------------------------------------------
# 🔥 PREDICTION DEMO (IMPORTANT)
# ------------------------------------------------

sample_seq = X_test[0].reshape(1, SEQ, 1)

pred = model.predict(sample_seq, verbose=0)
pred_class = np.argmax(pred)

pred_label = encoder.inverse_transform([pred_class])[0]

print("\n🔮 Sample Prediction:")
print("Predicted next category:", pred_label)

# ------------------------------------------------
# SAVE MODEL (OPTIONAL)
# ------------------------------------------------

MODEL_PATH = os.path.join(os.path.dirname(SESSION_HISTORY), "lstm_model.h5")
model.save(MODEL_PATH)

print("\n💾 Model saved at:", MODEL_PATH)

print("\n================================================")
print("✅ LSTM TRAINING COMPLETED")
print("================================================")