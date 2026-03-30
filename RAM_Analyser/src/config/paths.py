import os

# =========================================================
# BASE DIRECTORY
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# =========================================================
# MAIN FOLDERS
# =========================================================
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
PLOTS_DIR = os.path.join(PROCESSED_DIR, "plots")
REPORTS_DIR = BASE_DIR  # keeping report in root (you can change if needed)

# ---------------------------------------------------------
# CREATE FOLDERS (SAFE)
# ---------------------------------------------------------
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# =========================================================
# RAW FILES
# =========================================================
RAW_HISTORY = os.path.join(DATA_DIR, "browsing_history_raw.csv")
RAM_LOG = os.path.join(DATA_DIR, "ram_log.csv")

# =========================================================
# PROCESSED FILES
# =========================================================
CLEAN_HISTORY = os.path.join(PROCESSED_DIR, "cleaned_history.csv")
MERGED_DATA = os.path.join(DATA_DIR, "ram_browsing_merged.csv")
SESSION_HISTORY = os.path.join(PROCESSED_DIR, "browsing_sessions.csv")
SESSION_FEATURES = os.path.join(PROCESSED_DIR, "session_features.csv")

# =========================================================
# ANALYTICS OUTPUTS
# =========================================================
SOCIAL_LOOPS = os.path.join(PROCESSED_DIR, "social_loops.csv")
INSIGHTS_FILE = os.path.join(PROCESSED_DIR, "behavior_insights.txt")

# =========================================================
# REPORT
# =========================================================
REPORT_FILE = os.path.join(REPORTS_DIR, "RAM_Analysis_Report.pdf")