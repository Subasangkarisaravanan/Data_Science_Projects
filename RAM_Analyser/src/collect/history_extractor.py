import sqlite3
import pandas as pd
import os
import shutil
from datetime import datetime, timedelta
import getpass

print("\n================================================")
print("STEP 0 : BROWSER HISTORY EXTRACTION")
print("================================================\n")

# -------------------------------------------------
# Project paths
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(DATA_DIR, "browsing_history_raw.csv")

print("Project base directory:")
print(BASE_DIR)

print("\nData folder:")
print(DATA_DIR)

# -------------------------------------------------
# Timestamp conversion
# -------------------------------------------------

def convert_chrome_time(chrome_time):

    if chrome_time == 0:
        return None

    epoch_start = datetime(1601, 1, 1)

    return epoch_start + timedelta(microseconds=chrome_time)

# -------------------------------------------------
# Locate browser profiles
# -------------------------------------------------

username = getpass.getuser()

chrome_base = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data"
edge_base = f"C:/Users/{username}/AppData/Local/Microsoft/Edge/User Data"

print("\nDetected user:", username)

print("\nChecking browser locations...")

print("Chrome path:", chrome_base)
print("Edge path:", edge_base)

browsers = {
    "chrome": chrome_base,
    "edge": edge_base
}

records = []

# -------------------------------------------------
# Scan browser profiles
# -------------------------------------------------

for browser, base_path in browsers.items():

    print("\n------------------------------------------------")
    print(f"Scanning {browser} profiles")
    print("------------------------------------------------")

    if not os.path.exists(base_path):

        print("Browser not found:", browser)
        continue

    profiles = os.listdir(base_path)

    print("Profiles detected:", profiles)

    for profile in profiles:

        history_path = os.path.join(base_path, profile, "History")

        if not os.path.exists(history_path):
            continue

        print("\nReading profile:", profile)

        temp_db = os.path.join(DATA_DIR, f"{browser}_{profile}_temp.db")

        try:

            shutil.copy2(history_path, temp_db)

            conn = sqlite3.connect(temp_db)

            query = """
            SELECT
                urls.url,
                urls.title,
                urls.last_visit_time
            FROM urls
            """

            df = pd.read_sql_query(query, conn)

            conn.close()

            os.remove(temp_db)

            print("Rows extracted:", len(df))

            # Convert timestamp

            df["timestamp"] = df["last_visit_time"].apply(convert_chrome_time)

            df["browser"] = browser
            df["profile"] = profile

            df = df[["timestamp","url","title","browser","profile"]]

            records.append(df)

        except Exception as e:

            print("Error reading profile:", profile)
            print(e)

# -------------------------------------------------
# Combine results
# -------------------------------------------------

print("\n================================================")
print("COMBINING BROWSER HISTORY")
print("================================================")

if len(records) == 0:

    print("No browsing history found.")
    exit()

history = pd.concat(records)

print("Total rows before cleaning:", len(history))

history = history.dropna(subset=["timestamp"])

print("Rows after removing null timestamps:", len(history))

history = history.sort_values("timestamp")

# -------------------------------------------------
# Save dataset
# -------------------------------------------------

history.to_csv(OUTPUT_FILE, index=False)

print("\n================================================")
print("DATASET SAVED")
print("================================================")

print("Output file:")
print(OUTPUT_FILE)

print("\nFinal dataset rows:", len(history))

print("\nColumns:")
print(history.columns.tolist())

print("\nSample rows:\n")

print(history.head(10))

print("\n================================================")
print("HISTORY EXTRACTION COMPLETED")
print("================================================")