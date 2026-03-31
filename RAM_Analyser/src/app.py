import streamlit as st
import pandas as pd
import psutil
import time
import sys
import os

from config.paths import CLEAN_HISTORY, INSIGHTS_FILE, REPORT_FILE

st.set_page_config(page_title="RAM Analyzer", layout="wide")
# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    return pd.read_csv(CLEAN_HISTORY)

@st.cache_data
def load_insights():
    try:
        with open(INSIGHTS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except:
        return []

df = load_data()
insights_list = load_insights()

# =========================================================
# PREPROCESS
# =========================================================
df["domain"] = df["url"].apply(
    lambda x: str(x).split("/")[2] if "://" in str(x) else str(x)
)

if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df.dropna(subset=["timestamp"], inplace=True)
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day_name()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("🔧 Filters")

if "date" in df.columns:
    start_date = st.sidebar.date_input("Start Date", df["date"].min())
    end_date = st.sidebar.date_input("End Date", df["date"].max())
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

if "category" in df.columns:
    categories = df["category"].dropna().unique()
    selected_categories = st.sidebar.multiselect(
        "Category", categories, default=categories
    )
    df = df[df["category"].isin(selected_categories)]

search_term = st.sidebar.text_input("🔍 Search URL")
if search_term:
    df = df[df["url"].str.contains(search_term, case=False, na=False)]

if "domain" in df.columns:
    top_domains = df["domain"].value_counts().head(20).index.tolist()
    selected_domains = st.sidebar.multiselect("🌐 Domains", top_domains)
    if selected_domains:
        df = df[df["domain"].isin(selected_domains)]

# =========================================================
# HEADER
# =========================================================
st.title("🧠 User Behavior Analytics Dashboard")

if len(df) == 0:
    st.warning("No data after filtering")
    st.stop()

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Trends",
    "🚨 Anomaly",
    "💡 Insights"
])

# =========================================================
# OVERVIEW
# =========================================================
with tab1:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", len(df))
    col2.metric("Categories", df["category"].nunique() if "category" in df.columns else 0)
    col3.metric("Avg Confidence", round(df["confidence"].mean(), 2) if "confidence" in df.columns else 0)
    col4.metric("Top Category", df["category"].value_counts().idxmax() if "category" in df.columns else "N/A")

    st.subheader("📊 Category Distribution")
    if "category" in df.columns:
        st.bar_chart(df["category"].value_counts())

    st.subheader("⏱️ Time Spent per Category")
    if "time_spent" in df.columns:
        st.bar_chart(df.groupby("category")["time_spent"].sum())

    st.subheader("🌐 Top Domains")
    st.bar_chart(df["domain"].value_counts().head(10))

    # ✅ FIXED RAM MONITOR
    st.subheader("💻 Live RAM Usage")

    ram_placeholder = st.empty()
    ram_data = []

    for i in range(10):
        ram = psutil.virtual_memory().percent
        ram_data.append(ram)

        df_ram = pd.DataFrame({
            "Time": list(range(len(ram_data))),
            "RAM": ram_data
        }).set_index("Time")

        ram_placeholder.line_chart(df_ram)
        time.sleep(0.5)

# =========================================================
# TRENDS
# =========================================================
with tab2:

    if "date" in df.columns:
        st.subheader("📅 Daily Activity")
        st.line_chart(df.groupby("date").size())

        st.subheader("📊 Category Trends")
        trend = df.groupby(["date", "category"]).size().unstack().fillna(0)
        st.line_chart(trend)

# =========================================================
# ANOMALY
# =========================================================
with tab3:

    if "confidence" in df.columns:
        threshold = df["confidence"].mean() - df["confidence"].std()
        anomalies = df[df["confidence"] < threshold]

        st.metric("Anomalies Detected", len(anomalies))
        st.bar_chart(df["confidence"])

        if not anomalies.empty:
            st.dataframe(anomalies.head(20))

# =========================================================
# INSIGHTS
# =========================================================
with tab4:

    st.header("🧠 Advanced Behavior Insights")

    category_dist = df["category"].value_counts(normalize=True)

    work = category_dist.get("Work", 0)
    education = category_dist.get("Education", 0)
    entertainment = category_dist.get("Entertainment", 0)
    social = category_dist.get("Social Media", 0)

    productivity_score = round((work + education) * 100, 1)
    st.metric("🎯 Productivity Score", f"{productivity_score}/100")

    # Peak hour safe
    peak_hour = None
    if "hour" in df.columns:
        hourly = df["hour"].value_counts().sort_index()
        st.line_chart(hourly)
        peak_hour = hourly.idxmax()
        st.write(f"Peak Hour: {peak_hour}:00")

    st.subheader("🌐 Top Websites")
    st.bar_chart(df["domain"].value_counts().head(5))

    # Sessions
    if "timestamp" in df.columns:
        df_sorted = df.sort_values("timestamp").copy()
        df_sorted["session"] = (df_sorted["timestamp"].diff().dt.seconds > 1800).cumsum()
        session_sizes = df_sorted.groupby("session").size()

        st.write(f"Short Sessions: {(session_sizes < 5).sum()}")
        st.write(f"Medium Sessions: {((session_sizes >= 5) & (session_sizes < 20)).sum()}")
        st.write(f"Long Sessions: {(session_sizes >= 20).sum()}")

    # Insights from file
    st.subheader("📄 Behavior Insights")
    if insights_list:
        for i, insight in enumerate(insights_list, 1):
            st.success(f"{i}. {insight}")

    # Recommendations
    st.subheader("💡 Smart Recommendations")

    recs = []

    if productivity_score < 40:
        recs.append("Increase productive activities")

    if entertainment > 0.4:
        recs.append("Reduce entertainment usage")

    if social > 0.3:
        recs.append("Limit social media usage")

    if peak_hour is not None:
        recs.append(f"Use peak hour {peak_hour}:00 effectively")

    for i, r in enumerate(recs, 1):
        st.success(f"{i}. {r}")

    # Download report
    st.subheader("📥 Download Report")
    try:
        with open(REPORT_FILE, "rb") as file:
            st.download_button(
                "Download PDF Report",
                data=file,
                file_name="RAM_Report.pdf"
            )
    except:
        st.warning("Report not found")

# =========================================================
# DOWNLOAD DATA
# =========================================================
st.download_button(
    "⬇️ Download Filtered Data",
    data=df.to_csv(index=False),
    file_name="filtered_data.csv"
)
