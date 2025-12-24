import os
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch
import sys

class NewsSearchEngine:
    def __init__(self):
        print("🚀 Initializing News Search Engine...")
        
        # Check required files
        if not os.path.exists("news_faiss.index"):
            print("❌ Error: news_faiss.index not found!")
            print("   Please run: python build_faiss_index.py")
            exit()
        
        if not os.path.exists("news_metadata.parquet"):
            print("❌ Error: news_metadata.parquet not found!")
            print("   Please run: python build_embeddings.py")
            exit()
        
        # Load metadata
        print("📥 Loading metadata...")
        self.df = pd.read_parquet("news_metadata.parquet")
        print(f"   Loaded {len(self.df)} articles")
        
        # Load FAISS index
        print("📥 Loading FAISS index...")
        self.index = faiss.read_index("news_faiss.index")
        print(f"   Index contains {self.index.ntotal} vectors")
        
        # Load model
        print("🤖 Loading SentenceTransformer model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1", device=device)
        print(f"   Using device: {device}")
        
        print("✅ Search engine ready!\n")
    
    def search(self, query, k=5):
        """Search for top-k relevant news articles"""
        # Encode query
        q_emb = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True
        ).astype("float32")
        
        # Search
        scores, indices = self.index.search(q_emb, k)
        indices = indices[0]
        scores = scores[0]
        
        # Prepare results
        results = []
        for rank, (idx, score) in enumerate(zip(indices, scores), 1):
            row = self.df.iloc[int(idx)]
            results.append({
                "rank": rank,
                "score": float(score),
                "title": row["title"],
                "link": row["link"],
                "source": row["source"],
                "category": row["category"],
                "published": row["published"],
                "text": row["combined_text"][:200] + "..."  # First 200 chars
            })
        
        return results
    
    def print_results(self, results):
        """Pretty print search results"""
        for r in results:
            print(f"\n{'='*80}")
            print(f"Rank {r['rank']} | Score: {r['score']:.4f}")
            print(f"\n📰 {r['title']}")
            print(f"\n🔗 {r['link']}")
            print(f"\n📌 Source: {r['source']} | Category: {r['category']}")
            print(f"📅 Published: {r['published']}")
            print(f"\n📝 Snippet: {r['text']}")
        print(f"\n{'='*80}\n")

if __name__ == "__main__":
    # Initialize engine
    engine = NewsSearchEngine()
    
    # Check if query provided as argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"🔍 Query: {query}\n")
        results = engine.search(query, k=5)
        engine.print_results(results)
    else:
        # Interactive mode
        print("🔍 Interactive Search Mode")
        print("Type your query (or 'exit' to quit)\n")
        
        while True:
            query = input("🔎 Enter query: ").strip()
            
            if query.lower() in ["exit", "quit", "q"]:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print(f"\n🔍 Searching for: {query}\n")
            results = engine.search(query, k=5)
            engine.print_results(results)
