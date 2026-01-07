# News Data Extraction & Semantic Search System

A complete news scraping, storage, and semantic search pipeline that automatically collects news articles from RSS feeds and enables intelligent search using vector embeddings.

## 🚀 Features

- **Automated RSS Scraping**: GitHub Actions cron job scrapes news from multiple sources
- **Supabase Integration**: Stores news data in cloud database
- **Semantic Search**: Uses SentenceTransformers and FAISS for intelligent article retrieval
- **Duplicate Detection**: SHA256-based deduplication
- **Interactive Search**: Command-line and programmatic search interface

## 📁 Project Structure

```
├── rss_to_supabase.py       # RSS scraper with Supabase integration
├── rss_links.json            # RSS feed sources
├── build_embeddings.py       # Generate embeddings from Supabase data
├── build_faiss_index.py      # Build FAISS index for fast search
├── search_news.py            # Search engine interface
├── app.py                      # Streamlit web interface
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── .github/workflows/
    └── rss_scraper.yml       # GitHub Actions workflow
```

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 3. Add RSS Sources

Edit `rss_links.json` to add your news sources:

```json
[
  {
    "url": "https://example.com/feed.xml",
    "source": "Example News",
    "category": "Technology"
  }
]
```

## 📊 Usage

### Step 1: Scrape News (Manual)

```bash
python rss_to_supabase.py
```

This runs automatically via GitHub Actions on schedule.

### Step 2: Generate Embeddings

```bash
python build_embeddings.py
```

This will:
- Pull all news from Supabase
- Generate 384-dim embeddings using `multi-qa-MiniLM-L6-cos-v1`
- Save to `news_embeddings.npy` and `news_metadata.parquet`

### Step 3: Build FAISS Index

```bash
python build_faiss_index.py
```

Creates `news_faiss.index` for fast similarity search.

### Step 4: Search News

**Interactive Mode:**
```bash
python search_news.py
```

**Direct Query:**
```bash
python search_news.py "impact of interest rate hikes on economy"
```

**Programmatic Usage:**
```python
from search_news import NewsSearchEngine

engine = NewsSearchEngine()
results = engine.search("AI developments", k=5)

for r in results:
    print(f"{r['rank']}. {r['title']} (score: {r['score']:.4f})")
```

### Step 5: Streamlit Web Interface (Optional - For Instant Search)

For a better user experience with instant searches (no 17-second reload), use the Streamlit web interface:

```bash
streamlit run app.py
```

This will:
- Load the model once (17s startup)
- Open a web interface in your browser
- Enable instant searches (<1 second)
- Stay running for multiple searches

**Features:**
- 🔍 Search box with auto-complete
- 🎯 Relevance scores with color coding
- 📅 Metadata display (source, category, date)
- 🔗 Direct article links
- 📊 Statistics sidebar
- ⚡ No model reloading between searches



## 🤖 GitHub Actions Automation

The scraper runs automatically:
- **Schedule**: Every 6 hours (configured in `.github/workflows/rss_scraper.yml`)
- **Manual**: Via GitHub Actions "Run workflow" button

## 🔧 Technical Details

### Embedding Model
- **Model**: `sentence-transformers/multi-qa-MiniLM-L6-cos-v1`
- **Dimension**: 384
- **Optimized for**: Question-answering and semantic search

### FAISS Index
- **Type**: IndexFlatIP (Inner Product)
- **Similarity**: Cosine similarity with normalized vectors
- **Search**: Exact nearest neighbor search

### Data Flow

```
RSS Feeds → rss_to_supabase.py → Supabase
                                      ↓
                          build_embeddings.py → news_embeddings.npy
                                      ↓
                          build_faiss_index.py → news_faiss.index
                                      ↓
                             search_news.py → Results
```

## 📝 Example Output

```
🔍 Query: AI regulation policies

================================================================================
Rank 1 | Score: 0.8542

📰 EU Passes Landmark AI Regulation Act

🔗 https://example.com/article/123

📌 Source: Tech News | Category: Technology
📅 Published: 2025-12-24T08:00:00Z

📝 Snippet: The European Union has passed comprehensive AI regulation...
================================================================================
```

## 🔄 Updating the Search Index

When new articles are added:

```bash
python build_embeddings.py   # Re-generate embeddings
python build_faiss_index.py  # Rebuild index
```

## 📦 Dependencies

- `feedparser`: RSS feed parsing
- `supabase`: Database client
- `sentence-transformers`: Embedding generation
- `faiss-cpu`: Vector similarity search
- `pandas`: Data processing
- `torch`: Deep learning backend

## 🎯 Future Enhancements

- [ ] RAG integration with LLM for summarization
- [ ] Web API (FastAPI)
- [ ] Real-time search updates
- [ ] Multi-language support
- [ ] Advanced filtering (date, source, category)

## 📄 License

MIT License

---

**Created by Ransh Innovations**
