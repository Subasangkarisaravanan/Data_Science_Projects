import pandas as pd
import os

print("\n================================================")
print("STEP 8.5 : BEHAVIOR INSIGHT ENGINE")
print("================================================\n")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR,"data")

sessions_file = os.path.join(DATA_DIR,"browsing_sessions.csv")
features_file = os.path.join(DATA_DIR,"session_features.csv")
anomaly_file = os.path.join(DATA_DIR,"session_anomalies.csv")

sessions = pd.read_csv(sessions_file)
features = pd.read_csv(features_file)
anomalies = pd.read_csv(anomaly_file)

print("Sessions loaded:",len(sessions))

insights = []

# ------------------------------------------------
# PEAK HOUR
# ------------------------------------------------

peak_hour = sessions["hour"].mode()[0]

insights.append(f"Peak browsing hour is around {peak_hour}:00.")

# ------------------------------------------------
# TOP CATEGORY
# ------------------------------------------------

top_category = sessions["category"].value_counts().idxmax()

insights.append(f"Most visited category is {top_category}.")

# ------------------------------------------------
# LEARNING RATIO
# ------------------------------------------------

learning_ratio = (sessions["category"]=="learning").mean()*100

insights.append(f"Learning related browsing is {learning_ratio:.1f}% of activity.")

# ------------------------------------------------
# LONG SESSIONS
# ------------------------------------------------

long_sessions = (features["session_length"]>3600).sum()

insights.append(f"{long_sessions} sessions longer than 1 hour detected.")

# ------------------------------------------------
# ANOMALIES
# ------------------------------------------------

anomaly_count = anomalies["is_anomaly"].sum()

insights.append(f"{anomaly_count} anomalous browsing sessions detected.")

# ------------------------------------------------
# PRINT INSIGHTS
# ------------------------------------------------

print("\nGenerated Insights:\n")

for i in insights:
    print("•",i)

# ------------------------------------------------
# SAVE INSIGHTS
# ------------------------------------------------

output_file = os.path.join(DATA_DIR,"behavior_insights.txt")

with open(output_file,"w") as f:
    for i in insights:
        f.write(i+"\n")

print("\nInsights saved:")
print(output_file)

print("\n================================================")
print("STEP 8.5 COMPLETED")
print("================================================")