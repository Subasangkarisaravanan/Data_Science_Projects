import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="RAM Analyzer Dashboard",
    layout="wide",
    page_icon="📊"
)

# =====================================
# CORRECT BASE PATH (FIXED)
# =====================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_history.csv")
REPORT_PATH = os.path.join(BASE_DIR, "RAM_Analysis_Report.pdf")

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("❌ Cleaned data not found. Run clean_history.py first.")
        st.stop()

    df = pd.read_csv(DATA_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

df_original = load_data()
df = df_original.copy()

# =====================================
# SIDEBAR
# =====================================
st.sidebar.title("📊 RAM Analyzer")

# Theme toggle
theme = st.sidebar.radio("Theme", ["Light", "Dark"])

# Reset button
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.clear()
    st.rerun()

menu = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Category Analysis",
    "Time Analysis",
    "AI Insights",
    "Raw Data"
])

st.sidebar.divider()

# =====================================
# FILTERS
# =====================================
st.sidebar.subheader("Filters")

search = st.sidebar.text_input("🔍 Search URL")
date_range = st.sidebar.date_input("📅 Date Range", [])

if search:
    df = df[df["url"].str.contains(search, case=False, na=False)]

if len(date_range) == 2:
    start, end = date_range
    df = df[
        (df["timestamp"].dt.date >= start) &
        (df["timestamp"].dt.date <= end)
    ]

# =====================================
# EMPTY DATA HANDLING
# =====================================
if df.empty:
    st.warning("⚠️ No matching data found")

    if search:
        st.write(f"🔍 No results for: `{search}`")

    if len(date_range) == 2:
        st.write(f"📅 No data between {start} and {end}")

    st.info("👉 Try resetting filters")

    st.stop()

# =====================================
# DOWNLOAD OPTIONS
# =====================================
st.sidebar.subheader("📥 Downloads")

# CSV download
csv = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="Download CSV",
    data=csv,
    file_name="cleaned_history.csv",
    mime="text/csv"
)

# PDF download
if os.path.exists(REPORT_PATH):
    with open(REPORT_PATH, "rb") as f:
        st.sidebar.download_button(
            label="Download Report",
            data=f,
            file_name="RAM_Analysis_Report.pdf",
            mime="application/pdf"
        )
else:
    st.sidebar.info("Report not generated")

# =====================================
# THEME STYLE
# =====================================
if theme == "Dark":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# =====================================
# AI INSIGHTS FUNCTION
# =====================================
def generate_insights(df):

    df["hour"] = df["timestamp"].dt.hour
    peak_hour = df["hour"].value_counts().idxmax()

    if peak_hour < 12:
        peak_time = f"{peak_hour} AM"
    elif peak_hour == 12:
        peak_time = "12 PM"
    else:
        peak_time = f"{peak_hour-12} PM"

    top_category = df["category"].value_counts().idxmax()
    top_website = df["url"].value_counts().idxmax()
    top_sites = df["url"].value_counts().head(3).index.tolist()

    heavy_keywords = ["youtube", "netflix", "primevideo", "hotstar"]
    heavy_sites = set()

    for url in df["url"]:
        for k in heavy_keywords:
            if k in str(url).lower():
                heavy_sites.add(k)

    slow_sites = df["url"].value_counts()
    slow_sites = slow_sites[slow_sites > 10].index.tolist()[:3]

    insights = [
        f"Peak usage time: {peak_time}",
        f"Top category: {top_category}",
        f"Most visited site: {top_website}",
        f"Top sites: {', '.join(top_sites)}"
    ]

    if heavy_sites:
        insights.append(f"High RAM usage sites: {', '.join(heavy_sites)}")

    if slow_sites:
        insights.append(f"Heavy/slow sites: {', '.join(slow_sites)}")

    return insights

# =====================================
# DASHBOARD
# =====================================
if menu == "Dashboard":

    st.title("📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Top Category", df["category"].value_counts().idxmax())
    col3.metric("Unique Sites", df["url"].nunique())

    st.divider()

    category_counts = df["category"].value_counts().reset_index()
    category_counts.columns = ["category", "count"]

    fig = px.pie(category_counts, names="category", values="count")
    st.plotly_chart(fig, use_container_width=True)

# =====================================
# CATEGORY ANALYSIS
# =====================================
elif menu == "Category Analysis":

    st.title("📊 Category Analysis")

    category_counts = df["category"].value_counts().reset_index()
    category_counts.columns = ["category", "count"]

    fig = px.bar(category_counts, x="category", y="count", color="category")
    st.plotly_chart(fig, use_container_width=True)

# =====================================
# TIME ANALYSIS
# =====================================
elif menu == "Time Analysis":

    st.title("⏰ Time Analysis")

    df["date"] = df["timestamp"].dt.date
    time_data = df.groupby(["date", "category"]).size().reset_index(name="count")

    fig = px.line(time_data, x="date", y="count", color="category")
    st.plotly_chart(fig, use_container_width=True)

# =====================================
# AI INSIGHTS
# =====================================
elif menu == "AI Insights":

    st.title("🤖 Smart Insights")

    insights = generate_insights(df)

    for ins in insights:
        st.success(ins)

# =====================================
# RAW DATA
# =====================================
elif menu == "Raw Data":

    st.title("📄 Raw Data")
    st.dataframe(df.head(100))

# =====================================
# STYLE
# =====================================
st.markdown("""
    <style>
        .stMetric {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)