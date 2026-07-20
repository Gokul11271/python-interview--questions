import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# -----------------------------
# Load Dataset
# -----------------------------
file_path = r"C:\Users\Admin\Downloads\product+classification+and+clustering\pricerunner_aggregate.csv"

df = pd.read_csv(file_path)

print("First 5 Rows:")
print(df.head())

print("\nDataset Shape:", df.shape)

print("\nColumns:")
print(df.columns)

# -----------------------------
# Remove Missing Values
# -----------------------------
df = df.dropna()

# -----------------------------
# Convert Categorical Columns
# -----------------------------
label_encoder = LabelEncoder()

for column in df.columns:
    if df[column].dtype == 'object':
        df[column] = label_encoder.fit_transform(df[column].astype(str))

# -----------------------------
# Feature Scaling
# -----------------------------
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# -----------------------------
# Elbow Method
# -----------------------------
wcss = []

for i in range(1, 11):
    kmeans = KMeans(
        n_clusters=i,
        random_state=42,
        n_init=10
    )
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(8,5))
plt.plot(range(1,11), wcss, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.grid(True)
plt.show()

# -----------------------------
# K-Means Clustering
# -----------------------------
k = 4   # Change according to elbow graph

kmeans = KMeans(
    n_clusters=k,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(scaled_data)

df["Cluster"] = clusters

print("\nCluster Counts:")
print(df["Cluster"].value_counts())

# -----------------------------
# PCA Visualization
# -----------------------------
pca = PCA(n_components=2)

reduced_data = pca.fit_transform(scaled_data)

plt.figure(figsize=(10,7))

plt.scatter(
    reduced_data[:,0],
    reduced_data[:,1],
    c=clusters,
    cmap="viridis",
    s=40
)

plt.title("K-Means Clustering")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(label="Cluster")
plt.show()

# -----------------------------
# Cluster Centers
# -----------------------------
print("\nCluster Centers:")
print(kmeans.cluster_centers_)

# -----------------------------
# Save Clustered Dataset
# -----------------------------
output_file = "clustered_products.csv"
df.to_csv(output_file, index=False)

print("\nClustered dataset saved as:", output_file)