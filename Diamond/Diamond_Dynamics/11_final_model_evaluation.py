# ==========================================================
# 💎 DIAMOND DYNAMICS PROJECT
# FILE: 11_final_model_evaluation.py
# STEP 13 – FINAL MODEL & BUSINESS EVALUATION
# ==========================================================

import os
import pandas as pd
import numpy as np

os.makedirs("data", exist_ok=True)

print("\n" + "=" * 80)
print("STEP 13: FINAL MODEL & BUSINESS EVALUATION")
print("=" * 80)

# ----------------------------------------------------------
# Load Regression Results
# ----------------------------------------------------------
regression_results = pd.read_csv("data/regression_model_results.csv")

print("\nRegression Model Comparison:")
print(regression_results.sort_values(by="R2", ascending=False))

# ----------------------------------------------------------
# Identify Best Regression Model
# ----------------------------------------------------------
best_model_row = regression_results.sort_values(
    by="R2",
    ascending=False
).iloc[0]

best_model_name = best_model_row["Model"]
best_r2 = best_model_row["R2"]

print("\nBest Regression Model:")
print(f"Model: {best_model_name}")
print(f"R2 Score: {best_r2:.4f}")

# ----------------------------------------------------------
# Load Segmentation Summary
# ----------------------------------------------------------
segment_summary = pd.read_csv("data/segment_business_summary.csv")

print("\nMarket Segment Summary:")
print(segment_summary)

# ----------------------------------------------------------
# Business Insights Extraction
# ----------------------------------------------------------
highest_segment = segment_summary.sort_values(
    by="price_usd",
    ascending=False
).iloc[0]["Segment"]

lowest_segment = segment_summary.sort_values(
    by="price_usd",
    ascending=True
).iloc[0]["Segment"]

print("\nBusiness Insights:")
print(f"Highest Revenue Segment: {highest_segment}")
print(f"Lowest Revenue Segment: {lowest_segment}")

# ----------------------------------------------------------
# Final Recommendation
# ----------------------------------------------------------
print("\nFINAL RECOMMENDATION:")
print(f"""
1. Best Price Prediction Model:
   → {best_model_name} with R² = {best_r2:.4f}

2. ANN Performance:
   → Strong performance but slightly below best tree-based model.
   → Suitable for complex nonlinear modeling.

3. Market Segmentation:
   → Four distinct segments identified:
       - Budget
       - Mid-Range
       - Premium
       - Luxury

4. Strategic Insight:
   → Luxury and Premium segments contribute the highest average pricing.
   → Budget segment captures high-volume market.
""")

# ----------------------------------------------------------
# Save Final Summary Report
# ----------------------------------------------------------
final_report = {
    "Best_Model": best_model_name,
    "Best_R2": best_r2,
    "Highest_Segment": highest_segment,
    "Lowest_Segment": lowest_segment
}

final_report_df = pd.DataFrame([final_report])
final_report_df.to_csv("data/final_project_summary.csv", index=False)

print("\nFinal project summary saved to:")
print("data/final_project_summary.csv")

print("\nSTEP 13 COMPLETED SUCCESSFULLY!")
print("=" * 80)