# src/step04_target_analysis.py
import pandas as pd

df = pd.read_csv("data/forest_cover.csv")
print(df["Cover_Type"].value_counts())
print(df["Cover_Type"].value_counts(normalize=True)*100)