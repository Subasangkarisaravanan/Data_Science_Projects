import streamlit as st
import pandas as pd
import sqlite3
import requests

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
API_KEY = "bd697abc-1aab-44dc-86b1-4f9d7bab39b1"
URL_OBJECT = "https://api.harvardartmuseums.org/object"

# ------------------------------
# 3. Fixed Classifications
# ------------------------------
accessible_classifications = [
    "Photographs",
    "Drawings",
    "Prints",
    "Paintings",
    "Coins",
    "Vessels"
]

st.title("Harvard Artifacts Collection")
st.write("Welcome to Harvard Museum")

# ------------------------------
# Store selected classification in session_state to persist
# ------------------------------
if "selected_classification" not in st.session_state:
    st.session_state.selected_classification = accessible_classifications[0]

st.session_state.selected_classification = st.selectbox(
    "Select Classification",
    accessible_classifications,
    index=accessible_classifications.index(st.session_state.selected_classification)
)

selected_classification = st.session_state.selected_classification

# ------------------------------
# Step-wise buttons
# ------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    collect_data_btn = st.button("Collect Data")
with col2:
    migrate_sql_btn = st.button("Migrate to SQL")
with col3:
    sql_query_btn = st.button("SQL Queries")

# ------------------------------
# Initialize session state and data containers
# ------------------------------
for key in ["metadata_rows", "media_rows", "color_rows", "show_sql_queries"]:
    if key not in st.session_state:
        st.session_state[key] = [] if "rows" in key else False

metadata_rows = st.session_state.metadata_rows
media_rows = st.session_state.media_rows
color_rows = st.session_state.color_rows

# ------------------------------
# 4. Collect Data → Show JSON (3 columns)
# ------------------------------
if collect_data_btn:
    st.info(f"Fetching 2500+ records for classification: {selected_classification}...")

    BATCH_SIZE = 100
    MAX_RECORDS = 2500
    page = 1
    total_fetched = 0

    progress_bar = st.progress(0)
    status_text = st.empty()

    metadata_rows.clear()
    media_rows.clear()
    color_rows.clear()

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
        progress_bar.progress(min(total_fetched / MAX_RECORDS, 1.0))
        status_text.text(f"Fetched {total_fetched} / {MAX_RECORDS} objects...")

    # Save back to session state
    st.session_state.metadata_rows = metadata_rows
    st.session_state.media_rows = media_rows
    st.session_state.color_rows = color_rows

    # Display JSON in 3 columns
    st.subheader("List of Collected Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Metadata**")
        st.json(metadata_rows[:10])
    with col2:
        st.write("**Media**")
        st.json(media_rows[:10])
    with col3:
        st.write("**Colors**")
        st.json(color_rows[:10])

# ------------------------------
# 5. Migrate to SQL → Show Inserted Data
# ------------------------------
if migrate_sql_btn:
    if not metadata_rows:
        st.error("No data collected yet! Click 'Collect Data' first.")
    else:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Insert metadata
        cursor.executemany("""
            INSERT OR IGNORE INTO artifact_metadata 
            (id, title, culture, period, century, medium, dimensions, description, department, classification, accessionyear, accessionmethod)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [(m["id"], m["title"], m["culture"], m["period"], m["century"], m["medium"], m["dimensions"], m["description"],
               m["department"], m["classification"], m["accessionyear"], m["accessionmethod"]) for m in metadata_rows])

        # Insert media
        cursor.executemany("""
            INSERT OR IGNORE INTO artifact_media 
            (objectid, imagecount, mediacount, colorcount, rank, datebegin, dateend)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [(m["objectid"], m["imagecount"], m["mediacount"], m["colorcount"], m["rank"], m["datebegin"], m["dateend"]) for m in media_rows])

        # Insert colors
        cursor.executemany("""
            INSERT OR IGNORE INTO artifact_colors
            (objectid, color, spectrum, hue, percent, css3)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [(c["objectid"], c["color"], c["spectrum"], c["hue"], c["percent"], c["css3"]) for c in color_rows])

        conn.commit()

        st.subheader("All Inserted Records for Current Classification")
        df_meta = pd.read_sql_query(f"SELECT * FROM artifact_metadata WHERE classification=? ORDER BY id LIMIT 10", conn, params=(selected_classification,))
        df_media = pd.read_sql_query(f"""
            SELECT * FROM artifact_media 
            WHERE objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
            ORDER BY objectid LIMIT 10
        """, conn, params=(selected_classification,))
        df_colors = pd.read_sql_query(f"""
            SELECT * FROM artifact_colors 
            WHERE objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
            ORDER BY objectid LIMIT 10
        """, conn, params=(selected_classification,))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**Metadata Table**")
            st.dataframe(df_meta)
        with col2:
            st.write("**Media Table**")
            st.dataframe(df_media)
        with col3:
            st.write("**Colors Table**")
            st.dataframe(df_colors)

        conn.close()

# ------------------------------
# 6. SQL Queries Section
# ------------------------------
if sql_query_btn:
    st.session_state.show_sql_queries = True

if st.session_state.show_sql_queries:
    st.subheader("SQL Queries")

    query_options = [
        "List all artifacts from the 11th century belonging to Byzantine culture.",
        "What are the unique cultures represented in the artifacts?",
        "List all artifacts from the Archaic Period.",
        "List artifact titles ordered by accession year in descending order.",
        "How many artifacts are there per department?",
        "Which artifacts have more than 1 image?",
        "What is the average rank of all artifacts?",
        "Which artifacts have more colors than media files?",
        "List all artifacts created between 1500 and 1600.",
        "How many artifacts have no media files?",
        "What are all the distinct hues used in the dataset?",
        "What are the top 5 most used colors by frequency?",
        "What is the average coverage percentage for each hue?",
        "List all colors used for a given artifact ID.",  # special
        "What is the total number of color entries in the dataset?",
        "List artifact titles, cultures, and hues for Byzantine artifacts.",
        "List each artifact title with its associated hues.",
        "Get artifact titles, cultures, and media ranks where the period is not null.",
        "Find artifact titles ranked in the top 10 that include the color hue Grey.",
        "How many artifacts exist per classification, and what is the average media count for each?",
        "List artifact titles with their total number of media files.",
        "Show artifact titles, hues, and media counts for artifacts from the British period.",
        "Find all artifacts with the hue Blue and their corresponding rank.",
        "List each artifact title with its culture and the number of associated colors.",
        "Get the average rank of artifacts per culture.",
        "List artifact titles along with all their hues and media counts, ordered by rank descending.",
        "Find artifacts where the number of colors exceeds the number of media files.",
        "Show the top 5 artifacts with the most colors used.",
        "List artifact titles, cultures, and hues for artifacts acquired after 1800.",
        "Find all artifacts that share the same hue."
    ]

    selected_query = st.selectbox("Select a Query", query_options)

    # For the artifact ID query, show a text input
    artifact_id_input = ""
    if selected_query == query_options[13]:
        artifact_id_input = st.text_input("Enter Artifact ID (only for this query)")

    # Run Query button
    if st.button("Run Query"):
        conn = sqlite3.connect(DB_PATH)

        if selected_query == query_options[13]:
            if not artifact_id_input.strip():
                st.error("Please enter an Artifact ID.")
                conn.close()
            else:
                df = pd.read_sql_query(
                    "SELECT DISTINCT color FROM artifact_colors WHERE objectid=?",
                    conn,
                    params=(artifact_id_input.strip(),)
                )
                st.subheader("Query Results")
                st.dataframe(df)
                conn.close()
        else:
            # Queries with classification parameter
            queries = {
                query_options[0]: "SELECT * FROM artifact_metadata WHERE century='11th century' AND culture='Byzantine' AND classification=?",
                query_options[1]: "SELECT DISTINCT culture FROM artifact_metadata WHERE classification=?",
                query_options[2]: "SELECT * FROM artifact_metadata WHERE period='Archaic Period' AND classification=?",
                query_options[3]: "SELECT title, accessionyear FROM artifact_metadata WHERE classification=? ORDER BY accessionyear DESC",
                query_options[4]: "SELECT department, COUNT(*) AS artifact_count FROM artifact_metadata WHERE classification=? GROUP BY department",
                query_options[5]: """
                    SELECT * FROM artifact_media 
                    WHERE imagecount > 1 
                    AND objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                """,
                query_options[6]: """
                    SELECT AVG(rank) AS average_rank 
                    FROM artifact_media 
                    WHERE rank IS NOT NULL 
                    AND objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                """,
                query_options[7]: """
                    SELECT * FROM artifact_media
                    WHERE colorcount > mediacount
                    AND objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                """,
                query_options[8]: """
                    SELECT * FROM artifact_media
                    WHERE datebegin BETWEEN 1500 AND 1600
                    AND objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                """,
                query_options[9]: """
                    SELECT * FROM artifact_media
                    WHERE mediacount = 0
                    AND objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                """,
                query_options[10]: """
                    SELECT DISTINCT hue
                    FROM artifact_colors
                    WHERE objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                """,
                query_options[11]: """
                    SELECT color, COUNT(*) AS frequency
                    FROM artifact_colors
                    WHERE color IS NOT NULL
                    AND objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                    GROUP BY color
                    ORDER BY frequency DESC
                    LIMIT 5
                """,
                query_options[12]: """
                    SELECT hue, AVG(percent) AS average_percentage
                    FROM artifact_colors
                    WHERE hue IS NOT NULL AND percent IS NOT NULL
                    AND objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                    GROUP BY hue
                    ORDER BY average_percentage DESC
                """,
                query_options[14]: """
                    SELECT COUNT(*) AS color_count
                    FROM artifact_colors
                    WHERE color IS NOT NULL
                    AND objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                """,
                query_options[15]: """
                    SELECT m.title, m.culture, c.hue
                    FROM artifact_metadata m
                    JOIN artifact_colors c ON m.id=c.objectid
                    WHERE m.culture='Byzantine' AND m.classification=?
                """,
                query_options[16]: """
                    SELECT m.title, c.hue
                    FROM artifact_metadata m
                    JOIN artifact_colors c ON m.id=c.objectid
                    WHERE m.classification=?
                """,
                query_options[17]: """
                    SELECT m.title, m.culture, md.rank
                    FROM artifact_metadata m
                    JOIN artifact_media md ON m.id=md.objectid
                    WHERE m.period IS NOT NULL AND m.classification=?
                """,
                query_options[18]: """
                    SELECT m.title, md.rank
                    FROM artifact_metadata m
                    JOIN artifact_media md ON m.id=md.objectid
                    JOIN artifact_colors c ON m.id=c.objectid
                    WHERE c.hue='Grey' AND m.classification=?
                    ORDER BY md.rank DESC
                    LIMIT 10
                """,
                query_options[19]: """
                    SELECT m.classification,
                           COUNT(DISTINCT m.id) AS artifact_count,
                           AVG(md.mediacount) AS average_media_count
                    FROM artifact_metadata m
                    JOIN artifact_media md ON m.id=md.objectid
                    WHERE m.classification=?
                    GROUP BY m.classification
                """,
                query_options[20]: """
                    SELECT m.title, COUNT(md.mediacount) AS number_of_media_files
                    FROM artifact_metadata m
                    JOIN artifact_media md ON m.id=md.objectid
                    WHERE m.classification=?
                    GROUP BY m.title
                    ORDER BY number_of_media_files DESC
                """,
                query_options[21]: """
                    SELECT m.title, c.hue, md.mediacount
                    FROM artifact_metadata m
                    JOIN artifact_colors c ON m.id=c.objectid
                    JOIN artifact_media md ON m.id=md.objectid
                    WHERE m.period='British period' AND m.classification=?
                """,
                query_options[22]: """
                    SELECT m.title, md.rank, c.hue
                    FROM artifact_metadata m
                    JOIN artifact_media md ON m.id=md.objectid
                    JOIN artifact_colors c ON m.id=c.objectid
                    WHERE c.hue='Blue' AND m.classification=?
                """,
                query_options[23]: """
                    SELECT m.title, m.culture, COUNT(c.color) AS color_count
                    FROM artifact_metadata m
                    JOIN artifact_colors c ON m.id=c.objectid
                    WHERE m.classification=?
                    GROUP BY m.title, m.culture
                    ORDER BY color_count DESC
                """,
                query_options[24]: """
                    SELECT m.culture, AVG(md.rank) AS average_rank
                    FROM artifact_metadata m
                    JOIN artifact_media md ON m.id=md.objectid
                    WHERE m.classification=?
                    GROUP BY m.culture
                    ORDER BY average_rank DESC
                """,
                query_options[25]: """
                    SELECT m.title, c.hue, md.mediacount
                    FROM artifact_metadata m
                    JOIN artifact_colors c ON m.id=c.objectid
                    JOIN artifact_media md ON m.id=md.objectid
                    WHERE m.classification=?
                    ORDER BY md.rank DESC
                """,
                query_options[26]: """
                    SELECT m.title, COUNT(c.color) AS color_count, md.mediacount
                    FROM artifact_metadata m
                    JOIN artifact_colors c ON m.id=c.objectid
                    JOIN artifact_media md ON m.id=md.objectid
                    WHERE m.classification=?
                    GROUP BY m.title, md.mediacount
                    HAVING color_count > md.mediacount
                """,
                query_options[27]: """
                    SELECT m.title, m.culture, COUNT(c.color) AS color_count
                    FROM artifact_metadata m
                    JOIN artifact_colors c ON m.id=c.objectid
                    WHERE m.classification=?
                    GROUP BY m.title, m.culture
                    ORDER BY color_count DESC
                    LIMIT 5
                """,
                query_options[28]: """
                    SELECT m.title, m.culture, c.hue
                    FROM artifact_metadata m
                    JOIN artifact_colors c ON m.id=c.objectid
                    WHERE m.accessionyear > 1800 AND m.classification=?
                """,
                query_options[29]: """
                    SELECT m.title, m.culture, c.hue
                    FROM artifact_metadata m
                    JOIN artifact_colors c ON m.id=c.objectid
                    WHERE c.hue IN (
                        SELECT hue FROM artifact_colors
                        WHERE objectid IN (SELECT id FROM artifact_metadata WHERE classification=?)
                        GROUP BY hue
                        HAVING COUNT(DISTINCT objectid) > 1
                    )
                    AND m.classification=?
                    ORDER BY c.hue, m.title
                """
            }

            # Run the query with classification
            params = (selected_classification,) if selected_query != query_options[29] else (selected_classification, selected_classification)
            df = pd.read_sql_query(queries[selected_query], conn, params=params)
            st.subheader("Query Results")
            st.dataframe(df)
            conn.close()
