import feedparser, hashlib, pandas as pd, os, json
from supabase import create_client
from datetime import datetime

SUPABASE_URL = "YOUR_URL"
SUPABASE_KEY = "YOUR_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

csv_file = "news_data.csv"

# Load RSS config
with open("rss_links.json") as f:
    rss_config = json.load(f)

# Load history
if os.path.exists(csv_file):
    df_old = pd.read_csv(csv_file)
    existing_ids = set(df_old["id"])
else:
    df_old = pd.DataFrame()
    existing_ids = set()

new_rows = []

for source, categories in rss_config.items():
    for category, link in categories.items():
        print(f"📡 Fetching {source} - {category}")

        feed = feedparser.parse(link)

        for item in feed.entries:
            uid = hashlib.sha256(item.link.encode()).hexdigest()

            if uid in existing_ids:
                continue

            row = {
                "id": uid,
                "title": item.title,
                "link": item.link,
                "published": item.get("published", datetime.utcnow().isoformat()),
                "summary": item.get("summary", ""),
                "source": source,
                "category": category
            }

            new_rows.append(row)

# Save CSV
df_new = pd.DataFrame(new_rows)
df_final = pd.concat([df_old, df_new], ignore_index=True)
df_final.to_csv(csv_file, index=False)

print(f"✅ Added {len(new_rows)} new articles")

# Push to Supabase
if new_rows:
    try:
        res = supabase.table("news").upsert(new_rows).execute()
        print("✅ Uploaded to Supabase")
    except Exception as e:
        print("❌ Upload error:", e)

print("Done ✅")
