from config import EMBEDDING_MODEL, MAX_SEARCH_RESULTS, TOP_K_RESULTS
from embedder import Embedder
from search_web import search_web
from fetch_article import fetch_full_article
from similarity_ranker import rank_articles
from save_to_csv import save_results_to_csv


def run_pipeline(user_article: str):
    embedder = Embedder(EMBEDDING_MODEL)

    # 1️⃣ Embed user article
    print("\n[1] Embedding user article...")
    query_embedding = embedder.embed(user_article)

    # 2️⃣ Generate search query
    search_query = user_article[:300].replace("\n", " ")
    print("[2] Search query generated")

    # 3️⃣ Web search
    print("[3] Searching web...")
    urls = search_web(search_query, MAX_SEARCH_RESULTS)

    if not urls:
        print("❌ No URLs returned from web search.")
        return []

    print(f"   → {len(urls)} URLs found")

    articles = []
    embeddings = []

    # 4️⃣ Fetch + embed articles
    print("[4] Fetching full articles...")
    for url in urls:
        text = fetch_full_article(url)

        # relaxed filter (important for free scraping)
        if text and len(text) > 150:
            articles.append({
                "url": url,
                "content": text
            })
            embeddings.append(embedder.embed(text))

    if not articles:
        print("❌ No full articles could be extracted.")
        return []

    print(f"   → {len(articles)} articles extracted")

    # 5️⃣ Similarity ranking
    print("[5] Ranking articles...")
    ranked = rank_articles(query_embedding, embeddings, articles)

    if not ranked:
        print("❌ Similarity ranking failed.")
        return []

    return ranked[:TOP_K_RESULTS]


# ---------------- RUN ----------------
if __name__ == "__main__":
    print("\n===== WEB ARTICLE SIMILARITY PIPELINE =====\n")

    user_article = input("Paste full article and press Enter:\n\n")

    results = run_pipeline(user_article)

    if not results:
        print("\n⚠️ No similar articles found. Try another input.\n")
    else:
        print("\n===== TOP SIMILAR ARTICLES =====")

        for i, (article, score) in enumerate(results, 1):
            print(f"\n{i}. Similarity Score: {score:.3f}")
            print(f"URL: {article['url']}")
            print(article["content"][:500], "...")

        # ✅ SAVE TO CSV
        save_results_to_csv(user_article, results)
        print("\n✅ Results saved to results.csv")
