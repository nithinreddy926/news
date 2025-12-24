import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client
from dotenv import load_dotenv
import torch

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("🔄 Connecting to Supabase...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch all news data from Supabase
print("📥 Fetching news data from Supabase...")
response = supabase.table("news").select("*").execute()
data = response.data

if not data:
    print("❌ No data found in Supabase!")
    exit()

print(f"✅ Fetched {len(data)} articles")

# Convert to DataFrame
df = pd.DataFrame(data)

# Combine title + summary into combined_text
df["combined_text"] = df["title"].fillna("") + " " + df["summary"].fillna("")
df = df[["id", "title", "link", "combined_text", "source", "category", "published"]]

print(f"📝 Sample combined text: {df['combined_text'].iloc[0][:100]}...")

# Load SentenceTransformer model
print("🤖 Loading SentenceTransformer model (multi-qa-MiniLM-L6-cos-v1)...")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"   Using device: {device}")
model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1", device=device)

# Generate embeddings
print("🔄 Generating embeddings...")
texts = df["combined_text"].tolist()
embeddings = model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True  # Important for cosine similarity
)

print(f"✅ Generated embeddings with shape: {embeddings.shape}")

# Save embeddings and metadata
print("💾 Saving embeddings and metadata...")
np.save("news_embeddings.npy", embeddings)
df.to_parquet("news_metadata.parquet", index=False)

print("✅ Done! Files saved:")
print("   - news_embeddings.npy")
print("   - news_metadata.parquet")
print(f"\n📊 Total articles processed: {len(df)}")
print(f"📏 Embedding dimension: {embeddings.shape[1]}")
