import os
from fpdf import FPDF

print("\n================================================")
print("GENERATING PROJECT REPORT")
print("================================================\n")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

output_file = os.path.join(BASE_DIR, "RAM_Analysis_Report.pdf")

pdf = FPDF()

pdf.add_page()

pdf.set_font("Arial", size=16)

pdf.cell(200,10,"RAM Browsing Behaviour Analysis Report", ln=True)

pdf.set_font("Arial", size=12)

pdf.ln(10)

pdf.multi_cell(0,8,"This report summarizes browsing behaviour patterns and RAM usage correlation detected by the AI analysis pipeline.")

pdf.ln(5)

pdf.cell(200,10,"Generated Plots:", ln=True)

plots = os.listdir(PLOTS_DIR)

for plot in plots:

    path = os.path.join(PLOTS_DIR, plot)

    pdf.add_page()

    pdf.cell(200,10,plot, ln=True)

    pdf.image(path, x=10, y=30, w=180)

pdf.output(output_file)

print("Report saved:")
print(output_file)