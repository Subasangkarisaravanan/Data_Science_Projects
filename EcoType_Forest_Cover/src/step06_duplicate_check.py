# src/step06_duplicate_check.py
import pandas as pd

df = pd.read_csv("data/forest_cover.csv")
print("Duplicates:", df.duplicated().sum())