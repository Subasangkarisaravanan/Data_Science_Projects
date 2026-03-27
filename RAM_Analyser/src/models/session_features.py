import pandas as pd
import os

print("\n================================================")
print("STEP 5 : SESSION FEATURE ENGINEERING (FIXED)")
print("================================================\n")

# ------------------------------------------------
# PATHS
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

input_file = os.path.join(DATA_DIR, "ram_browsing_merged.csv")
output_file = os.path.join(DATA_DIR, "session_features.csv")

print("Input file:")
print(input_file)

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

df = pd.read_csv(input_file)

print("\nRows loaded:", len(df))

# ------------------------------------------------
# CHECK AVAILABLE COLUMNS
# ------------------------------------------------

print("\nAvailable columns:", df.columns.tolist())

# ------------------------------------------------
# SAFE AGGREGATION (IMPORTANT FIX 🔥)
# ------------------------------------------------

agg_dict = {
    "session_length": ("session_duration", "max"),
    "pages_visited": ("pages_visited", "max"),
    "unique_domains": ("unique_domains", "max"),
    "domain_switches": ("domain_switches", "max"),
    "category_switches": ("category_switches", "max"),
    "session_complexity": ("session_complexity", "max"),
    "avg_ram": ("ram_used_mb", "mean"),
    "peak_ram": ("ram_used_mb", "max"),
}

# Add CPU only if exists
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

# ------------------------------------------------
# OUTPUT
# ------------------------------------------------

print("\nFeature dataset created\n")
print(features.head())

features.to_csv(output_file, index=False)

print("\n================================================")
print("FEATURE DATASET SAVED")
print("================================================")

print("Output file:", output_file)
print("Total sessions:", len(features))

print("\n================================================")
print("STEP 5 COMPLETED (FIXED)")
print("================================================")