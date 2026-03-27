import pandas as pd
import os

print("\n================================================")
print("STEP 8 : ADVANCED INTELLIGENT RECOMMENDATIONS")
print("================================================\n")

# ------------------------------------------------
# PATHS
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

features_file = os.path.join(DATA_DIR, "session_features.csv")
sessions_file = os.path.join(DATA_DIR, "browsing_sessions.csv")
anomaly_file = os.path.join(DATA_DIR, "session_anomalies.csv")
output_file = os.path.join(DATA_DIR, "recommendations.txt")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

features = pd.read_csv(features_file)
sessions = pd.read_csv(sessions_file)
anomalies = pd.read_csv(anomaly_file)

recommendations = []

# ------------------------------------------------
# 1. ANOMALY ANALYSIS
# ------------------------------------------------

anomaly_count = anomalies["is_anomaly"].sum()
recommendations.append(f"{anomaly_count} anomalous sessions detected. Review unusual browsing behavior.")

# ------------------------------------------------
# 2. LONG SESSIONS
# ------------------------------------------------

long_sessions = (features["session_length"] > 3600).sum()
recommendations.append(f"{long_sessions} sessions exceed 1 hour. Consider taking regular breaks.")

# ------------------------------------------------
# 3. SWITCHING BEHAVIOR
# ------------------------------------------------

high_switch = (features["domain_switches"] > 10).sum()
recommendations.append(f"{high_switch} sessions show high tab switching. This may indicate distraction.")

# ------------------------------------------------
# 4. LEARNING ACTIVITY
# ------------------------------------------------

learning_ratio = (sessions["category"] == "learning").mean()
recommendations.append(f"Learning activity is {learning_ratio*100:.1f}% of total browsing.")

if learning_ratio < 0.2:
    recommendations.append("Learning usage is relatively low. Consider increasing educational content consumption.")

# ------------------------------------------------
# 5. LATE NIGHT USAGE
# ------------------------------------------------

late_night = (sessions["hour"] >= 23).sum()
recommendations.append(f"{late_night} late-night browsing activities detected.")

if late_night > 20:
    recommendations.append("Frequent late-night browsing may affect sleep quality.")

# ------------------------------------------------
# 6. PEAK HOUR
# ------------------------------------------------

peak_hour = sessions["hour"].value_counts().idxmax()
recommendations.append(f"Your peak browsing hour is {peak_hour}:00. Use this time for focused work.")

# ------------------------------------------------
# 7. RAM USAGE
# ------------------------------------------------

avg_ram = features["avg_ram"].mean()
recommendations.append(f"Average RAM usage per session is {avg_ram:.0f} MB.")

# ------------------------------------------------
# 8. SHORT SESSIONS
# ------------------------------------------------

short_sessions = (features["session_length"] < 60).sum()
recommendations.append(f"{short_sessions} very short sessions detected, indicating possible distractions.")

# ------------------------------------------------
# 9. HIGH INTENSITY
# ------------------------------------------------

high_intensity = (features["session_intensity"] > features["session_intensity"].mean()).sum()
recommendations.append(f"{high_intensity} high intensity sessions detected.")

# ------------------------------------------------
# 10. TOP WEBSITES
# ------------------------------------------------

top_sites = sessions["domain"].value_counts().head(5)
recommendations.append("Most visited websites: " + ", ".join(top_sites.index))

# ------------------------------------------------
# 11. CATEGORY DOMINANCE
# ------------------------------------------------

top_category = sessions["category"].value_counts().idxmax()
recommendations.append(f"Most frequently used category is '{top_category}'.")

# ------------------------------------------------
# 12. SOCIAL LOOP
# ------------------------------------------------

social_file = os.path.join(DATA_DIR, "social_loops.csv")

if os.path.exists(social_file):
    social = pd.read_csv(social_file)
    if len(social) > 0:
        recommendations.append(f"{len(social)} social loop sessions detected. Consider reducing social media usage.")

# ------------------------------------------------
# 13. HIGH RAM SITES
# ------------------------------------------------

ram_file = os.path.join(DATA_DIR, "high_ram_sites.csv")

if os.path.exists(ram_file):
    ram_df = pd.read_csv(ram_file)
    top_ram_sites = ram_df.iloc[:, 0].head(3).tolist()
    recommendations.append("High RAM consuming sites include: " + ", ".join(top_ram_sites))

# ------------------------------------------------
# 14. SLOW SITES
# ------------------------------------------------

slow_file = os.path.join(DATA_DIR, "slow_sites.csv")

if os.path.exists(slow_file):
    slow_df = pd.read_csv(slow_file)
    slow_sites = slow_df.iloc[:, 0].head(3).tolist()
    recommendations.append("Potential slow or heavy sites: " + ", ".join(slow_sites))

# ------------------------------------------------
# 15. GENERAL PRODUCTIVITY
# ------------------------------------------------

recommendations.append("Consider organizing browsing sessions into focused time blocks for better productivity.")

# ------------------------------------------------
# SAVE (UTF-8 FIX 🔥)
# ------------------------------------------------

with open(output_file, "w", encoding="utf-8") as f:
    for i, rec in enumerate(recommendations, 1):
        f.write(f"{i}. {rec}\n")

# ------------------------------------------------
# PRINT OUTPUT
# ------------------------------------------------

print("\nGenerated Recommendations:\n")

for r in recommendations:
    print("-", r)

print("\n================================================")
print("RECOMMENDATIONS SAVED SUCCESSFULLY")
print("================================================")
print("Output file:", output_file)