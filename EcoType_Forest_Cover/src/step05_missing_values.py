# src/step05_missing_values.py
import pandas as pd

df = pd.read_csv("data/forest_cover.csv")
print(df.isnull().sum())