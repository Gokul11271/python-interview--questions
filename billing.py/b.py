import random
import pandas as pd
from datetime import datetime, timedelta

def generate_bill(batch_num, start_time):
    end_time = start_time + timedelta(minutes=10)

    # Random ranges
    water_abs = random.randint(1439, 1445)
    msa = random.randint(523, 530)
    mm12 = 0
    mm20 = 0
    cem1 = 0
    cem2 = random.randint(367, 374)

    # Constants
    admixture = 1.40
    batch_size = 1.00
    water_target = 150
    others_constant = 0

    # Totals (example calculation based on pattern)
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
        "Total Set Weight (Kg)": total_set_weight,
        "Total Actual (Kg)": total_actual
    }

def generate_bills(n=20):
    bills = []
    base_time = datetime(2024, 6, 14, 8, 24, 0)
    for i in range(n):
        start_time = base_time + timedelta(minutes=i * 10)
        bills.append(generate_bill(i + 1, start_time))
    return bills

# Generate and export
bills = generate_bills(20)
df = pd.DataFrame(bills)
print(df)
df.to_csv("rmc_billing_report.csv", index=False)
print("\n✅ 20 Billing Reports Generated and Saved as 'rmc_billing_report.csv'")
