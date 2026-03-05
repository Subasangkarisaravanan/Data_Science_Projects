import psutil
import pandas as pd
import time
import os
from datetime import datetime

print("\n================================================")
print("STEP 1 : RAM LOGGER")
print("================================================\n")

# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

output_file = os.path.join(DATA_DIR, "ram_log.csv")

print("Data folder:")
print(DATA_DIR)

print("\nOutput file:")
print(output_file)

# ------------------------------------------------
# Logging parameters
# ------------------------------------------------

INTERVAL = 5      # seconds
RECORDS = 120     # total rows

print("\nLogging interval:", INTERVAL, "seconds")
print("Total records to capture:", RECORDS)

print("\nStarting RAM monitoring...\n")

# ------------------------------------------------
# Helper function to get browser RAM
# ------------------------------------------------

def get_browser_ram():

    browser_ram = 0

    for proc in psutil.process_iter(['name','memory_info']):

        try:

            name = proc.info['name']

            if name and (
                "chrome" in name.lower() or
                "edge" in name.lower() or
                "firefox" in name.lower()
            ):
                browser_ram += proc.info['memory_info'].rss

        except:
            pass

    return browser_ram / (1024 * 1024)

# ------------------------------------------------
# Collect RAM logs
# ------------------------------------------------

rows = []

for i in range(RECORDS):

    timestamp = datetime.now()

    # system RAM
    ram_used = psutil.virtual_memory().used / (1024 * 1024)

    # browser RAM
    browser_ram = get_browser_ram()

    # CPU usage
    cpu = psutil.cpu_percent(interval=None)

    rows.append({
        "timestamp": timestamp,
        "ram_used_mb": round(ram_used,2),
        "browser_ram_mb": round(browser_ram,2),
        "cpu_percent": cpu
    })

    print(f"{i+1}/{RECORDS} | RAM Used: {ram_used:.2f} MB | Browser RAM: {browser_ram:.2f} MB | CPU: {cpu}%")

    time.sleep(INTERVAL)

# ------------------------------------------------
# Save dataset
# ------------------------------------------------

df = pd.DataFrame(rows)

df.to_csv(output_file, index=False)

print("\n================================================")
print("RAM LOG DATASET SAVED")
print("================================================")

print("Rows captured:", len(df))

print("\nSample rows:\n")
print(df.head())

print("\n================================================")
print("RAM LOGGER COMPLETED")
print("================================================")