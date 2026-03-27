import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

print("\nSTEP X : LSTM")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

df = pd.read_csv(os.path.join(DATA_DIR, "browsing_sessions.csv"))

df = df.sort_values("timestamp")

encoder = LabelEncoder()
encoded = encoder.fit_transform(df["category"])

SEQ = 5

X, y = [], []

for i in range(len(encoded) - SEQ):
    X.append(encoded[i:i+SEQ])
    y.append(encoded[i+SEQ])

X = np.array(X).reshape(-1, SEQ, 1)
y = to_categorical(y)

model = Sequential([
    LSTM(64, input_shape=(SEQ,1)),
    Dense(32, activation='relu'),
    Dense(y.shape[1], activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X, y, epochs=5)

print("\nTraining Done")