# st = input("Enter the string: ")
# for i in st:
#   if not (('a' <= i <= 'z') or ('A' <= i <= 'Z') or ('0' <= i <= '9')):
#     print(i,end="")

import urllib.request

with urllib.request.urlopen("https://www.sparshdesigners.com/") as resp:
	page_bytes = resp.read()
	page_text = page_bytes.decode('utf-8', errors='replace')
	print(resp.getcode())
	print(page_text[:500])
	

import pandas as pd
import matplotlib.pyplot as plt

# load the 'tips' dataset from seaborn's public repo without requiring seaborn
tips_url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
tips = pd.read_csv(tips_url)

# compute mean total_bill per day and plot with matplotlib
mean_bills = tips.groupby("day")["total_bill"].mean()
days = mean_bills.index.tolist()
values = mean_bills.values.tolist()

plt.bar(days, values)
plt.xlabel("day")
plt.ylabel("average total_bill")
plt.title("Average total bill by day")
plt.show()

