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
