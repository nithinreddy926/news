import pandas as pd
import os
from datetime import datetime

CSV_FILE = "results.csv"

def save_results_to_csv(input_article, results):
    rows = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for rank, (article, score) in enumerate(results, start=1):
        rows.append({
            "run_timestamp": timestamp,
            "input_article": input_article.replace("\n", " "),
            "similar_article_rank": rank,
            "similarity_score": round(float(score), 4),
            "article_url": article["url"],
            "article_content": article["content"][:2000]  # keep CSV light
        })

    df = pd.DataFrame(rows)

    file_exists = os.path.exists(CSV_FILE)

    df.to_csv(
        CSV_FILE,
        mode="a",
        header=not file_exists,
        index=False,
        encoding="utf-8"
    )
