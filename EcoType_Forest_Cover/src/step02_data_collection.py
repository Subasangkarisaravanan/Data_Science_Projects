# src/step02_data_collection.py
import pandas as pd

df = pd.read_csv("data/forest_cover.csv")
print("Dataset Loaded")
print("Shape:", df.shape)
print(df.head())