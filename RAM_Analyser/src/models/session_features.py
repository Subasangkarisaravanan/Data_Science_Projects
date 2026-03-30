import pandas as pd
import os
from urllib.parse import urlparse

from src.config.paths import DATA_DIR

print("\n================================================")
print("STEP 5 : SESSION FEATURE ENGINEERING")
print("================================================\n")

# ------------------------------------------------
# PATHS
# ------------------------------------------------
input_file = os.path.join(DATA_DIR, "ram_browsing_merged.csv")
output_file = os.path.join(DATA_DIR, "processed", "session_features.csv")

print("📥 Input file:", input_file)
print("📤 Output file:", output_file)

# ------------------------------------------------
# FILE CHECK
# ------------------------------------------------
if not os.path.exists(input_file):
    print("❌ Input file not found:", input_file)
    exit()

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
df = pd.read_csv(input_file)

if df.empty:
    print("⚠️ No data available")
    exit()

print(f"\n📊 Rows loaded: {len(df)}")
print("\n📋 Available columns:\n", df.columns.tolist())

# ------------------------------------------------
# ✅ FIX 1: ADD DOMAIN COLUMN
# ------------------------------------------------
def extract_domain(url):
    try:
        return urlparse(url).netloc.lower()
    except:
        return ""

df["domain"] = df["url"].apply(extract_domain)

# ------------------------------------------------
# CREATE SESSION IF MISSING
# ------------------------------------------------
if "session_id" not in df.columns:
    print("\n⚠️ session_id not found → Creating sessions...\n")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df.dropna(subset=["timestamp"], inplace=True)

    df = df.sort_values("timestamp").reset_index(drop=True)

    df["time_gap"] = df["timestamp"].diff().dt.total_seconds()

    SESSION_TIMEOUT = 900  # 15 mins

    df["new_session"] = (df["time_gap"] > SESSION_TIMEOUT) | df["time_gap"].isna()
    df["session_id"] = df["new_session"].cumsum()

    # Session duration
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
    # SAFE FEATURE CREATION
    # ------------------------------------------------
    df["pages_visited"] = df.groupby("session_id")["url"].transform("count")
    df["unique_domains"] = df.groupby("session_id")["domain"].transform("nunique")

    df["domain_switches"] = (
        df["domain"] != df["domain"].shift()
    ).astype(int)

    df["category_switches"] = (
        df["category"] != df["category"].shift()
    ).astype(int)

    df["session_complexity"] = (
        df["pages_visited"] +
        df["domain_switches"] +
        df["category_switches"]
    )

# ------------------------------------------------
# AGGREGATION
# ------------------------------------------------
agg_dict = {
    "session_length": ("session_duration", "max"),
    "pages_visited": ("pages_visited", "max"),
    "unique_domains": ("unique_domains", "max"),
    "domain_switches": ("domain_switches", "sum"),
    "category_switches": ("category_switches", "sum"),
    "session_complexity": ("session_complexity", "max"),
    "avg_ram": ("ram_used_mb", "mean"),
    "peak_ram": ("ram_used_mb", "max"),
}

if "cpu_percent" in df.columns:
    agg_dict["avg_cpu"] = ("cpu_percent", "mean")

# ------------------------------------------------
# FEATURE CREATION
# ------------------------------------------------
features = df.groupby("session_id").agg(**agg_dict).reset_index()

# ------------------------------------------------
# DERIVED FEATURES
# ------------------------------------------------
features["ram_per_page"] = features["avg_ram"] / features["pages_visited"].replace(0, 1)
features["ram_per_domain"] = features["avg_ram"] / features["unique_domains"].replace(0, 1)
features["ram_per_switch"] = features["avg_ram"] / (features["domain_switches"] + 1)

features["session_intensity"] = (
    features["pages_visited"] +
    features["domain_switches"] +
    features["category_switches"]
)

features["efficiency_score"] = (
    features["session_complexity"] /
    features["session_length"].replace(0, 1)
)

features["ram_efficiency"] = (
    features["session_complexity"] /
    features["avg_ram"].replace(0, 1)
)

features["high_ram_usage"] = features["avg_ram"] > features["avg_ram"].mean()

# ------------------------------------------------
# SORT
# ------------------------------------------------
features = features.sort_values("avg_ram", ascending=False)

# ------------------------------------------------
# PRINT
# ------------------------------------------------
print("\n📊 FEATURE DATASET SAMPLE:\n")
print(features.head())

print("\n📊 SUMMARY STATS:\n")
print(features.describe())

# ------------------------------------------------
# SAVE
# ------------------------------------------------
os.makedirs(os.path.dirname(output_file), exist_ok=True)
features.to_csv(output_file, index=False)

print("\n================================================")
print("✅ FEATURE DATASET SAVED")
print("================================================")

print("📁 Output file:", output_file)
print(f"📊 Total sessions: {len(features)}")

print("\n================================================")
print("🚀 STEP 5 COMPLETED")
print("================================================")