import numpy as np
import faiss
import os

print("🔍 Building FAISS index for semantic search...")

# Check if embeddings file exists
if not os.path.exists("news_embeddings.npy"):
    print("❌ Error: news_embeddings.npy not found!")
    print("   Please run 'python build_embeddings.py' first.")
    exit()

# Load embeddings
print("📥 Loading embeddings...")
embeddings = np.load("news_embeddings.npy").astype("float32")
print(f"   Loaded {embeddings.shape[0]} embeddings with dimension {embeddings.shape[1]}")

# Get dimension
d = embeddings.shape[1]

# Create FAISS index
# Using IndexFlatIP (Inner Product) with normalized vectors = cosine similarity
print("🔨 Creating FAISS IndexFlatIP...")
index = faiss.IndexFlatIP(d)

# Add vectors to index
print("🔄 Adding embeddings to index...")
index.add(embeddings)

print(f"   Index contains {index.ntotal} vectors")

# Save index
print("💾 Saving FAISS index...")
faiss.write_index(index, "news_faiss.index")

print("✅ Done! FAISS index saved as: news_faiss.index")
print(f"\n📊 Index stats:")
print(f"   Total vectors: {index.ntotal}")
print(f"   Dimension: {d}")
print(f"   Index type: Flat (exact search)")
print(f"   Similarity metric: Inner Product (cosine with normalized vectors)")
