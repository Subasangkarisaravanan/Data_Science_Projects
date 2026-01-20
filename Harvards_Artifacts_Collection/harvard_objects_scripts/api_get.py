import requests
import time
import json
import os
import re

# -------------------------------
# Configuration
# -------------------------------
api_key = "bd697abc-1aab-44dc-86b1-4f9d7bab39b1"

base_url_classification = f"https://api.harvardartmuseums.org/classification?apikey={api_key}"
base_url_object = f"https://api.harvardartmuseums.org/object?apikey={api_key}"

# Folder to save JSON files inside your project folder
# Determine main project folder
#project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#data_folder = os.path.join(project_folder, "harvard_objects_data")
#os.makedirs(data_folder, exist_ok=True)

MAX_OBJECTS = 2500
PAGE_SIZE = 100

# -------------------------------
# Step 1: Fetch all classifications
# -------------------------------
classifications = []
page = 1

while True:
    url = f"{base_url_classification}&page={page}"
    response = requests.get(url).json()
    classifications.extend(response.get('records', []))
    if page >= response['info']['pages']:
        break
    page += 1
    time.sleep(0.1)

print(f"Total classifications found: {len(classifications)}")

# -------------------------------
# Step 2: Fetch objects per classification
# -------------------------------
for classification in classifications:
    class_name = classification['name']
    print(f"\nFetching objects for classification: {class_name}")

    objects = []
    page_num = 1

    while len(objects) < MAX_OBJECTS:
        url_object = f"{base_url_object}&classification={class_name}&size={PAGE_SIZE}&page={page_num}"
        response = requests.get(url_object).json()
        records = response.get('records', [])
        objects.extend(records)

        if page_num >= response['info']['pages']:
            break
        page_num += 1
        time.sleep(0.1)

    objects = objects[:MAX_OBJECTS]

    # -------------------------------
    # Step 3: Save to JSON inside harvard_objects_data
    # -------------------------------
   # safe_class_name = re.sub(r'[\\/:"*?<>|]+', '_', class_name.strip())
    #filename = os.path.join(data_folder, f"{safe_class_name}.json")

    #with open(filename, "w", encoding="utf-8") as f:
        #json.dump(objects, f, ensure_ascii=False, indent=2)

    print(f"Collected and saved {len(objects)} objects for classification: {class_name}")

#print("\nAll data fetching and saving complete!")
#print(f"All JSON files are stored in: {data_folder}")
