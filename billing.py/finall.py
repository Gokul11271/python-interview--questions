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
RANGE_CEM2 = (367, 374)
RANGE_WATER = (133, 140)
ADMIX1_VALUE = 1.40

# === Columns ===
columns = ["40MM ","0","12MM","20MM","0","M SA","CEM1", "CEM2","CEM3","0", "WATER","0", "ADMIX1","0.00"]
columns = ["Targets based on batchsize in"]

# === Create workbook ===
wb = Workbook()
ws = wb.active
ws.title = "Bill Report"

current_row = 1

# === Generate 230 sets ===
for set_num in range(1, 231):  # 230 sets
    ws.append([f"Set {set_num}"])
    ws.append(columns)

    data_rows = []
    for _ in range(10):  # 10 data rows per set
        row = [
            random.randint(*RANGE_40MM),
            0,
            random.randint(*RANGE_M_SA),
            0,
            0,
            0,
            0,
            random.randint(*RANGE_CEM2),
            0,
            0,
            random.randint(*RANGE_WATER),
            0,
            ADMIX1_VALUE,
            0.00,
        ]  
        ws.append(row)
        data_rows.append(row)

    # === Total Row ===
    total_row = ["Total"]
    for col_idx in range(1, len(columns)):
        col_values = [r[col_idx] for r in data_rows if isinstance(r[col_idx], (int, float))]
        total_sum = sum(col_values)
        total_row.append(round(total_sum, 2))

    ws.append([])
    ws.append(total_row)
    ws.append([])  # Blank line between sets

# === Adjust column widths ===
for col in ws.columns:
    max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
    ws.column_dimensions[col[0].column_letter].width = max_length + 3

# === Save file ===
filename = os.path.join(output_folder, "All_Bills_230_Sets.xlsx")
wb.save(filename)
wb.close()

print(f"✅ Successfully created single Excel file with 230 sets at:\n{filename}")
