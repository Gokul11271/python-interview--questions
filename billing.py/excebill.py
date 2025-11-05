from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from datetime import datetime, timedelta
import random
import os

OUT_DIR = "RMC_Exact_Bills"
os.makedirs(OUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('title', parent=styles['Title'], alignment=1, fontSize=14, leading=16)
small_center = ParagraphStyle('small_center', parent=styles['Normal'], alignment=1, fontSize=8)
left = ParagraphStyle('left', parent=styles['Normal'], alignment=0, fontSize=9)

# Configuration for ranges
RANGE_WATER = (1439, 1445)
RANGE_MSA = (523, 530)
RANGE_CEM2 = (367, 374)

# Column headers and widths
COL_HEADERS = ["40MM", "M SA", "12MM", "20MM", "CEM1", "CEM2", "CEM3", "WATER", "+/-", "ADMIX1"]
COL_WIDTHS = [28*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm, 20*mm, 30*mm]

def build_top_info(batch_number, start_time, end_time):
    dt = start_time.strftime("%d.%m.%Y")
    info = [
        ["MCI 370 Control System Ver 3.1", "", "", ""],
        ["", "", "", ""],
        ["Batch Date", dt, "Plant Serial Number :", "RMC-1"],
        ["Batch Start Time", start_time.strftime("%I:%M:%S %p"), "Batch End Time", end_time.strftime("%I:%M:%S %p")],
        ["Batch Number / Docket Number", f"{batch_number}", "Ordered Quantity", "10.00 M³"],
        ["Customer", "K K CONSTRUCTION", "Production Quantity", "10.00 M³"],
        ["Site", "MTP", "Adj/Manual Quantity", "0.00 M³"],
        ["Recipe Code", "3", "With This Load", "10.00 M³"],
        ["Recipe Name", "M30", "Mixer Capacity", "1.00 M³"],
        ["Truck Number", "TN40T8628", "Batch Size", "1.00 M³"],
        ["Truck Driver", "MAHINDRAN", "Order Number", "VBM"],
        ["Batcher Name", "STETTER", "", ""],
    ]
    return info

def generate_10_rows():
    # Each row corresponds to one measurement line (like water/moisture lines)
    rows = []
    for _ in range(10):
        val_40mm = 0
        val_msa = random.randint(*RANGE_MSA)
        val_12mm = 0
        val_20mm = 0
        val_cem1 = 0
        val_cem2 = random.randint(*RANGE_CEM2)
        val_cem3 = 0
        val_water = random.randint(*RANGE_WATER)
        val_plusminus = 0
        val_admix1 = 0
        rows.append([val_40mm, val_msa, val_12mm, val_20mm, val_cem1, val_cem2, val_cem3, val_water, val_plusminus, val_admix1])
    return rows

def sum_columns(rows):
    totals = [sum(row[i] for row in rows) for i in range(len(COL_HEADERS))]
    return totals

def make_pdf_for_batch(batch_number, start_time):
    end_time = start_time + timedelta(minutes=10)
    filename = os.path.join(OUT_DIR, f"Batch_{batch_number}.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=15*mm, bottomMargin=12*mm)
    story = []

    # Header area (company title centered)
    story.append(Paragraph("SCHWING", title_style))
    story.append(Paragraph("Stetter", small_center))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>VENKATESWARA READY MIX CONCRETE</b>", ParagraphStyle('h', parent=styles['Heading2'], alignment=1, fontSize=12)))
    story.append(Paragraph("Docket / Batch Report / Autographic Record", small_center))
    story.append(Spacer(1, 6))

    # Top info table
    top_info = build_top_info(batch_number, start_time, end_time)
    top_tbl = Table(top_info, colWidths=[45*mm, 55*mm, 45*mm, 55*mm], hAlign='LEFT')
    top_tbl.setStyle(TableStyle([
        ('SPAN', (0,0), (3,0)),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOX', (0,2), (-1,11), 0.4, colors.black),
        ('INNERGRID', (0,2), (-1,11), 0.25, colors.black),
    ]))
    story.append(top_tbl)
    story.append(Spacer(1, 8))

    # Data table: headers + 10 rows + totals rows
    rows = generate_10_rows()
    totals_set = sum_columns(rows)
    # Total actual = totals_set + small random variation per column
    totals_actual = [totals_set[i] + random.randint(-10, 10) for i in range(len(totals_set))]

    data = []
    data.append(COL_HEADERS)
    # Add the 10 measurement rows (these correspond to "Water Abs(%) / Moisture (%)" lines)
    for r in rows:
        data.append(r)
    # Blank spacer row
    data.append([""] * len(COL_HEADERS))
    # Totals rows (as in PDF: "Total Set Weight in Kgs." and "Total Actual in Kgs.")
    data.append(["Total Set Weight in Kgs."] + totals_set[1:])  # put label in first col, rest totals
    data.append(["Total Actual in Kgs."] + totals_actual[1:])

    tbl = Table(data, colWidths=COL_WIDTHS, hAlign='CENTER')
    tbl_style = TableStyle([
        ('GRID', (0,0), (-1,-1), 0.35, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('SPAN', (0, len(rows)+1), (0, len(rows)+1)),  # label row span handled below by writing text in first cell
        ('BACKGROUND', (0, len(rows)+1), (-1, len(rows)+1), colors.whitesmoke),
        ('BACKGROUND', (0, len(rows)+2), (-1, len(rows)+2), colors.whitesmoke),
    ])
    tbl.setStyle(tbl_style)

    # Fix the totals rows: Table expects same number of columns on each row; we placed label in first cell and totals in others.
    story.append(tbl)
    story.append(Spacer(1, 8))

    # Footer block — mimic excel footer lines (aggregate/cement/water/admixture) and some repeated small lines as in sample
    footer_lines = [
        ["Aggregate", "Cement", "Water", "Admixture", ""],
        ["ADMIX1 -", "", "", "", ""],
        ["Generated Automatically", "", "", "", ""]
    ]
    footer_tbl = Table(footer_lines, colWidths=[50*mm, 40*mm, 40*mm, 40*mm, 20*mm], hAlign='LEFT')
    footer_tbl.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('SPAN', (0,2), (4,2)),
        ('ALIGN', (0,2), (4,2), 'LEFT'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(footer_tbl)

    # add a short footer area for docket info and final spacing
    story.append(Spacer(1,6))
    story.append(Paragraph(f"Docket / Batch Report - Generated for Batch {batch_number}", left))
    story.append(Spacer(1,4))

    doc.build(story)
    print(f"Created: {filename}")

def main():
    # Base start time taken from your sample (05.02.2024 06:03:20 AM)
    base_time = datetime(2024, 2, 5, 6, 3, 20)
    start_batch_no = 15752  # as in your sample
    total_bills = 20

    for i in range(total_bills):
        batch_no = start_batch_no + i
        start_time = base_time + timedelta(minutes=10 * i)
        make_pdf_for_batch(batch_no, start_time)

    print("\n✅ All PDFs generated in folder:", OUT_DIR)

if __name__ == "__main__":
    main()
