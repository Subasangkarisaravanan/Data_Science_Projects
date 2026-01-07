import sqlite3
import pandas as pd

# Connect DB
conn = sqlite3.connect("nutrition.db")

# Create tables
conn.execute("""
CREATE TABLE IF NOT EXISTS obesity(
    Year INTEGER, Gender TEXT, Mean_Estimate REAL, LowerBound REAL,
    UpperBound REAL, age_group TEXT, Country TEXT, Region TEXT,
    CI_Width REAL, obesity_level TEXT
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS malnutrition(
    Year INTEGER, Gender TEXT, Mean_Estimate REAL, LowerBound REAL,
    UpperBound REAL, age_group TEXT, Country TEXT, Region TEXT,
    CI_Width REAL, malnutrition_level TEXT
)
""")

# Insert data
df_obesity = pd.read_csv("df_obesity_clean.csv")
df_malnutrition = pd.read_csv("df_malnutrition_clean.csv")

df_obesity.to_sql("obesity", conn, if_exists='replace', index=False)
df_malnutrition.to_sql("malnutrition", conn, if_exists='replace', index=False)

conn.commit()
conn.close()
print("SQLite DB ready with data!")