from sklearn.metrics.pairwise import cosine_similarity

def rank_articles(query_embedding, article_embeddings, articles):
    if not article_embeddings:
        return []

    scores = cosine_similarity(
        [query_embedding], article_embeddings
    )[0]

    ranked = sorted(
        zip(articles, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked
