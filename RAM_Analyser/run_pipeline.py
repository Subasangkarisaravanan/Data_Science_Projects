import subprocess
import sys
import os

print("\n================================================")
print("RAM ANALYSER PIPELINE EXECUTION")
print("================================================\n")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------
# FUNCTION TO RUN EACH STEP
# ------------------------------------------------

def run_step(step_name, script_path):

    full_path = os.path.join(BASE_DIR, script_path)

    print("\n------------------------------------------------")
    print(step_name)
    print("Running:", full_path)
    print("------------------------------------------------\n")

    try:

        subprocess.run(
            [sys.executable, full_path],
            check=True
        )

    except subprocess.CalledProcessError as e:

        print("\nERROR OCCURRED IN:", step_name)
        print(e)

        sys.exit(1)


# ------------------------------------------------
# STEP 0 : HISTORY EXTRACTION
# ------------------------------------------------

run_step(
    "STEP 0 : Browser History Extraction",
    "src/collect/history_extractor.py"
)


# ------------------------------------------------
# STEP 1 : RAM LOGGER
# ------------------------------------------------

run_step(
    "STEP 1 : RAM Logger",
    "src/collect/ram_logger.py"
)


# ------------------------------------------------
# STEP 1.5 : ACTIVE TAB TRACKER
# ------------------------------------------------

run_step(
    "STEP 1.5 : Active Tab Tracker",
    "src/collect/active_tab_tracker.py"
)


# ------------------------------------------------
# STEP 2 : DATA CLEANING
# ------------------------------------------------

run_step(
    "STEP 2 : Data Cleaning",
    "src/prep/clean_history.py"
)


# ------------------------------------------------
# STEP 3 : SESSION BUILDING
# ------------------------------------------------

run_step(
    "STEP 3 : Session Building",
    "src/prep/session_builder.py"
)


# ------------------------------------------------
# STEP 4 : RAM CORRELATION ANALYSIS
# ------------------------------------------------

run_step(
    "STEP 4 : RAM Correlation Analysis",
    "src/analytics/ram_correlation.py"
)


# ------------------------------------------------
# STEP 5 : SESSION FEATURE ENGINEERING
# ------------------------------------------------

run_step(
    "STEP 5 : Session Feature Engineering",
    "src/models/session_features.py"
)


# ------------------------------------------------
# STEP 6 : SESSION CLUSTERING
# ------------------------------------------------

run_step(
    "STEP 6 : Session Clustering",
    "src/models/session_clustering.py"
)


# ------------------------------------------------
# STEP 7 : AUTOENCODER ANOMALY DETECTION
# ------------------------------------------------

run_step(
    "STEP 7 : Autoencoder Anomaly Detection",
    "src/models/autoencoder_model.py"
)


# ------------------------------------------------
# STEP 8 : RECOMMENDATION ENGINE
# ------------------------------------------------

run_step(
    "STEP 8 : Recommendation Engine",
    "src/analytics/recommendation_engine.py"
)


# ------------------------------------------------
# STEP 8.5 : BEHAVIOR INSIGHT ENGINE
# ------------------------------------------------

run_step(
    "STEP 8.5 : Behavior Insights",
    "src/analytics/behavior_insights.py"
)


# ------------------------------------------------
# STEP 9 : FINAL REPORT GENERATION
# ------------------------------------------------

run_step(
    "STEP 9 : Final Report Generator",
    "src/analytics/report_generator.py"
)


print("\n================================================")
print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
print("================================================\n")