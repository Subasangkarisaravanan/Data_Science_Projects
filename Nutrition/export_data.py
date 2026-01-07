import sqlite3
import pandas as pd

conn = sqlite3.connect("nutrition.db")

obesity_df = pd.read_sql_query("SELECT * FROM obesity", conn)
malnutrition_df = pd.read_sql_query("SELECT * FROM malnutrition", conn)

obesity_df.to_csv("obesity.csv", index=False)
malnutrition_df.to_csv("malnutrition.csv", index=False)

conn.close()
