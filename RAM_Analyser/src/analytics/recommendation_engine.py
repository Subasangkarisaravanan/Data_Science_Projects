import pandas as pd
import os

from src.config.paths import DATA_DIR, SESSION_HISTORY

print("\n================================================")
print("STEP 8 : ADVANCED INTELLIGENT RECOMMENDATIONS")
print("================================================\n")

# ------------------------------------------------
# PATHS (FIXED)
# ------------------------------------------------

features_file = os.path.join(DATA_DIR, "processed", "session_features.csv")
sessions_file = SESSION_HISTORY
anomaly_file = os.path.join(DATA_DIR, "processed", "session_anomalies.csv")
output_file = os.path.join(DATA_DIR, "processed", "recommendations.txt")

print("📥 Loading files...")

# ------------------------------------------------
# LOAD DATA (SAFE)
# ------------------------------------------------

def safe_read(path, name):
    if not os.path.exists(path):
        print(f"⚠️ {name} not found:", path)
        return pd.DataFrame()
    df = pd.read_csv(path)
    print(f"✅ {name} loaded:", len(df))
    return df

features = safe_read(features_file, "Features")
sessions = safe_read(sessions_file, "Sessions")
anomalies = safe_read(anomaly_file, "Anomalies")

recommendations = []

# ------------------------------------------------
# FIX CATEGORY COLUMN
# ------------------------------------------------

if "category" not in sessions.columns and "dominant_category" in sessions.columns:
    sessions["category"] = sessions["dominant_category"]

if "category" in sessions.columns:
    sessions["category"] = sessions["category"].astype(str).str.lower()

# ------------------------------------------------
# 1. ANOMALY ANALYSIS
# ------------------------------------------------

if "is_anomaly" in anomalies.columns:
    anomaly_count = anomalies["is_anomaly"].sum()
    recommendations.append(f"{anomaly_count} anomalous sessions detected.")

    if anomaly_count > 10:
        recommendations.append("High anomaly count → Review unusual or inefficient browsing behavior.")

# ------------------------------------------------
# 2. LONG SESSIONS
# ------------------------------------------------

if "session_length" in features.columns:
    long_sessions = (features["session_length"] > 3600).sum()
    recommendations.append(f"{long_sessions} sessions exceed 1 hour.")

    if long_sessions > 5:
        recommendations.append("Take regular breaks to improve productivity and reduce fatigue.")

# ------------------------------------------------
# 3. SWITCHING BEHAVIOR
# ------------------------------------------------

if "domain_switches" in features.columns:
    high_switch = (features["domain_switches"] > 10).sum()
    recommendations.append(f"{high_switch} sessions show high tab switching.")

    if high_switch > 10:
        recommendations.append("High switching may indicate distraction. Try focused browsing sessions.")

# ------------------------------------------------
# 4. LEARNING ACTIVITY
# ------------------------------------------------

if "category" in sessions.columns:
    learning_ratio = (sessions["category"] == "learning").mean()
    recommendations.append(f"Learning activity: {learning_ratio*100:.1f}%")

    if learning_ratio < 0.2:
        recommendations.append("Increase learning-related browsing for skill development.")

# ------------------------------------------------
# 5. LATE NIGHT USAGE
# ------------------------------------------------

if "hour" in sessions.columns:
    late_night = (sessions["hour"] >= 23).sum()
    recommendations.append(f"{late_night} late-night sessions detected.")

    if late_night > 20:
        recommendations.append("Reduce late-night browsing to improve sleep quality.")

# ------------------------------------------------
# 6. PEAK HOUR
# ------------------------------------------------

if "hour" in sessions.columns and not sessions.empty:
    peak_hour = sessions["hour"].value_counts().idxmax()
    recommendations.append(f"Peak browsing hour: {peak_hour}:00 → Use for focused work.")

# ------------------------------------------------
# 7. RAM USAGE
# ------------------------------------------------

if "avg_ram" in features.columns:
    avg_ram = features["avg_ram"].mean()
    recommendations.append(f"Average RAM usage: {avg_ram:.0f} MB")

    if avg_ram > 2000:
        recommendations.append("High RAM usage detected. Consider closing unused tabs.")

# ------------------------------------------------
# 8. SHORT SESSIONS
# ------------------------------------------------

if "session_length" in features.columns:
    short_sessions = (features["session_length"] < 60).sum()
    recommendations.append(f"{short_sessions} short sessions detected.")

# ------------------------------------------------
# 9. HIGH INTENSITY
# ------------------------------------------------

if "session_intensity" in features.columns:
    high_intensity = (features["session_intensity"] > features["session_intensity"].mean()).sum()
    recommendations.append(f"{high_intensity} high-intensity sessions detected.")

# ------------------------------------------------
# 10. TOP WEBSITES
# ------------------------------------------------

if "domain" in sessions.columns:
    top_sites = sessions["domain"].value_counts().head(5)
    recommendations.append("Top sites: " + ", ".join(top_sites.index))

# ------------------------------------------------
# 11. CATEGORY DOMINANCE
# ------------------------------------------------

if "category" in sessions.columns:
    top_category = sessions["category"].value_counts().idxmax()
    recommendations.append(f"Dominant category: {top_category}")

# ------------------------------------------------
# 12. SOCIAL LOOP
# ------------------------------------------------

social_file = os.path.join(DATA_DIR, "processed", "social_loops.csv")

if os.path.exists(social_file):
    social = pd.read_csv(social_file)
    if not social.empty:
        recommendations.append(f"{len(social)} social loop sessions detected.")
        recommendations.append("Reduce excessive social media usage.")

# ------------------------------------------------
# FINAL GENERAL ADVICE
# ------------------------------------------------

recommendations.append("Organize browsing into focused sessions for better productivity.")

# ------------------------------------------------
# SAVE
# ------------------------------------------------

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    for i, rec in enumerate(recommendations, 1):
        f.write(f"{i}. {rec}\n")

# ------------------------------------------------
# PRINT OUTPUT
# ------------------------------------------------

print("\n📊 GENERATED RECOMMENDATIONS:\n")

for i, r in enumerate(recommendations, 1):
    print(f"{i}. {r}")

print("\n================================================")
print("✅ RECOMMENDATIONS SAVED")
print("================================================")

print("📁 Output file:", output_file)