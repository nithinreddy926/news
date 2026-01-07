"""News Semantic Search - Streamlit Web Interface
Created by Ransh Innovations
"""

import streamlit as st
from search_news import NewsSearchEngine
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="News Semantic Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cache the engine so it loads only once
@st.cache_resource
def load_search_engine():
    """Load the search engine once and cache it"""
    return NewsSearchEngine()

# Load engine with progress indicator
with st.spinner("🚀 Initializing News Search Engine..."):
    engine = load_search_engine()

# Main UI
st.title("🔍 News Semantic Search")
st.markdown("""
Search across **1000+ news articles** using AI-powered semantic search.  
Results ranked by semantic similarity, not just keyword matching.
""")

# Search interface
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "Search Query",
        placeholder="e.g., AI regulation, climate change policy, economic outlook",
        label_visibility="collapsed"
    )

with col2:
    num_results = st.slider("Results", 3, 20, 10, label_visibility="collapsed")

# Search results
if query:
    # Perform search
    with st.spinner(f"🔎 Searching for '{query}'..."):
        results = engine.search(query, k=num_results)
    
    # Success message
    st.success(f"✅ Found **{len(results)} results** in less than 1 second!")
    
    # Display results
    for r in results:
        with st.container():
            # Create columns for rank and content
            col_rank, col_content = st.columns([0.8, 11])
            
            # Rank and score
            with col_rank:
                st.markdown(f"### {r['rank']}")
                score_color = "green" if r['score'] > 0.7 else "orange" if r['score'] > 0.5 else "red"
                st.markdown(f":{score_color}[**{r['score']:.3f}**]")
            
            # Article content
            with col_content:
                # Title with link
                st.markdown(f"### [{r['title']}]({r['link']})")
                
                # Metadata row
                col_source, col_category, col_date = st.columns(3)
                with col_source:
                    st.caption(f"📰 **Source:** {r['source']}")
                with col_category:
                    st.caption(f"📂 **Category:** {r['category']}")
                with col_date:
                    st.caption(f"📅 **Published:** {r['published']}")
                
                # Snippet
                st.markdown(f"_{r['snippet']}_")
                
                # Link button
                st.link_button("🔗 Read Full Article", r['link'], use_container_width=False)
            
            st.divider()

# Empty state - show examples
else:
    st.info("👆 Enter a search query above to get started!")
    
    # Example searches
    st.markdown("### 💡 Try these example searches:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    example_queries = [
        ("🤖", "AI developments"),
        ("🌍", "Climate change"),
        ("💰", "Economic policy"),
        ("🏥", "Healthcare news")
    ]
    
    for col, (emoji, example) in zip([col1, col2, col3, col4], example_queries):
        with col:
            if st.button(f"{emoji} {example}", use_container_width=True):
                st.session_state['query'] = example
                st.rerun()

# Sidebar - statistics
with st.sidebar:
    st.header("📊 Statistics")
    
    # Try to get stats from engine
    try:
        total_articles = len(engine.metadata)
        st.metric("Total Articles", f"{total_articles:,}")
        st.metric("Vector Dimension", "384")
        st.metric("Model", "multi-qa-MiniLM-L6-cos-v1")
    except:
        pass
    
    st.divider()
    
    st.markdown("### 🛠️ About")
    st.markdown("""
    This semantic search engine uses:
    - **SentenceTransformers** for embeddings
    - **FAISS** for fast similarity search
    - **Supabase** for data storage
    """)
    
    st.divider()
    
    st.markdown("### 🚀 Features")
    st.markdown("""
    - ⚡ Instant search after first load
    - 🎯 Semantic similarity matching
    - 📊 Relevance scoring
    - 🔄 Auto-updated from RSS feeds
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("🚀 Powered by SentenceTransformers + FAISS | Built by Ransh Innovations")
