# src/step12_train_test_split.py

import pandas as pd
from sklearn.model_selection import train_test_split

print("=" * 70)
print("STEP 12: TRAIN–TEST SPLIT")
print("=" * 70)

df = pd.read_csv("data/final_processed_data.csv")

X = df.drop("Cover_Type", axis=1)
y = df["Cover_Type"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Save splits
X_train.to_csv("data/X_train.csv", index=False)
X_test.to_csv("data/X_test.csv", index=False)
y_train.to_csv("data/y_train.csv", index=False)
y_test.to_csv("data/y_test.csv", index=False)

print("Train/Test split completed and files saved:")
print("X_train:", X_train.shape)
print("X_test :", X_test.shape)

print("=" * 70)