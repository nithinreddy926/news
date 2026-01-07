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
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── .github/workflows/
    └── rss_scraper.yml       # GitHub Actions workflow
```

## 🔄 How It Works

### Current Automated Workflow

This project runs a fully automated pipeline that keeps your news search engine up-to-date:

#### 1. **Automated RSS Scraping** (⏰ Every 6 hours)
- **GitHub Actions** workflow runs automatically
- Scrapes RSS feeds from sources defined in `rss_links.json`
- Extracts: title, description, link, published date, source, category
- Performs SHA256-based deduplication
- Upserts new articles into **Supabase `news` table**
- Also updates local `news_data.csv` cache

#### 2. **Embedding Generation** (🧠 After scraping)
- Pulls all articles from Supabase
- Combines title + description into `combinedtext`
- Generates 384-dimensional embeddings using **SentenceTransformer**
- Model: `multi-qa-MiniLM-L6-cos-v1`
- Saves embeddings to `news_embeddings.npy`
- Saves metadata to `news_metadata.parquet`

#### 3. **FAISS Index Building** (📁 After embeddings)
- Loads embeddings from `.npy` file
- Builds **FAISS IndexFlatIP** for fast similarity search
- Normalizes vectors for cosine similarity
- Saves index to `news_faiss.index`

#### 4. **Ready for Search** (🔍 Instant queries)
- Command-line: `python search_news.py "your query"`
- Web interface: `streamlit run app.py`
- Encodes query using same SentenceTransformer model
- Performs top-k similarity search in FAISS
- Returns ranked results with scores

### Workflow Diagram

```
GitHub Actions (every 6 hours)
        ↓
  RSS Feeds → rss_to_supabase.py → Supabase (news table)
        ↓
  build_embeddings.py → news_embeddings.npy + news_metadata.parquet
        ↓
  build_faiss_index.py → news_faiss.index
        ↓
  search_news.py / app.py → Search Results
```

### Download Index Files

Since embeddings and FAISS index are built on GitHub Actions runners, you need to:

1. Go to **Actions** tab in GitHub
2. Click on latest **"RSS scraper + index builder"** workflow run
3. Scroll to **Artifacts** section
4. Download `news-search-index.zip`
5. Extract into your local project folder
6. Now you can search locally!



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
