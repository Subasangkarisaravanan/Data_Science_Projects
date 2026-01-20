import requests
import pandas as pd
from sqlalchemy import create_engine

# ------------------------------
# 1. TiDB/MySQL Engine Setup
# ------------------------------
import pandas as pd
from sqlalchemy import create_engine

# Replace with your MySQL credentials
username = "39RK8eN7Bd2Mo2m.root"
password = "4yvw3Uy2MkmN34gy"
host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"     
port = 4000    
database = "Harvards_Artifacts_Collection"
ca_path = "C:\\Users\\Suba\\OneDrive\\Desktop\\Harvards_Artifacts_Collection\\isrgrootx1.pem" 
# Create SQLAlchemy engine with SSL verification
engine = create_engine(
    f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}',
    connect_args={
        "ssl": {"ca": ca_path}
    }
)
# ------------------------------
# 2. Harvard Art Museums API Setup
# ------------------------------
api_key = "bd697abc-1aab-44dc-86b1-4f9d7bab39b1"
url_classification = "https://api.harvardartmuseums.org/classification"
url_object = "https://api.harvardartmuseums.org/object"

# ------------------------------
# 3. Fetch Classifications
# ------------------------------
all_classifications = []
url = url_classification
params = {"apikey": api_key, "size": 100}

while url:
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching classifications: {response.status_code}")
        break
    data = response.json()
    all_classifications.extend(data.get("records", []))
    url = data.get("info", {}).get("next")
    params = {}

# ------------------------------
# 4. Filter classifications with >=2500 objects
# ------------------------------
accessible_classifications = []
for i in all_classifications:
    classification_name = i["name"]
    params = {"apikey": api_key, "size": 1, "classification": classification_name}
    response = requests.get(url_object, params=params)
    if response.status_code != 200:
        continue
    total_records = response.json().get("info", {}).get("totalrecords", 0)
    if total_records >= 2500:
        accessible_classifications.append(i)

# Show the accessible classifications
print("Classifications with >=2500 objects:")
for idx, item in enumerate(accessible_classifications, start=1):
    print(f"{idx}. {item['name']}")

# ------------------------------
# 5. User selects ONE classification by name
# ------------------------------
selected_name = input("Enter the name of the classification to fetch: ")

# Validate input
classification_names = [i["name"] for i in accessible_classifications]

if selected_name not in classification_names:
    raise ValueError("Invalid classification name!")
else:
    selected_classification = selected_name
    print(f"Fetching objects for classification: {selected_classification}")

# ------------------------------
# 6. Fetch up to 2500 objects for the chosen classification
# ------------------------------
BATCH_SIZE = 100
MAX_RECORDS = 2500

metadata_rows = []
media_rows = []
color_rows = []

page = 1
total_fetched = 0

while total_fetched < MAX_RECORDS:
    params = {
        "apikey": api_key,
        "size": BATCH_SIZE,
        "page": page,
        "classification": selected_classification
    }
    response = requests.get(url_object, params=params)
    if response.status_code != 200:
        print(f"Error fetching objects: {response.status_code}")
        break
    objects = response.json().get("records", [])
    if not objects:
        break

    for obj in objects:
        metadata_rows.append({
            "id": obj.get("id"),
            "title": obj.get("title"),
            "culture": obj.get("culture"),
            "period": obj.get("period"),
            "century": obj.get("century"),
            "medium": obj.get("medium"),
            "dimensions": obj.get("dimensions"),
            "description": obj.get("description"),
            "department": obj.get("division"),
            "classification": obj.get("classification"),
            "accessionyear": obj.get("accessionyear"),
            "accessionmethod": obj.get("accessionmethod")
        })

        media_rows.append({
            "objectid": obj.get("id"),
            "imagecount": len(obj.get("images", [])),
            "mediacount": obj.get("mediacount") or 0,
            "colorcount": len(obj.get("colors", [])) if obj.get("colors") else 0,
            "rank": obj.get("rank") or 0,
            "datebegin": obj.get("datebegin"),
            "dateend": obj.get("dateend")
        })

        for color in obj.get("colors", []):
            color_rows.append({
                "objectid": obj.get("id"),
                "color": color.get("color"),
                "spectrum": color.get("spectrum"),
                "hue": color.get("hue"),
                "percent": color.get("percent"),
                "css3": color.get("css3")
            })

    total_fetched += len(objects)
    page += 1

# ------------------------------
# 7. Insert into TiDB/MySQL
# ------------------------------
if metadata_rows:
    pd.DataFrame(metadata_rows).to_sql("artifact_metadata", engine, if_exists="append", index=False)
if media_rows:
    pd.DataFrame(media_rows).to_sql("artifact_media", engine, if_exists="append", index=False)
if color_rows:
    pd.DataFrame(color_rows).to_sql("artifact_colors", engine, if_exists="append", index=False)

print(f"Inserted {total_fetched} objects for classification: {selected_classification}")
print("Done!")