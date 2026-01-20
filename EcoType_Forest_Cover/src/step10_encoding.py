# src/step10_encoding.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib, os

df = pd.read_csv("data/forest_engineered.csv")

le = LabelEncoder()
df["Cover_Type"] = le.fit_transform(df["Cover_Type"])

os.makedirs("models", exist_ok=True)
joblib.dump(le, "models/label_encoder.pkl")

df.to_csv("data/final_processed_data.csv", index=False)
print("Encoding done")