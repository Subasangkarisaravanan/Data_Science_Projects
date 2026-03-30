import pandas as pd
import os
from urllib.parse import urlparse

from src.config.paths import CLEAN_HISTORY, SESSION_HISTORY

print("\n================================================")
print("STEP 3 : SESSION BUILDING")
print("================================================\n")

# ------------------------------------------------
# Paths
# ------------------------------------------------
input_file = CLEAN_HISTORY
output_file = SESSION_HISTORY

print("Input file:", input_file)
print("Output file:", output_file)

# ------------------------------------------------
# File Check
# ------------------------------------------------
if not os.path.exists(input_file):
    print("❌ Input file not found:", input_file)
    exit()

# ------------------------------------------------
# Load dataset
# ------------------------------------------------
df = pd.read_csv(input_file)

if df.empty:
    print("⚠️ No data available in input file")
    exit()

print(f"\n📊 Rows loaded: {len(df)}")

# ------------------------------------------------
# ✅ FIX 1: ADD DOMAIN COLUMN (CRITICAL)
# ------------------------------------------------
def extract_domain(url):
    try:
        return urlparse(url).netloc.lower()
    except:
        return ""

df["domain"] = df["url"].apply(extract_domain)

# ------------------------------------------------
# Convert timestamp
# ------------------------------------------------
if "timestamp" not in df.columns:
    print("❌ 'timestamp' column missing")
    exit()

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df.dropna(subset=["timestamp"], inplace=True)

# ------------------------------------------------
# Sort by time
# ------------------------------------------------
df = df.sort_values("timestamp").reset_index(drop=True)

# ------------------------------------------------
# Time gap calculation
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
# Category switching (SAFE)
# ------------------------------------------------
if "category" in df.columns:
    df["prev_category"] = df["category"].shift()
    df["category_switch"] = df["category"] != df["prev_category"]
    df.loc[df["new_session"], "category_switch"] = False
else:
    df["category_switch"] = False

# ------------------------------------------------
# Session duration
# ------------------------------------------------
session_times = df.groupby("session_id")["timestamp"].agg(["min", "max"])

session_times["session_duration"] = (
    session_times["max"] - session_times["min"]
).dt.total_seconds().clip(lower=1)

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
# Dominant category (SAFE)
# ------------------------------------------------
if "category" in df.columns:
    dominant_category = (
        df.groupby(["session_id", "category"])
        .size()
        .reset_index(name="count")
        .sort_values(["session_id", "count"], ascending=[True, False])
        .drop_duplicates("session_id")
    )

    dominant_category = dominant_category.set_index("session_id")["category"]
    session_stats["dominant_category"] = dominant_category
else:
    session_stats["dominant_category"] = "Unknown"

# ------------------------------------------------
# Session complexity
# ------------------------------------------------
session_stats["session_complexity"] = (
    session_stats["pages_visited"]
    + session_stats["domain_switches"] * 2
    + session_stats["category_switches"] * 2
)

# ------------------------------------------------
# Engagement level
# ------------------------------------------------
def get_engagement(score):
    if score < 5:
        return "low"
    elif score < 15:
        return "medium"
    else:
        return "high"

session_stats["engagement_level"] = session_stats["session_complexity"].apply(get_engagement)

# ------------------------------------------------
# Start hour
# ------------------------------------------------
session_start = df.groupby("session_id")["timestamp"].min()
session_stats["start_hour"] = session_start.dt.hour

# ------------------------------------------------
# Merge stats back
# ------------------------------------------------
df = df.merge(session_stats, left_on="session_id", right_index=True)

# ------------------------------------------------
# Ensure output folder exists
# ------------------------------------------------
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# ------------------------------------------------
# Save dataset
# ------------------------------------------------
df.to_csv(output_file, index=False)

# ------------------------------------------------
# Logs
# ------------------------------------------------
print("\n================================================")
print("✅ SESSION DATASET SAVED")
print("================================================")

print("📁 Output file:", output_file)
print(f"📊 Final rows: {len(df)}")

print("\n📊 Session statistics sample:\n")
print(session_stats.head())

print("\n================================================")
print("🚀 STEP 3 COMPLETED")
print("================================================")