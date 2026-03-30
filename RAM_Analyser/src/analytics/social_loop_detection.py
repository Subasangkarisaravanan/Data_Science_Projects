import pandas as pd
import os

from src.config.paths import SESSION_HISTORY, DATA_DIR

print("\n================================================")
print("STEP X : SOCIAL LOOP DETECTION")
print("================================================\n")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
if not os.path.exists(SESSION_HISTORY):
    print("❌ File not found:", SESSION_HISTORY)
    exit()

df = pd.read_csv(SESSION_HISTORY)

if df.empty:
    print("⚠️ No data available")
    exit()

print(f"📊 Rows loaded: {len(df)}")

# ------------------------------------------------
# PREPROCESS
# ------------------------------------------------

# Normalize category
if "category" not in df.columns:
    print("❌ 'category' column missing")
    exit()

df["category"] = df["category"].astype(str).str.lower()

# ------------------------------------------------
# ✅ FIX 1: CREATE HOUR COLUMN
# ------------------------------------------------
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df.dropna(subset=["timestamp"], inplace=True)
    df["hour"] = df["timestamp"].dt.hour
else:
    print("❌ 'timestamp' column missing → cannot create hour")
    exit()

# ------------------------------------------------
# REQUIRED COLUMNS CHECK
# ------------------------------------------------
required_cols = ["session_id", "url", "pages_visited", "hour", "category"]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    print("❌ Missing columns:", missing)
    exit()

# ------------------------------------------------
# FILTER SOCIAL + ENTERTAINMENT
# ------------------------------------------------
social = df[df["category"].isin(["social media", "entertainment"])].copy()

print(f"\n📊 Social/Entertainment rows: {len(social)}")

if social.empty:
    print("⚠️ No social/entertainment data found")
    exit()

# ------------------------------------------------
# SESSION LEVEL AGGREGATION
# ------------------------------------------------
group = social.groupby("session_id").agg(
    social_pages=("url", "count"),
    total_pages=("pages_visited", "max"),
    hour=("hour", "first")
).reset_index()

# ------------------------------------------------
# SAFE CALCULATIONS
# ------------------------------------------------
group["total_pages"] = group["total_pages"].replace(0, 1)

group["ratio"] = group["social_pages"] / group["total_pages"]

# ------------------------------------------------
# DETECT LOOPS (IMPROVED LOGIC)
# ------------------------------------------------
loops = group[
    (group["ratio"] > 0.6) &   # heavy usage
    (group["hour"] >= 22)      # late night
].copy()

# ------------------------------------------------
# ADD FLAGS (SAFE)
# ------------------------------------------------
loops["is_extreme"] = loops["ratio"] > 0.8

# ------------------------------------------------
# OPTIONAL: ADD RISK SCORE (🔥 ADVANCED)
# ------------------------------------------------
loops["risk_score"] = (
    loops["ratio"] * 0.7 +
    (loops["hour"] / 24) * 0.3
) * 100

# ------------------------------------------------
# PRINT OUTPUT
# ------------------------------------------------
print("\n🔥 SOCIAL LOOP SUMMARY:\n")
print(loops.head())

print("\n📊 Total social loops detected:", len(loops))
print("📊 Extreme loops (>80%):", loops["is_extreme"].sum())

# ------------------------------------------------
# SAVE OUTPUT
# ------------------------------------------------
output_file = os.path.join(DATA_DIR, "processed", "social_loops.csv")

os.makedirs(os.path.dirname(output_file), exist_ok=True)

loops.to_csv(output_file, index=False)

print("\n================================================")
print("✅ SOCIAL LOOP DATA SAVED")
print("================================================")

print("📁 Output file:", output_file)

print("\n================================================")
print("🚀 STEP COMPLETED")
print("================================================")