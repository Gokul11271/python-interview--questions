# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import gaussian_kde  

# data = np.random.randn(500) 


# plt.hist(data,                # Data to plot
#          bins=20,             # Number of bins
#          color='skyblue',     # Color of bars
#          edgecolor='black',   # Border color of bars
#          density=True,        # Normalize to form a probability density
#          label='Histogram')   # Label for legend


# density = gaussian_kde(data)                 
# x = np.linspace(min(data), max(data), 200)  
# plt.plot(x, density(x), color='red', label='Density Curve')  

# plt.title("Data Distribution")
# plt.xlabel("Value")
# plt.ylabel("Frequency / Density")
# plt.legend()
# plt.show()







import matplotlib.pyplot as plt

# Data for plots
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# 1️⃣ Line Plot
plt.figure(figsize=(8, 4))
plt.plot(x, y, color='blue', marker='o')
plt.title("Line Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()

# 2️⃣ Bar Plot
plt.figure(figsize=(8, 4))
plt.bar(x, y, color='orange')
plt.title("Bar Plot")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.show()



# Sample AI-Powered SEO System (Simplified)

import pandas as pd
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer, util
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# 1. Load sample dataset
data = pd.DataFrame({
    "keyword": ["bridal couture", "designer sarees", "luxury boutique"],
    "page_url": ["page1.html", "page2.html", "page3.html"]
})

# 2. Split dataset: 70% train, 15% val, 15% test
train, temp = train_test_split(data, test_size=0.3, random_state=42)
val, test = train_test_split(temp, test_size=0.5, random_state=42)

# 3. Semantic Keyword Embeddings (BERT)
bert_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = bert_model.encode(train['keyword'].tolist(), convert_to_tensor=True)

# Sample similarity
sim = util.pytorch_cos_sim(embeddings[0], embeddings[1])
print(f"Keyword similarity: {sim.item():.4f}")

# 4. GPT-based Meta Description
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def generate_meta(keyword):
    prompt = f"SEO meta description for: '{keyword}'"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=40)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Generate meta for sample keywords
for kw in train['keyword']:
    print(f"Keyword: {kw}")
    print(f"Meta: {generate_meta(kw)}\n")

# 5. Placeholder for crawling & APIs
def crawl_site(url): print(f"Crawling {url}... [sample]")
def fetch_backlinks(keyword): print(f"Fetching backlinks for '{keyword}'... [sample]")
def fetch_performance(page): print(f"Fetching performance for {page}... [sample]")

# Sample workflow
for _, row in train.iterrows():
    crawl_site(row['page_url'])
    fetch_backlinks(row['keyword'])
    fetch_performance(row['page_url'])
