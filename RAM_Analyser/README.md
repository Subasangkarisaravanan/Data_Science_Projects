# RAM Browsing Behaviour Analyzer

AI system that analyzes browsing history patterns and correlates them with RAM usage to identify productivity behaviour, anomalies and system performance patterns.

## Features

- Browser history extraction from Chrome and Edge
- RAM usage monitoring
- URL cleaning and domain categorization
- Session building and browsing behavior analysis
- RAM usage correlation with browsing activity
- Machine learning clustering of browsing sessions
- Deep learning anomaly detection using autoencoder
- Recommendation engine for productivity and system optimization
- Streamlit dashboard visualization
- Automated analytics plots
- Automated PDF report generation

## Project Structure

RAM_Analyser

src/
collect/
history_extractor.py
ram_logger.py
active_tab_tracker.py

prep/
clean_history.py
session_builder.py

analytics/
ram_correlation.py
recommendation_engine.py
report_generator.py

models/
session_features.py
session_clustering.py
autoencoder_model.py

app.py

data/

plots/

run_pipeline.py

## Installation

Install dependencies

pip install pandas numpy matplotlib seaborn scikit-learn tensorflow psutil streamlit fpdf pywin32

## Run Pipeline

python run_pipeline.py

This will execute:

1 Browser history extraction  
2 RAM logging  
3 Data preprocessing  
4 Session building  
5 RAM correlation analysis  
6 Feature engineering  
7 Clustering  
8 Deep learning anomaly detection  
9 Recommendation generation  

## Run Dashboard

streamlit run src/app.py

## Output

Datasets generated

browsing_history_raw.csv  
browsing_history_clean.csv  
browsing_sessions.csv  
ram_log.csv  
session_features.csv  
session_clusters.csv  
session_anomalies.csv  

Plots generated

RAM vs browsing complexity  
RAM vs domains  
Cluster visualization  

Report

RAM_Analysis_Report.pdf

## Use Cases

- Employee productivity analytics
- Digital wellbeing monitoring
- RAM usage optimization
- Behavioral anomaly detection

## Author

RAM Behaviour Analytics Project