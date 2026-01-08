import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

# ----------------------- Connect to SQLite -----------------------
conn = sqlite3.connect("nutrition.db")

# ----------------------- Queries Dictionary (25 Queries) -----------------------
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

# ----------------------- Streamlit UI -----------------------
st.title("🌍 Nutrition Paradox Dashboard")
st.markdown("Select a query from the dropdown to view results and charts:")

selected_query_name = st.selectbox("Choose Query", list(queries.keys()))

query = queries[selected_query_name]
df = pd.read_sql_query(query, conn)

st.subheader("Query Result")
st.dataframe(df)

# ----------------------- Auto Charting -----------------------
if not df.empty:

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    object_cols = [c for c in df.columns if c not in numeric_cols]

    if len(numeric_cols) == 1 and len(object_cols) >= 1:
        x = object_cols[0]
        y = numeric_cols[0]
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(f"{x}:N", sort='-y'),
            y=alt.Y(f"{y}:Q"),
            tooltip=[x, y]
        )
        st.altair_chart(chart, use_container_width=True)

    elif "Year" in df.columns and len(numeric_cols) >= 1:
        for y in numeric_cols:
            chart = alt.Chart(df).mark_line(point=True).encode(
                x="Year:O",
                y=alt.Y(f"{y}:Q"),
                tooltip=["Year", y]
            )
            st.altair_chart(chart, use_container_width=True)

    elif len(numeric_cols) > 1 and len(object_cols) >= 1:
        id_var = object_cols[0]
        df_long = df.melt(id_vars=[id_var], value_vars=numeric_cols,
                          var_name="Metric", value_name="Value")
        chart = alt.Chart(df_long).mark_bar().encode(
            x=f"{id_var}:N",
            y="Value:Q",
            color="Metric:N",
            tooltip=[id_var, "Metric", "Value"]
        )
        st.altair_chart(chart, use_container_width=True)

    else:
        st.warning("No numeric columns detected for charting.")

conn.close()