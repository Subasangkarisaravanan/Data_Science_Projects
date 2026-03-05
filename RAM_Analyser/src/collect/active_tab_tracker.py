import time
import psutil
import pandas as pd
from datetime import datetime
import os
import win32gui

print("\n================================================")
print("ACTIVE TAB TRACKER")
print("================================================\n")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

output_file = os.path.join(DATA_DIR, "active_tabs.csv")

records = []

duration = 120
interval = 5

print("Tracking active browser tabs...")

for i in range(duration):

    timestamp = datetime.now()

    window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(window)

    browser = "unknown"

    if "Chrome" in title:
        browser = "chrome"
    elif "Edge" in title:
        browser = "edge"

    records.append({
        "timestamp": timestamp,
        "window_title": title,
        "browser": browser
    })

    print(f"{i+1}/{duration} | Active window: {title}")

    time.sleep(interval)

df = pd.DataFrame(records)

df.to_csv(output_file, index=False)

print("\nActive tab dataset saved:")
print(output_file)