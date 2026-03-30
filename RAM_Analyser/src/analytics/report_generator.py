import os
import pandas as pd
from fpdf import FPDF

# ✅ IMPORT CENTRAL PATHS (IMPORTANT)
from src.config.paths import CLEAN_HISTORY, PLOTS_DIR, REPORT_FILE

print("\n================================================")
print("GENERATING PROJECT REPORT")
print("================================================\n")

# -------------------------------------------------
# SAFE TEXT
# -------------------------------------------------
def safe_text(text):
    return str(text).encode("latin-1", "replace").decode("latin-1")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
if not os.path.exists(CLEAN_HISTORY):
    print("❌ Cleaned data not found!")
    exit()

df = pd.read_csv(CLEAN_HISTORY)

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
df["hour"] = df["timestamp"].dt.hour
peak_hour = df["hour"].value_counts().idxmax()

peak_time = f"{peak_hour}:00"

top_sites = df["url"].value_counts().head(3).index.tolist()

high_ram_keywords = ["youtube", "netflix", "primevideo", "hotstar"]
high_ram_sites = set()

for url in df["url"]:
    for kw in high_ram_keywords:
        if kw in str(url).lower():
            high_ram_sites.add(kw)

# -------------------------------------------------
# BUILD INSIGHTS
# -------------------------------------------------
insights = [
    f"Most used category: {top_category} ({top_count} visits)",
    f"Most visited website: {top_website}",
    f"Peak browsing time: {peak_time}",
    f"Top visited sites: {', '.join(top_sites)}"
]

if high_ram_sites:
    insights.append(f"High RAM usage sites: {', '.join(high_ram_sites)}")

# -------------------------------------------------
# CREATE PDF
# -------------------------------------------------
pdf = FPDF()
pdf.add_page()

pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, safe_text("RAM Behaviour Analysis Report"), ln=True, align="C")

pdf.ln(10)

pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 8, safe_text(
    "This report summarizes browsing behaviour, productivity, and system usage insights."
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
pdf.cell(200, 10, safe_text("Insights"), ln=True)

pdf.set_font("Arial", size=12)
for ins in insights:
    pdf.multi_cell(0, 8, safe_text(f"- {ins}"))

pdf.ln(5)

# -------------------------------------------------
# 🔥 ADD PLOTS (FIXED)
# -------------------------------------------------
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, safe_text("Visual Analysis"), ln=True)

if os.path.exists(PLOTS_DIR):

    plots = [p for p in os.listdir(PLOTS_DIR) if p.endswith((".png", ".jpg"))]

    if not plots:
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
pdf.output(REPORT_FILE)

print("\n================================================")
print("✅ REPORT GENERATED SUCCESSFULLY")
print("================================================")

print("📄 File:", REPORT_FILE)