import pandas as pd
import os

from src.config.paths import SESSION_HISTORY, DATA_DIR

print("\n================================================")
print("STEP 8.5 : BEHAVIOR INSIGHT ENGINE")
print("================================================\n")

# ------------------------------------------------
# PATHS (FIXED)
# ------------------------------------------------

sessions_file = SESSION_HISTORY
features_file = os.path.join(DATA_DIR, "processed", "session_features.csv")
anomaly_file = os.path.join(DATA_DIR, "processed", "session_anomalies.csv")

output_file = os.path.join(DATA_DIR, "processed", "behavior_insights.txt")

# ------------------------------------------------
# SAFE LOAD FUNCTION
# ------------------------------------------------

def safe_load(path, name):
    if not os.path.exists(path):
        print(f"⚠️ {name} not found:", path)
        return pd.DataFrame()
    df = pd.read_csv(path)
    print(f"✅ {name} loaded:", len(df))
    return df

sessions = safe_load(sessions_file, "Sessions")
features = safe_load(features_file, "Features")
anomalies = safe_load(anomaly_file, "Anomalies")

insights = []

# ------------------------------------------------
# FIX CATEGORY
# ------------------------------------------------

if "category" not in sessions.columns and "dominant_category" in sessions.columns:
    sessions["category"] = sessions["dominant_category"]

if "category" in sessions.columns:
    sessions["category"] = sessions["category"].astype(str).str.lower()

# ------------------------------------------------
# PEAK HOUR
# ------------------------------------------------

if "hour" in sessions.columns and not sessions.empty:
    peak_hour = sessions["hour"].mode()[0]
    insights.append(f"🕒 Peak browsing hour is around {peak_hour}:00.")

# ------------------------------------------------
# TOP CATEGORY
# ------------------------------------------------

if "category" in sessions.columns and not sessions.empty:
    top_category = sessions["category"].value_counts().idxmax()
    insights.append(f"📊 Most visited category is '{top_category}'.")

# ------------------------------------------------
# LEARNING RATIO
# ------------------------------------------------

if "category" in sessions.columns:
    learning_ratio = (sessions["category"] == "learning").mean() * 100
    insights.append(f"📚 Learning activity: {learning_ratio:.1f}%.")

    if learning_ratio < 20:
        insights.append("⚠️ Learning usage is low — consider increasing educational content.")

# ------------------------------------------------
# LONG SESSIONS
# ------------------------------------------------

if "session_length" in features.columns:
    long_sessions = (features["session_length"] > 3600).sum()
    insights.append(f"⏳ {long_sessions} sessions longer than 1 hour detected.")

    if long_sessions > 5:
        insights.append("⚠️ Frequent long sessions — consider taking breaks.")

# ------------------------------------------------
# SHORT SESSIONS
# ------------------------------------------------

if "session_length" in features.columns:
    short_sessions = (features["session_length"] < 60).sum()
    insights.append(f"⚡ {short_sessions} very short sessions detected.")

# ------------------------------------------------
# ANOMALIES
# ------------------------------------------------

if "is_anomaly" in anomalies.columns:
    anomaly_count = anomalies["is_anomaly"].sum()
    insights.append(f"🚨 {anomaly_count} anomalous sessions detected.")

    if anomaly_count > 10:
        insights.append("⚠️ High anomaly rate — unusual browsing behavior detected.")

# ------------------------------------------------
# RAM INSIGHT
# ------------------------------------------------

if "avg_ram" in features.columns:
    avg_ram = features["avg_ram"].mean()
    insights.append(f"💻 Average RAM usage per session: {avg_ram:.0f} MB.")

# ------------------------------------------------
# INTENSITY INSIGHT
# ------------------------------------------------

if "session_intensity" in features.columns:
    high_intensity = (features["session_intensity"] > features["session_intensity"].mean()).sum()
    insights.append(f"🔥 {high_intensity} high-intensity sessions detected.")

# ------------------------------------------------
# FINAL PRODUCTIVITY INSIGHT
# ------------------------------------------------

insights.append("💡 Organizing browsing into focused time blocks can improve productivity.")

# ------------------------------------------------
# PRINT OUTPUT
# ------------------------------------------------

print("\n📊 GENERATED INSIGHTS:\n")

for ins in insights:
    print("•", ins)

# ------------------------------------------------
# SAVE OUTPUT
# ------------------------------------------------

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    for ins in insights:
        f.write(ins + "\n")

print("\n================================================")
print("✅ INSIGHTS SAVED")
print("================================================")

print("📁 Output file:", output_file)