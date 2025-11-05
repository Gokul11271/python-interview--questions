import openpyxl
from openpyxl import Workbook
import random
import os

# === Save location ===
output_folder = r"C:\Users\Admin\Downloads\Generated_Bills"
os.makedirs(output_folder, exist_ok=True)

# === Ranges and constants ===
RANGE_40MM = (1439, 1445)
RANGE_M_SA = (523, 530)
RANGE_CEM2 = (3671, 3674)
RANGE_WATER = (133, 140)
ADMIX1_VALUE = 1.40

# === Columns ===
columns = ["40MM", "M SA", "CEM2", "WATER", "ADMIX1"]

def create_bill(filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bill Report"

    # === Header Section ===
    ws.append(columns)
    ws.append([])

    # === Data rows ===
    data_rows = []
    for _ in range(10):  # 10 data rows
        row = [
            random.randint(*RANGE_40MM),  # 40MM
            random.randint(*RANGE_M_SA),  # M SA
            random.randint(*RANGE_CEM2),  # CEM2
            random.randint(*RANGE_WATER),  # WATER
            ADMIX1_VALUE,                 # ADMIX1
        ]
        ws.append(row)
        data_rows.append(row)

    # === Add Total Row ===
    total_row = ["Total"]
    # Sum each numeric column
    for col_idx in range(1, len(columns)):
        col_values = [r[col_idx] for r in data_rows if isinstance(r[col_idx], (int, float))]
        total_sum = sum(col_values)
        total_row.append(round(total_sum, 2))

    # Add the total row
    ws.append([])
    ws.append(total_row)

    # === Adjust column widths ===
    for col in ws.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 3

    wb.save(filename)
    wb.close()


# === Generate 2 Excel sheets ===
for i in range(1, 3):
    filename = os.path.join(output_folder, f"Bill_{i:02}.xlsx")
    create_bill(filename)
    print(f"✅ Generated: {filename}")

print("\n🎯 Successfully created 2 Excel bills with correct total row (ADMIX1 = 14.00).")
