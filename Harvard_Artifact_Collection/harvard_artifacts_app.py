# ------------------------------
# Harvard Artifacts Collection Streamlit App
# ------------------------------

import streamlit  as st
import requests
import sqlite3
import pandas as pd

# ------------------------------
# 1. Database Setup
# ------------------------------
DB_PATH = "harvard_artifacts.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Metadata table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_metadata (
        id INTEGER PRIMARY KEY,
        title TEXT,
        culture TEXT,
        period TEXT,
        century TEXT,
        medium TEXT,
        dimensions TEXT,
        description TEXT,
        department TEXT,
        classification TEXT,
        accessionyear INTEGER,
        accessionmethod TEXT
    )
    """)
    
    # Media table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_media (
        objectid INTEGER,
        imagecount INTEGER,
        mediacount INTEGER,
        colorcount INTEGER,
        rank INTEGER,
        datebegin INTEGER,
        dateend INTEGER,
        FOREIGN KEY(objectid) REFERENCES artifact_metadata(id)
    )
    """)
    
    # Colors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_colors (
        objectid INTEGER,
        color TEXT,
        spectrum TEXT,
        hue TEXT,
        percent REAL,
        css3 TEXT,
        FOREIGN KEY(objectid) REFERENCES artifact_metadata(id)
    )
    """)
    
    conn.commit()
    conn.close()

init_db()

# ------------------------------
# 2. API Setup
# ------------------------------
API_KEY = "YOUR_API_KEY_HERE"
URL_CLASSIFICATION = "https://api.harvardartmuseums.org/classification"
URL_OBJECT = "https://api.harvardartmuseums.org/object"

# ------------------------------
# 3. Fetch Classifications
# ------------------------------
@st.cache_data
def get_accessible_classifications():
    all_classifications = []
    url = URL_CLASSIFICATION
    params = {"apikey": API_KEY, "size": 100}

    while url:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            st.error(f"Error fetching classifications: {response.status_code}")
            break
        data = response.json()
        all_classifications.extend(data.get("records", []))
        url = data.get("info", {}).get("next")
        params = {}

    accessible_classifications = []
    for i in all_classifications:
        classification_name = i["name"]
        params = {"apikey": API_KEY, "size": 1, "classification": classification_name}
        response = requests.get(URL_OBJECT, params=params)
        if response.status_code != 200:
            continue
        total_records = response.json().get("info", {}).get("totalrecords", 0)
        if total_records >= 2500:
            accessible_classifications.append(i["name"])
    return accessible_classifications

# ------------------------------
# 4. Streamlit UI
# ------------------------------
st.title("🏛️ Harvard Artifacts Collection: ETL & SQL Analytics")
st.write("""
Explore, collect, store, and query rich artifact collections from Harvard's digital archive.
""")

accessible_classifications = get_accessible_classifications()
selected_classification = st.selectbox("Select Classification", accessible_classifications)

# ------------------------------
# 5. Fetch & Store Data
# ------------------------------
if st.button("Collect & Store Data"):
    st.info(f"Fetching 2500+ records for classification: {selected_classification}...")
    
    BATCH_SIZE = 100
    MAX_RECORDS = 2500
    page = 1
    total_fetched = 0

    metadata_rows, media_rows, color_rows = [], [], []
    progress_bar = st.progress(0)
    status_text = st.empty()

    while total_fetched < MAX_RECORDS:
        params = {
            "apikey": API_KEY,
            "size": BATCH_SIZE,
            "page": page,
            "classification": selected_classification
        }
        response = requests.get(URL_OBJECT, params=params)
        if response.status_code != 200:
            st.error(f"Error fetching objects: {response.status_code}")
            break
        objects = response.json().get("records", [])
        if not objects:
            break

        for obj in objects:
            metadata_rows.append((
                obj.get("id"),
                obj.get("title"),
                obj.get("culture"),
                obj.get("period"),
                obj.get("century"),
                obj.get("medium"),
                obj.get("dimensions"),
                obj.get("description"),
                obj.get("division"),
                obj.get("classification"),
                obj.get("accessionyear"),
                obj.get("accessionmethod")
            ))

            media_rows.append((
                obj.get("id"),
                len(obj.get("images", [])),
                obj.get("mediacount") or 0,
                len(obj.get("colors", [])) if obj.get("colors") else 0,
                obj.get("rank") or 0,
                obj.get("datebegin"),
                obj.get("dateend")
            ))

            for color in obj.get("colors", []):
                color_rows.append((
                    obj.get("id"),
                    color.get("color"),
                    color.get("spectrum"),
                    color.get("hue"),
                    color.get("percent"),
                    color.get("css3")
                ))

        total_fetched += len(objects)
        page += 1

        progress_bar.progress(min(total_fetched / MAX_RECORDS, 1.0))
        status_text.text(f"Fetched {total_fetched} / {MAX_RECORDS} objects...")

    # Insert into SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany("""
    INSERT OR IGNORE INTO artifact_metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, metadata_rows)
    cursor.executemany("""
    INSERT OR IGNORE INTO artifact_media VALUES (?, ?, ?, ?, ?, ?, ?)
    """, media_rows)
    cursor.executemany("""
    INSERT OR IGNORE INTO artifact_colors VALUES (?, ?, ?, ?, ?, ?)
    """, color_rows)
    conn.commit()
    conn.close()

    st.success(f"Inserted {total_fetched} objects for classification: {selected_classification}")
    st.subheader("Sample Metadata Preview")
    st.dataframe(pd.DataFrame(metadata_rows).head(10))

# ------------------------------
# 6. SQL Queries Section
# ------------------------------
st.subheader("Run Predefined SQL Queries")

query_options = [
    # Metadata Queries
    "Artifacts from 11th century Byzantine culture",
    "Unique cultures represented",
    "Artifacts from Archaic Period",
    "Artifact titles by descending accession year",
    "Number of artifacts per department",
    # Media Queries
    "Artifacts with more than 1 image",
    "Average rank of artifacts",
    "Artifacts with colorcount > mediacount",
    "Artifacts created between 1500 and 1600",
    "Artifacts with no media files",
    # Color Queries
    "Distinct hues used",
    "Top 5 most used colors",
    "Average coverage percentage per hue",
    "Colors for a given artifact ID",
    "Total number of color entries",
    # Join Queries
    "Artifact titles and hues for Byzantine culture",
    "Each artifact title with associated hues",
    "Artifact titles, cultures, media ranks where period is not null",
    "Top 10 artifacts including hue 'Grey'",
    "Number of artifacts per classification and avg media count"
]

selected_query = st.selectbox("Select a query", query_options)

# Input for artifact ID (for color query)
artifact_id_input = st.text_input("Enter Artifact ID (only for 'Colors for a given artifact ID'):")

if st.button("Run Query"):
    conn = sqlite3.connect(DB_PATH)
    
    if selected_query == "Artifacts from 11th century Byzantine culture":
        df = pd.read_sql_query(
            "SELECT * FROM artifact_metadata WHERE century='11th century' AND culture='Byzantine'", conn)
    elif selected_query == "Unique cultures represented":
        df = pd.read_sql_query(
            "SELECT DISTINCT culture FROM artifact_metadata", conn)
    elif selected_query == "Artifacts from Archaic Period":
        df = pd.read_sql_query(
            "SELECT * FROM artifact_metadata WHERE period='Archaic Period'", conn)
    elif selected_query == "Artifact titles by descending accession year":
        df = pd.read_sql_query(
            "SELECT title, accessionyear FROM artifact_metadata ORDER BY accessionyear DESC", conn)
    elif selected_query == "Number of artifacts per department":
        df = pd.read_sql_query(
            "SELECT department, COUNT(*) as count FROM artifact_metadata GROUP BY department", conn)
    elif selected_query == "Artifacts with more than 1 image":
        df = pd.read_sql_query(
            "SELECT * FROM artifact_media WHERE imagecount > 1", conn)
    elif selected_query == "Average rank of artifacts":
        df = pd.read_sql_query(
            "SELECT AVG(rank) as average_rank FROM artifact_media", conn)
    elif selected_query == "Artifacts with colorcount > mediacount":
        df = pd.read_sql_query(
            "SELECT * FROM artifact_media WHERE colorcount > mediacount", conn)
    elif selected_query == "Artifacts created between 1500 and 1600":
        df = pd.read_sql_query(
            "SELECT * FROM artifact_media WHERE datebegin >= 1500 AND dateend <= 1600", conn)
    elif selected_query == "Artifacts with no media files":
        df = pd.read_sql_query(
            "SELECT * FROM artifact_media WHERE mediacount=0 OR mediacount IS NULL", conn)
    elif selected_query == "Distinct hues used":
        df = pd.read_sql_query(
            "SELECT DISTINCT hue FROM artifact_colors", conn)
    elif selected_query == "Top 5 most used colors":
        df = pd.read_sql_query(
            "SELECT color, COUNT(*) as freq FROM artifact_colors GROUP BY color ORDER BY freq DESC LIMIT 5", conn)
    elif selected_query == "Average coverage percentage per hue":
        df = pd.read_sql_query(
            "SELECT hue, AVG(percent) as avg_percent FROM artifact_colors GROUP BY hue", conn)
    elif selected_query == "Colors for a given artifact ID":
        if artifact_id_input.strip() == "":
            st.error("Please enter an Artifact ID!")
            conn.close()
            st.stop()
        df = pd.read_sql_query(
            f"SELECT * FROM artifact_colors WHERE objectid={artifact_id_input}", conn)
    elif selected_query == "Total number of color entries":
        df = pd.read_sql_query(
            "SELECT COUNT(*) as total_colors FROM artifact_colors", conn)
    elif selected_query == "Artifact titles and hues for Byzantine culture":
        df = pd.read_sql_query(
            """SELECT m.title, c.hue 
               FROM artifact_metadata m
               JOIN artifact_colors c ON m.id=c.objectid
               WHERE m.culture='Byzantine'""", conn)
    elif selected_query == "Each artifact title with associated hues":
        df = pd.read_sql_query(
            """SELECT m.title, c.hue
               FROM artifact_metadata m
               JOIN artifact_colors c ON m.id=c.objectid""", conn)
    elif selected_query == "Artifact titles, cultures, media ranks where period is not null":
        df = pd.read_sql_query(
            """SELECT m.title, m.culture, md.rank 
               FROM artifact_metadata m
               JOIN artifact_media md ON m.id=md.objectid
               WHERE m.period IS NOT NULL""", conn)
    elif selected_query == "Top 10 artifacts including hue 'Grey'":
        df = pd.read_sql_query(
            """SELECT m.title, md.rank, c.hue
               FROM artifact_metadata m
               JOIN artifact_media md ON m.id=md.objectid
               JOIN artifact_colors c ON m.id=c.objectid
               WHERE c.hue='Grey'
               ORDER BY md.rank DESC
               LIMIT 10""", conn)
    elif selected_query == "Number of artifacts per classification and avg media count":
        df = pd.read_sql_query(
            """SELECT m.classification, COUNT(*) as total_artifacts, AVG(md.mediacount) as avg_mediacount
               FROM artifact_metadata m
               JOIN artifact_media md ON m.id=md.objectid
               GROUP BY m.classification""", conn)
    
    st.dataframe(df)
    conn.close()
