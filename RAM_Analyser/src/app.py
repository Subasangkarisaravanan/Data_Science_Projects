import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(
    page_title="RAM Analyzer Dashboard",
    layout="wide"
)

st.title("🧠 Time-Based Browsing Pattern Analyzer")
st.subheader("Deep Learning + RAM Usage Correlation")

# ------------------------------------------------
# PATHS
# ------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "..", "data")
PLOT_DIR = os.path.join(BASE_DIR, "..", "plots")

features_file = os.path.join(DATA_DIR, "session_features.csv")
clusters_file = os.path.join(DATA_DIR, "session_clusters.csv")
anomaly_file = os.path.join(DATA_DIR, "session_anomalies.csv")
recommend_file = os.path.join(DATA_DIR, "recommendations.txt")
insight_file = os.path.join(DATA_DIR, "behavior_insights.txt")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

if os.path.exists(features_file):
    features = pd.read_csv(features_file)
else:
    features = None

if os.path.exists(clusters_file):
    clusters = pd.read_csv(clusters_file)
else:
    clusters = None

if os.path.exists(anomaly_file):
    anomalies = pd.read_csv(anomaly_file)
else:
    anomalies = None


# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("Navigation")

section = st.sidebar.radio(
    "Select Section",
    [
        "Overview",
        "RAM Analysis",
        "Session Clusters",
        "Anomaly Detection",
        "Behavior Insights",
        "Recommendations",
        "Datasets"
    ]
)

# ------------------------------------------------
# OVERVIEW
# ------------------------------------------------

if section == "Overview":

    st.header("Project Overview")

    st.write(
        """
        This system analyzes browsing behavior and correlates it with RAM usage.

        The pipeline performs:
        - Browser history extraction
        - RAM monitoring
        - Sessionization
        - Clustering
        - Deep learning anomaly detection
        - Recommendation generation
        """
    )

    if features is not None:

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Sessions", len(features))

        col2.metric(
            "Average RAM Usage",
            f"{features['avg_ram'].mean():.2f} MB"
        )

        col3.metric(
            "Average Session Length",
            f"{features['session_length'].mean():.2f}"
        )

# ------------------------------------------------
# RAM ANALYSIS
# ------------------------------------------------

elif section == "RAM Analysis":

    st.header("RAM Usage Analytics")

    plot_files = [
        "ram_by_category.png",
        "ram_vs_complexity.png",
        "ram_vs_pages.png",
        "ram_vs_domains.png",
        "ram_heatmap.png"
    ]

    for p in plot_files:

        path = os.path.join(PLOT_DIR, p)

        if os.path.exists(path):

            st.image(Image.open(path), caption=p)

# ------------------------------------------------
# SESSION CLUSTERS
# ------------------------------------------------

elif section == "Session Clusters":

    st.header("Browsing Session Clusters")

    plot_files = [
        "cluster_session_length_vs_pages.png",
        "cluster_ram_efficiency.png",
        "cluster_pca_visualization.png"
    ]

    for p in plot_files:

        path = os.path.join(PLOT_DIR, p)

        if os.path.exists(path):

            st.image(Image.open(path), caption=p)

    if clusters is not None:

        st.subheader("Cluster Data")

        st.dataframe(clusters.head(20))

# ------------------------------------------------
# ANOMALY DETECTION
# ------------------------------------------------

elif section == "Anomaly Detection":

    st.header("Deep Learning Anomaly Detection")

    if anomalies is not None:

        anomaly_sessions = anomalies[anomalies["is_anomaly"] == True]

        st.metric("Total Anomalies", len(anomaly_sessions))

        st.subheader("Top Anomalous Sessions")

        st.dataframe(
            anomaly_sessions.sort_values(
                "anomaly_score",
                ascending=False
            ).head(20)
        )

# ------------------------------------------------
# BEHAVIOR INSIGHTS
# ------------------------------------------------

elif section == "Behavior Insights":

    st.header("AI Generated Behavioral Insights")

    if os.path.exists(insight_file):

        with open(insight_file) as f:

            lines = f.readlines()

        for l in lines:

            st.write("•", l.strip())

    else:

        st.warning("Behavior insights not found. Run pipeline first.")

# ------------------------------------------------
# RECOMMENDATIONS
# ------------------------------------------------

elif section == "Recommendations":

    st.header("System Recommendations")

    if os.path.exists(recommend_file):

        with open(recommend_file) as f:

            recs = f.readlines()

        for r in recs:

            st.write("•", r.strip())

    else:

        st.warning("Recommendations not found. Run pipeline first.")

# ------------------------------------------------
# DATASETS
# ------------------------------------------------

elif section == "Datasets":

    st.header("Generated Datasets")

    if features is not None:

        st.subheader("Session Features")

        st.dataframe(features.head(20))

    if clusters is not None:

        st.subheader("Cluster Dataset")

        st.dataframe(clusters.head(20))

    if anomalies is not None:

        st.subheader("Anomaly Dataset")

        st.dataframe(anomalies.head(20))