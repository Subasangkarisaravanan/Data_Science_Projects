import sqlite3
import pandas as pd
import os

# ---------------- CONFIG ----------------
DB_NAME = "nutrition.db"
OUTPUT_DIR = "powerbi_outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_NAME)

# ---------------- ALL 25 SQL QUERIES ----------------
queries = {

    # ---------- OBESITY ----------
    "q01_avg_obesity_by_region": """
        SELECT Region, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        GROUP BY Region
    """,

    "q02_top10_obesity_countries": """
        SELECT Country, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        GROUP BY Country
        ORDER BY Avg_Obesity DESC
        LIMIT 10
    """,

    "q03_obesity_by_gender": """
        SELECT Gender, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        GROUP BY Gender
    """,

    "q04_obesity_trend_by_year": """
        SELECT Year, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        GROUP BY Year
        ORDER BY Year
    """,

    "q05_female_vs_male_obesity": """
        SELECT Country,
               AVG(CASE WHEN Gender='Female' THEN Mean_Estimate END) AS Female_Obesity,
               AVG(CASE WHEN Gender='Male' THEN Mean_Estimate END) AS Male_Obesity
        FROM obesity
        GROUP BY Country
        HAVING Female_Obesity IS NOT NULL AND Male_Obesity IS NOT NULL
    """,

    # ---------- MALNUTRITION ----------
    "q06_avg_malnutrition_by_region": """
        SELECT Region, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Region
    """,

    "q07_top10_malnutrition_countries": """
        SELECT Country, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Country
        ORDER BY Avg_Malnutrition DESC
        LIMIT 10
    """,

    "q08_malnutrition_by_age_group": """
        SELECT Age_Group, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Age_Group
    """,

    "q09_malnutrition_trend_by_year": """
        SELECT Year, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Year
        ORDER BY Year
    """,

    "q10_child_vs_adult_malnutrition": """
        SELECT Country,
               AVG(CASE WHEN Age_Group='Child/Adolescent' THEN Mean_Estimate END) AS Child_Malnutrition,
               AVG(CASE WHEN Age_Group='Adult' THEN Mean_Estimate END) AS Adult_Malnutrition
        FROM malnutrition
        GROUP BY Country
    """,

    # ---------- COMPARISON ----------
    "q11_obesity_vs_malnutrition": """
        SELECT o.Country,
               AVG(o.Mean_Estimate) AS Avg_Obesity,
               AVG(m.Mean_Estimate) AS Avg_Malnutrition
        FROM obesity o
        JOIN malnutrition m ON o.Country = m.Country
        GROUP BY o.Country
    """,

    "q12_region_dual_burden": """
        SELECT o.Region,
               AVG(o.Mean_Estimate) AS Avg_Obesity,
               AVG(m.Mean_Estimate) AS Avg_Malnutrition
        FROM obesity o
        JOIN malnutrition m ON o.Region = m.Region
        GROUP BY o.Region
    """,

    # ---------- CI WIDTH / RELIABILITY ----------
    "q13_ci_width_obesity_by_region": """
        SELECT Region, AVG(CI_Width) AS Avg_CI_Width
        FROM obesity
        GROUP BY Region
    """,

    "q14_ci_width_malnutrition_by_region": """
        SELECT Region, AVG(CI_Width) AS Avg_CI_Width
        FROM malnutrition
        GROUP BY Region
    """,

    "q15_low_reliability_countries": """
        SELECT Country, AVG(CI_Width) AS Avg_CI_Width
        FROM malnutrition
        GROUP BY Country
        ORDER BY Avg_CI_Width DESC
        LIMIT 10
    """,

    # ---------- YEARLY REGIONAL ----------
    "q16_obesity_year_region": """
        SELECT Year, Region, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        GROUP BY Year, Region
    """,

    "q17_malnutrition_year_region": """
        SELECT Year, Region, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Year, Region
    """,

    # ---------- GENDER & AGE ----------
    "q18_gender_obesity_by_region": """
        SELECT Region, Gender, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        GROUP BY Region, Gender
    """,

    "q19_age_malnutrition_by_region": """
        SELECT Region, Age_Group, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Region, Age_Group
    """,

    # ---------- EXTREMES ----------
    "q20_highest_obesity_year": """
        SELECT Year, MAX(Mean_Estimate) AS Max_Obesity
        FROM obesity
        GROUP BY Year
    """,

    "q21_highest_malnutrition_year": """
        SELECT Year, MAX(Mean_Estimate) AS Max_Malnutrition
        FROM malnutrition
        GROUP BY Year
    """,

    # ---------- SUMMARY ----------
    "q22_country_count_by_region": """
        SELECT Region, COUNT(DISTINCT Country) AS Country_Count
        FROM obesity
        GROUP BY Region
    """,

    "q23_avg_obesity_global": """
        SELECT AVG(Mean_Estimate) AS Global_Avg_Obesity
        FROM obesity
    """,

    "q24_avg_malnutrition_global": """
        SELECT AVG(Mean_Estimate) AS Global_Avg_Malnutrition
        FROM malnutrition
    """,

    "q25_yearly_summary": """
        SELECT Year,
               (SELECT AVG(Mean_Estimate) FROM obesity o WHERE o.Year=m.Year) AS Avg_Obesity,
               AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition m
        GROUP BY Year
    """
}

# ---------------- EXECUTE & EXPORT ----------------
for name, sql in queries.items():
    df = pd.read_sql_query(sql, conn)
    output_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
    df.to_csv(output_path, index=False)
    print(f"✔ Exported: {output_path}")

conn.close()

print("\n🎉 ALL 25 SQL QUERIES EXECUTED & EXPORTED SUCCESSFULLY")
