from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta
import random, os

# Output folder
os.makedirs("RMC_Exact_Bills", exist_ok=True)

styles = getSampleStyleSheet()
title_style = styles["Title"]
normal = styles["Normal"]

def generate_batch_data(batch_no, start_time):
    end_time = start_time + timedelta(minutes=10)

    rows = []
    for _ in range(10):
        water = random.randint(1439, 1445)
        msa = random.randint(523, 530)
        cem2 = random.randint(367, 374)
        row = [0, msa, 0, 0, 0, cem2, 0, water, 0, 0]
        rows.append(row)

    # Totals
    totals_set = [
        sum(r[0] for r in rows),
        sum(r[1] for r in rows),
        sum(r[2] for r in rows),
        sum(r[3] for r in rows),
        sum(r[4] for r in rows),
        sum(r[5] for r in rows),
        sum(r[6] for r in rows),
        sum(r[7] for r in rows),
        sum(r[8] for r in rows),
        sum(r[9] for r in rows),
    ]
    totals_actual = [v + random.randint(-5, 5) for v in totals_set]

    return rows, totals_set, totals_actual, end_time

def create_pdf(batch_no, start_time):
    filename = f"RMC_Exact_Bills/Batch_{batch_no}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=30, bottomMargin=30)
    story = []

    rows, total_set, total_actual, end_time = generate_batch_data(batch_no, start_time)

    # Header
    story.append(Paragraph("<b>SCHWING STETTER</b>", title_style))
    story.append(Paragraph("MCI 370 Control System Ver 3.1", normal))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>VENKATESWARA READY MIX CONCRETE</b>", normal))
    story.append(Paragraph("Docket / Batch Report / Autographic Record", normal))
    story.append(Spacer(1, 8))

    # Batch Info
    info = [
        ["Batch Date", start_time.strftime("%d.%m.%Y"), "Plant Serial Number", "RMC-1"],
        ["Batch Start Time", start_time.strftime("%I:%M:%S %p"), "Batch End Time", end_time.strftime("%I:%M:%S %p")],
        ["Batch Number / Docket Number", f"1575{batch_no}", "Ordered Quantity", "10.00 M³"],
        ["Customer", "K K CONSTRUCTION", "Production Quantity", "10.00 M³"],
        ["Site", "MTP", "Adj/Manual Quantity", "0.00 M³"],
        ["Recipe Code", "3", "With This Load", "10.00 M³"],
        ["Recipe Name", "M30", "Mixer Capacity", "1.00 M³"],
        ["Truck Number", "TN40T8628", "Batch Size", "1.00 M³"],
        ["Truck Driver", "MAHINDRAN", "Order Number", "VBM"],
        ["Batcher Name", "STETTER", "", ""]
    ]
    t = Table(info, colWidths=[130, 120, 130, 120])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke)
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Data table header
    headers = ["40MM","M SA","12MM","20MM","CEM1","CEM2","CEM3","WATER","+/-","ADMIX1"]
    data = [headers] + rows + [["Total Set Weight in Kgs."] + total_set] + [["Total Actual in Kgs."] + total_actual]

    tbl = Table(data, colWidths=[45]*10)
    tbl.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.4, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 10))

    # Footer
    footer_data = [
        ["14.00","0.00"],
        ["1.40","0.00"],
        ["1.40","0.00"],
        ["Aggregate Cement Water Admixture","ADMIX1 -"]
    ]
    footer_tbl = Table(footer_data)
    story.append(footer_tbl)

    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Generated Automatically</b>", styles["Italic"]))
    doc.build(story)
    print(f"✅ Generated {filename}")

# Generate 20 bills
start_time = datetime(2024, 5, 2, 6, 3, 20)
for i in range(20):
    create_pdf(751 + i, start_time + timedelta(minutes=i*10))

print("\n✅ 20 Exact-Template RMC Bills Generated in 'RMC_Exact_Bills/'")
