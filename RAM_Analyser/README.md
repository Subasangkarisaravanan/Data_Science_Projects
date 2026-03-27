# 🚀 RAM Browsing Behaviour Analyzer

An AI-powered system that analyzes browser activity and correlates it with RAM usage to detect productivity patterns, anomalies, and system performance issues.

---

## 🔥 Key Features

* 📊 Browser history extraction (Chrome & Edge)
* 🧠 RAM usage monitoring (real-time logging)
* 🧹 Data cleaning & preprocessing
* 🌐 Domain categorization (shopping, entertainment, etc.)
* ⏱️ Session building & behavioral analysis
* 📈 RAM vs browsing correlation analysis
* 🤖 Machine Learning clustering (user behavior segmentation)
* 🧬 Deep Learning anomaly detection (Autoencoder)
* 💡 Smart recommendation engine
* 📊 Interactive Streamlit dashboard (with Plotly visuals)
* 📑 Automated PDF report generation
* 📉 Advanced analytics plots

---

## 🏗️ Project Structure

```
RAM_Analyser/
│
├── src/
│   ├── app.py                  # Streamlit dashboard
│   ├── collect/               # Data collection
│   ├── analytics/             # Insights & reports
│   ├── models/                # ML & DL models
│
├── data/                      # Raw & processed datasets
├── plots/                     # Generated visualizations
├── run_pipeline.py            # Full automation script
├── requirements.txt
├── README.md
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Full Pipeline

```bash
python run_pipeline.py
```

This executes:

1. Browser history extraction
2. RAM logging
3. Data cleaning
4. Session building
5. RAM correlation analysis
6. Feature engineering
7. Clustering
8. Anomaly detection (Autoencoder)
9. Recommendation generation

---

## 📊 Run Dashboard

```bash
streamlit run src/app.py
```

---

## 📂 Outputs

### 📁 Generated Data

* browsing_history_clean.csv
* browsing_sessions.csv
* ram_log.csv
* session_features.csv
* session_clusters.csv
* session_anomalies.csv

### 📈 Generated Plots

* RAM vs time
* RAM vs domains
* Category-wise RAM usage
* Cluster visualizations
* CPU vs RAM correlation

### 📑 Report

* RAM_Analysis_Report.pdf

---

## 🎯 Use Cases

* Employee productivity tracking
* Digital wellbeing monitoring
* System performance optimization
* Behavioral anomaly detection

---

## 🛠️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* TensorFlow (Deep Learning)
* Streamlit (Dashboard)
* Plotly (Interactive charts)
* Matplotlib & Seaborn (Visualization)

---

## 👤 Author

RAM Behaviour Analytics Project
