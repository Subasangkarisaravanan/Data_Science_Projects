import pandas as pd
import os

print("\nSTEP X : SOCIAL LOOP DETECTION")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

df = pd.read_csv(os.path.join(DATA_DIR, "browsing_sessions.csv"))

social = df[df["category"] == "social"]

group = social.groupby("session_id").agg(
    social_pages=("url", "count"),
    total_pages=("pages_visited", "max"),
    hour=("hour", "first")
).reset_index()

group["ratio"] = group["social_pages"] / group["total_pages"]

loops = group[(group["ratio"] > 0.6) & (group["hour"] >= 22)]

print("Social loops:", len(loops))

loops.to_csv(os.path.join(DATA_DIR, "social_loops.csv"), index=False)