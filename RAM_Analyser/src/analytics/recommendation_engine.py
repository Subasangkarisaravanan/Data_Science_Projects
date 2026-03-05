import pandas as pd
import os

print("\n================================================")
print("STEP 8 : RECOMMENDATION ENGINE")
print("================================================\n")

# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

features_file = os.path.join(DATA_DIR, "session_features.csv")
anomaly_file = os.path.join(DATA_DIR, "session_anomalies.csv")
sessions_file = os.path.join(DATA_DIR, "browsing_sessions.csv")

output_file = os.path.join(DATA_DIR, "recommendations.txt")

print("Features file:")
print(features_file)

print("\nAnomaly file:")
print(anomaly_file)

# ------------------------------------------------
# Load datasets
# ------------------------------------------------

features = pd.read_csv(features_file)
anomalies = pd.read_csv(anomaly_file)
sessions = pd.read_csv(sessions_file)

print("\nSessions analyzed:", len(features))

recommendations = []

# ------------------------------------------------
# 1️⃣ Anomaly based recommendation
# ------------------------------------------------

anomaly_count = anomalies["is_anomaly"].sum()

if anomaly_count > 0:
    recommendations.append(
        f"{anomaly_count} unusual browsing sessions detected. Review abnormal activity or long browsing sessions."
    )

# ------------------------------------------------
# 2️⃣ High RAM usage
# ------------------------------------------------

avg_ram = features["avg_ram"].mean()

if avg_ram > 7000:
    recommendations.append(
        "High RAM usage detected during browsing sessions. Consider reducing open tabs or disabling heavy browser extensions."
    )

# ------------------------------------------------
# 3️⃣ Long browsing sessions
# ------------------------------------------------

long_sessions = features[features["session_length"] > 3600]

if len(long_sessions) > 0:
    recommendations.append(
        "Several browsing sessions exceed 1 hour. Consider taking breaks to improve productivity and reduce fatigue."
    )

# ------------------------------------------------
# 4️⃣ High tab switching
# ------------------------------------------------

high_switch = features[features["domain_switches"] > 10]

if len(high_switch) > 0:
    recommendations.append(
        "Frequent switching between websites detected. This may indicate multitasking or distraction."
    )

# ------------------------------------------------
# 5️⃣ Late night browsing
# ------------------------------------------------

late_night = sessions[sessions["hour"] >= 23]

if len(late_night) > 0:
    recommendations.append(
        "Late-night browsing activity detected. Reducing screen time before sleep can improve digital wellbeing."
    )

# ------------------------------------------------
# 6️⃣ Productivity window suggestion
# ------------------------------------------------

hour_counts = sessions["hour"].value_counts()

peak_hour = hour_counts.idxmax()

recommendations.append(
    f"Your most active browsing hour is around {peak_hour}:00. Consider scheduling focused work sessions during this time."
)

# ------------------------------------------------
# 7️⃣ Learning vs distraction balance
# ------------------------------------------------

category_counts = sessions["category"].value_counts()

if "learning" in category_counts:

    learning_ratio = category_counts["learning"] / len(sessions)

    if learning_ratio < 0.3:
        recommendations.append(
            "Learning activity appears relatively low. Consider allocating more time for educational browsing."
        )

# ------------------------------------------------
# 8️⃣ RAM efficiency recommendation
# ------------------------------------------------

ram_per_page = features["ram_per_page"].mean()

if ram_per_page > 1000:
    recommendations.append(
        "High RAM usage per page detected. Websites with heavy media or scripts may be affecting performance."
    )

# ------------------------------------------------
# Print recommendations
# ------------------------------------------------

print("\nGenerated Recommendations:\n")

for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

# ------------------------------------------------
# Save recommendations
# ------------------------------------------------

with open(output_file, "w") as f:
    for i, rec in enumerate(recommendations, 1):
        f.write(f"{i}. {rec}\n")

print("\n================================================")
print("RECOMMENDATIONS SAVED")
print("================================================")

print("Output file:")
print(output_file)

print("\n================================================")
print("STEP 8 COMPLETED")
print("================================================")