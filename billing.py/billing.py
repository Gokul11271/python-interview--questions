from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta
import random
import os

# === SETTINGS ===
OUTPUT_FOLDER = "RMC_Bills"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === GENERATE RANDOM BILL DATA ===
def generate_bill_data(batch_num, start_time):
    end_time = start_time + timedelta(minutes=10)

    water_abs = random.randint(1439, 1445)
    msa = random.randint(523, 530)
    mm12 = 0
    mm20 = 0
    cem1 = 0
    cem2 = random.randint(367, 374)
    admixture = 1.40
    water_target = 150
    total_set_weight = 7380 + msa - 820
    total_actual = total_set_weight + random.randint(-10, 10)

    return {
        "Batch Number": f"153{batch_num}",
        "Batch Date": start_time.strftime("%d-%b-%Y"),
        "Start Time": start_time.strftime("%I:%M:%S %p"),
        "End Time": end_time.strftime("%I:%M:%S %p"),
        "M SA": msa,
        "12MM": mm12,
        "20MM": mm20,
        "CEM1": cem1,
        "CEM2": cem2,
        "Water Abs(%)": water_abs,
        "Water Target": water_target,
        "Admixture": admixture,
        "Total Set Weight": total_set_weight,
        "Total Actual": total_actual
    }

# === GENERATE PDF BILL ===
def create_pdf(bill):
    filename = os.path.join(OUTPUT_FOLDER, f"RMC_Bill_{bill['Batch Number']}.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Header
    story.append(Paragraph("<b>VENKATESWARA READY MIX CONCRETE</b>", styles['Title']))
    story.append(Paragraph("MCI 370 Control System Ver 3.1", styles['Normal']))
    story.append(Spacer(1, 8))

    # Batch info
    info_data = [
        ["Batch Date:", bill["Batch Date"], "Batch Number:", bill["Batch Number"]],
        ["Batch Start Time:", bill["Start Time"], "Batch End Time:", bill["End Time"]],
        ["Customer:", "KK CONSTRUCTION", "Site:", "METTUPALAYAM"],
        ["Recipe Code:", "3", "Recipe Name:", "M30"],
        ["Truck Number:", "TN40T8628", "Truck Driver:", "MAHENDRAN"]
    ]
    info_table = Table(info_data, hAlign='LEFT', colWidths=[100, 150, 100, 150])
    story.append(info_table)
    story.append(Spacer(1, 12))

    # Material Table
    data = [
        ["Aggregate", "M SA", "12MM", "20MM", "CEM1", "CEM2", "Water", "Admixture"],
        ["Target (Kgs)", bill["M SA"], bill["12MM"], bill["20MM"], bill["CEM1"], bill["CEM2"], bill["Water Target"], bill["Admixture"]],
        ["Actual (Kgs)", bill["M SA"], bill["12MM"], bill["20MM"], bill["CEM1"], bill["CEM2"], bill["Water Abs(%)"], bill["Admixture"]],
    ]

    table = Table(data, hAlign='CENTER', colWidths=[80]*8)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.8, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    # Totals
    totals_data = [
        ["Total Set Weight (Kgs):", f"{bill['Total Set Weight']}"],
        ["Total Actual (Kgs):", f"{bill['Total Actual']}"]
    ]
    totals_table = Table(totals_data, colWidths=[200, 100])
    totals_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    story.append(totals_table)

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Generated Automatically</b>", styles['Italic']))
    doc.build(story)
    print(f"✅ Created {filename}")

# === MAIN EXECUTION ===
def generate_all_bills(n=20):
    base_time = datetime(2024, 6, 14, 8, 24, 0)
    for i in range(n):
        start_time = base_time + timedelta(minutes=i * 10)
        bill = generate_bill_data(i + 1, start_time)
        create_pdf(bill)

generate_all_bills(20)
print("\n✅ All 20 PDF bills generated inside the 'RMC_Bills' folder.")
