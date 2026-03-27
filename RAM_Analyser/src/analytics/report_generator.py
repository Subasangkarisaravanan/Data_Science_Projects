import os
import pandas as pd
from fpdf import FPDF

print("\n================================================")
print("GENERATING PROJECT REPORT")
print("================================================\n")

# -------------------------------------------------
# BASE PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_history.csv")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
OUTPUT_FILE = os.path.join(BASE_DIR, "RAM_Analysis_Report.pdf")

# -------------------------------------------------
# SAFE TEXT (fix unicode issue)
# -------------------------------------------------
def safe_text(text):
    return str(text).encode("latin-1", "replace").decode("latin-1")

# -------------------------------------------------
# CHECK FILE EXISTS
# -------------------------------------------------
if not os.path.exists(DATA_PATH):
    print("❌ Cleaned data not found!")
    print("👉 Run clean_history.py first")
    exit()

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_csv(DATA_PATH)

# Ensure timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df.dropna(subset=["timestamp"], inplace=True)

# -------------------------------------------------
# BASIC STATS
# -------------------------------------------------
category_counts = df["category"].value_counts()

top_category = category_counts.idxmax() if len(category_counts) > 0 else "N/A"
top_count = category_counts.max() if len(category_counts) > 0 else 0
top_website = df["url"].value_counts().idxmax() if len(df) > 0 else "N/A"

# -------------------------------------------------
# ADVANCED INSIGHTS
# -------------------------------------------------

# ⏰ Peak Usage Time
df["hour"] = df["timestamp"].dt.hour
peak_hour = df["hour"].value_counts().idxmax()

if peak_hour < 12:
    peak_time = f"{peak_hour} AM"
elif peak_hour == 12:
    peak_time = "12 PM"
else:
    peak_time = f"{peak_hour-12} PM"

# 🌐 Top Sites
top_sites = df["url"].value_counts().head(3).index.tolist()

# 💻 High RAM sites (approx)
high_ram_keywords = ["youtube", "netflix", "primevideo", "hotstar"]
high_ram_sites = set()

for url in df["url"]:
    for kw in high_ram_keywords:
        if kw in str(url).lower():
            high_ram_sites.add(kw)

# 🐢 Slow/Hanging sites (approx)
slow_sites = df["url"].value_counts()
slow_sites = slow_sites[slow_sites > 10].index.tolist()[:3]

# -------------------------------------------------
# BUILD INSIGHTS LIST
# -------------------------------------------------
insights = []

insights.append(f"Most used category: {top_category} ({top_count} visits)")
insights.append(f"Most visited website: {top_website}")
insights.append(f"Peak browsing time is around {peak_time}")
insights.append(f"Top visited sites: {', '.join(top_sites)}")

if len(high_ram_sites) > 0:
    insights.append(f"High RAM usage sites detected: {', '.join(high_ram_sites)}")

if len(slow_sites) > 0:
    insights.append(f"Frequently accessed (possibly slow/heavy) sites: {', '.join(slow_sites)}")

if top_category == "Entertainment":
    insights.append("High entertainment usage detected. Consider reducing screen time.")

if "Learning" in category_counts:
    insights.append("Learning activity detected. Good productivity habit.")

if "Shopping" in category_counts:
    insights.append("Frequent shopping activity observed.")

if "Work" in category_counts:
    insights.append("Work-related usage detected.")

if "Personal" in category_counts:
    insights.append("Personal usage detected (mail/banking).")

# -------------------------------------------------
# CREATE PDF
# -------------------------------------------------
pdf = FPDF()
pdf.add_page()

# Title
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, safe_text("RAM Browsing Behaviour Analysis Report"), ln=True, align="C")

pdf.ln(10)

# Description
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 8, safe_text(
    "This report summarizes browsing behaviour patterns, peak activity times, and system usage insights."
))

pdf.ln(5)

# Summary
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, safe_text("Summary"), ln=True)

pdf.set_font("Arial", size=12)
pdf.cell(200, 10, safe_text(f"Total Records: {len(df)}"), ln=True)
pdf.cell(200, 10, safe_text(f"Top Category: {top_category}"), ln=True)
pdf.cell(200, 10, safe_text(f"Top Website: {top_website}"), ln=True)

pdf.ln(5)

# Insights
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, safe_text("AI Insights"), ln=True)

pdf.set_font("Arial", size=12)

for ins in insights:
    pdf.multi_cell(0, 8, safe_text(f"- {ins}"))

pdf.ln(5)

# -------------------------------------------------
# ADD PLOTS
# -------------------------------------------------
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, safe_text("Generated Plots"), ln=True)

if os.path.exists(PLOTS_DIR):

    plots = os.listdir(PLOTS_DIR)

    if len(plots) == 0:
        pdf.cell(200, 10, safe_text("No plots found"), ln=True)

    for plot in plots:
        path = os.path.join(PLOTS_DIR, plot)

        pdf.add_page()

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, safe_text(plot), ln=True)

        try:
            pdf.image(path, x=10, y=30, w=180)
        except:
            pdf.cell(200, 10, safe_text("Error loading image"), ln=True)

else:
    pdf.cell(200, 10, safe_text("Plots folder not found"), ln=True)

# -------------------------------------------------
# SAVE
# -------------------------------------------------
pdf.output(OUTPUT_FILE)

print("✅ Report successfully generated!")
print("📄 File location:")
print(OUTPUT_FILE)