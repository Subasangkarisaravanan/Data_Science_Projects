import sqlite3
import pandas as pd

# Connect SQLite DB
conn = sqlite3.connect("nutrition.db")

# Dictionary with 25 meaningful queries
queries = {

    # ---------------- OBESITY ----------------
    "Top 5 Countries by Obesity (2022)": """
        SELECT Country, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        WHERE Year = 2022
        GROUP BY Country
        ORDER BY Avg_Obesity DESC
        LIMIT 5;
    """,

    "Top 5 Regions by Obesity (2022)": """
        SELECT Region, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        WHERE Year = 2022
        GROUP BY Region
        ORDER BY Avg_Obesity DESC
        LIMIT 5;
    """,

    "Average Obesity by Gender": """
        SELECT Gender, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        GROUP BY Gender;
    """,

    "India Obesity Trend (2012-2022)": """
        SELECT Year, AVG(Mean_Estimate) AS Avg_Obesity
        FROM obesity
        WHERE Country = 'India'
        GROUP BY Year
        ORDER BY Year;
    """,

    "Country count by obesity level category & age group": """
        SELECT age_group, obesity_level, COUNT(DISTINCT Country) AS country_count
        FROM obesity
        GROUP BY age_group, obesity_level;
    """,

    "Top 5 least reliable countries (highest CI Width)": """
        SELECT Country, AVG(CI_Width) AS Avg_CI
        FROM obesity
        GROUP BY Country
        ORDER BY Avg_CI DESC
        LIMIT 5;
    """,

    "Average obesity by age group": """
        SELECT Age_Group, AVG(Mean_Estimate) AS avg_obesity
        FROM obesity
        GROUP BY Age_Group;
    """,

    "Top 10 countries with consistent LOW obesity (low avg + low CI)": """
        SELECT country,
        AVG(mean_estimate) AS avg_obesity,
        AVG(ci_width) AS avg_ci
        FROM obesity
        GROUP BY country
        HAVING AVG(mean_estimate) < 10
        AND AVG(ci_width) < 2
        ORDER BY avg_obesity ASC, avg_ci ASC
        LIMIT 10;
    """,

    "Countries where Female Obesity Exceeds Male (Large Margin)": """
        SELECT 
        f.Country,
        f.Year,
        f.Age_Group,
        AVG(f.Mean_Estimate) AS Female_Obesity,
        AVG(m.Mean_Estimate) AS Male_Obesity,
        (AVG(f.Mean_Estimate) - AVG(m.Mean_Estimate)) AS Difference
        FROM obesity f
        JOIN obesity m
        ON f.Country = m.Country
        AND f.Year = m.Year
        AND f.Age_Group = m.Age_Group
        WHERE f.Gender = 'Female'
        AND m.Gender = 'Male'
        GROUP BY f.Country, f.Year, f.Age_Group
        HAVING Difference >= 5
        ORDER BY Difference DESC;
    """,

    "Global average obesity percentage per year": """
        SELECT Year, AVG(Mean_Estimate) AS Global_Obesity
        FROM obesity
        GROUP BY Year
        ORDER BY Year;
    """,

    # ---------------- MALNUTRITION ----------------
    "Avg. malnutrition by age group": """
        SELECT Age_Group, AVG(Mean_Estimate) AS avg_malnutrition
        FROM malnutrition
        GROUP BY Age_Group;
    """,

    "Top 5 countries with highest malnutrition(mean_estimate)": """
        SELECT Country, AVG(Mean_Estimate) AS avg_malnutrition
        FROM malnutrition
        GROUP BY Country
        ORDER BY avg_malnutrition DESC
        LIMIT 5;
    """,

    "Malnutrition trend in African region over the years": """
        SELECT Year, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        WHERE Region = 'Africa'
        GROUP BY Year
        ORDER BY Year;
    """,

    "Gender-based average malnutrition": """
        SELECT Gender, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Gender;
    """,

    "Malnutrition level-wise (average CI_Width by age group)": """
        SELECT Age_Group, malnutrition_level, AVG(CI_Width) AS Avg_CI
        FROM malnutrition
        GROUP BY Age_Group, malnutrition_level;
    """,

    "Yearly trend — India, Nigeria, Brazil": """
        SELECT Country, Year, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        WHERE Country IN ('India','Nigeria','Brazil')
        GROUP BY Country, Year
        ORDER BY Country, Year;
    """,

    "Regions with lowest malnutrition averages": """
        SELECT Region, AVG(Mean_Estimate) AS Avg_Malnutrition
        FROM malnutrition
        GROUP BY Region
        ORDER BY Avg_Malnutrition ASC;
    """,

    "Countries with increasing malnutrition": """
        SELECT Country,
        MIN(Mean_Estimate) AS Min_Value,
        MAX(Mean_Estimate) AS Max_Value
        FROM malnutrition
        GROUP BY Country
        HAVING Max_Value > Min_Value;
    """,

    "Min/Max malnutrition levels year-wise comparison": """
        SELECT Year,
        MIN(Mean_Estimate) AS Min_Malnutrition,
        MAX(Mean_Estimate) AS Max_Malnutrition
        FROM malnutrition
        GROUP BY Year
        ORDER BY Year;
    """,

    "High CI_Width flags for monitoring(CI_width > 5)": """
        SELECT *
        FROM malnutrition
        WHERE CI_Width > 5;
    """,

    # ---------------- COMBINED ----------------
    "Obesity vs malnutrition comparison by country": """
        SELECT o.Country,
        AVG(o.Mean_Estimate) AS avg_obesity,
        AVG(m.Mean_Estimate) AS avg_malnutrition
        FROM obesity o
        JOIN malnutrition m
        ON o.Country = m.Country
        GROUP BY o.Country
        LIMIT 5;
    """,

    "Gender-based disparity in both obesity and malnutrition": """
        SELECT o.Gender,
        AVG(o.Mean_Estimate) AS avg_obesity,
        AVG(m.Mean_Estimate) AS avg_malnutrition
        FROM obesity o
        JOIN malnutrition m
        ON o.Gender = m.Gender
        GROUP BY o.Gender;
    """,

    "Region-wise avg estimates side-by-side(Africa and America)": """
        SELECT o.Region,
        AVG(o.Mean_Estimate) AS avg_obesity,
        AVG(m.Mean_Estimate) AS avg_malnutrition
        FROM obesity o
        JOIN malnutrition m
        ON o.Region = m.Region
        WHERE o.Region IN ('Africa','Americas')
        GROUP BY o.Region;
    """,

    "Countries with obesity up & malnutrition down": """
        SELECT o.Age_Group, o.Year,
        AVG(o.Mean_Estimate) AS avg_obesity,
        AVG(m.Mean_Estimate) AS avg_malnutrition
        FROM obesity o
        JOIN malnutrition m
        ON o.Year = m.Year AND o.Age_Group = m.Age_Group
        GROUP BY o.Age_Group, o.Year
        ORDER BY o.Age_Group, o.Year;
    """,

    "Age-wise trend analysis": """
        SELECT o.Year, o.Age_Group,
        AVG(o.Mean_Estimate) AS Avg_Obesity,
        AVG(m.Mean_Estimate) AS Avg_Malnutrition
        FROM obesity o
        JOIN malnutrition m
        ON o.Country=m.Country
        AND o.Year=m.Year
        AND o.Gender=m.Gender
        AND o.Age_Group=m.Age_Group
        GROUP BY o.Year, o.Age_Group
        ORDER BY o.Year;
    """
}

# Execute queries and store results
results = {}
for name, q in queries.items():
    results[name] = pd.read_sql_query(q, conn)
    print(f"\n{name}:\n", results[name].head(10))  # show top 10 rows for preview

conn.close()