import pandas as pd
import os

print("\n================================================")
print("STEP 3 : SESSION BUILDING")
print("================================================\n")

# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

input_file = os.path.join(DATA_DIR, "browsing_history_clean.csv")
output_file = os.path.join(DATA_DIR, "browsing_sessions.csv")

print("Input file:")
print(input_file)

# ------------------------------------------------
# Load dataset
# ------------------------------------------------

df = pd.read_csv(input_file)

print("\nRows loaded:", len(df))

df["timestamp"] = pd.to_datetime(df["timestamp"])

# ------------------------------------------------
# Sort by time
# ------------------------------------------------

df = df.sort_values("timestamp").reset_index(drop=True)

# ------------------------------------------------
# Calculate time gap
# ------------------------------------------------

df["time_gap_sec"] = df["timestamp"].diff().dt.total_seconds()

SESSION_TIMEOUT = 900  # 15 minutes

df["new_session"] = (df["time_gap_sec"] > SESSION_TIMEOUT) | df["time_gap_sec"].isna()

df["session_id"] = df["new_session"].cumsum()

# ------------------------------------------------
# Domain switching
# ------------------------------------------------

df["prev_domain"] = df["domain"].shift()

df["domain_switch"] = df["domain"] != df["prev_domain"]

df.loc[df["new_session"], "domain_switch"] = False

# ------------------------------------------------
# Category switching
# ------------------------------------------------

df["prev_category"] = df["category"].shift()

df["category_switch"] = df["category"] != df["prev_category"]

df.loc[df["new_session"], "category_switch"] = False

# ------------------------------------------------
# Session duration
# ------------------------------------------------

session_times = df.groupby("session_id")["timestamp"].agg(["min", "max"])

session_times["session_duration"] = (
    session_times["max"] - session_times["min"]
).dt.total_seconds()

df = df.merge(
    session_times["session_duration"],
    left_on="session_id",
    right_index=True
)

# ------------------------------------------------
# Session statistics
# ------------------------------------------------

session_stats = df.groupby("session_id").agg(
    pages_visited=("url", "count"),
    unique_domains=("domain", "nunique"),
    domain_switches=("domain_switch", "sum"),
    category_switches=("category_switch", "sum"),
)

# ------------------------------------------------
# Dominant category
# ------------------------------------------------

dominant_category = (
    df.groupby(["session_id", "category"])
    .size()
    .reset_index(name="count")
    .sort_values(["session_id", "count"], ascending=False)
    .drop_duplicates("session_id")
)

dominant_category = dominant_category.set_index("session_id")["category"]

session_stats["dominant_category"] = dominant_category

# ------------------------------------------------
# Session complexity score
# ------------------------------------------------

session_stats["session_complexity"] = (
    session_stats["pages_visited"]
    + session_stats["domain_switches"]
    + session_stats["category_switches"]
)

print("\nSession statistics sample:\n")

print(session_stats.head())

# ------------------------------------------------
# Merge stats back
# ------------------------------------------------

df = df.merge(session_stats, left_on="session_id", right_index=True)

# ------------------------------------------------
# Save dataset
# ------------------------------------------------

df.to_csv(output_file, index=False)

print("\n================================================")
print("SESSION DATASET SAVED")
print("================================================")

print("Output file:")
print(output_file)

print("\nColumns:")
print(df.columns.tolist())

print("\nSample rows:\n")

print(df.head(10))

print("\n================================================")
print("STEP 3 COMPLETED")
print("================================================")