import pandas as pd
import random
import os

# === Template path ===
template_path = r"C:\Users\Admin\Downloads\EXCEL BATCH REPORT  07.06.2025.xlsx"
output_folder = r"C:\Users\Admin\Downloads\Generated_Bills"

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# === Load template ===
df = pd.read_excel(template_path, header=None)

# === Define column indexes based on your structure ===
# Adjust indices if columns differ (index starts at 0)
COL_40MM = 0       # 40MM
COL_M_SA = 2       # M SA
COL_CEM2 = 7       # CEM2
COL_WATER = 10     # WATER

# === Define value ranges ===
RANGE_40MM = (1439, 1445)
RANGE_M_SA = (523, 530)
RANGE_CEM2 = (3671, 3674)
RANGE_WATER = (133, 140)

# === Function to modify values ===
def modify_values(df):
    df_copy = df.copy()
    # Modify only numeric rows where the first few columns contain numbers
    for i in range(len(df_copy)):
        row = df_copy.iloc[i]
        try:
            # Check if row contains numeric data in first column
            if pd.api.types.is_number(row[COL_40MM]):
                df_copy.iat[i, COL_40MM] = random.randint(*RANGE_40MM)
                df_copy.iat[i, COL_M_SA] = random.randint(*RANGE_M_SA)
                df_copy.iat[i, COL_CEM2] = random.randint(*RANGE_CEM2)
                df_copy.iat[i, COL_WATER] = random.randint(*RANGE_WATER)
        except:
            continue
    return df_copy

# === Generate 10 random bills ===
for n in range(1, 11):
    modified_df = modify_values(df)
    output_path = os.path.join(output_folder, f"Billing_{n:02}.xlsx")
    modified_df.to_excel(output_path, index=False, header=False)
    print(f"✅ Bill {n} saved at: {output_path}")

print("\nAll 10 Excel billing files generated successfully!")
