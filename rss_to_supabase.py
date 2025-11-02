import feedparser, hashlib, pandas as pd, os, json
from supabase import create_client
from datetime import datetime

SUPABASE_URL = "https://bwtgiawaktzohibphcgx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ3dGdpYXdha3R6b2hpYnBoY2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA4Njk1NzUsImV4cCI6MjA3NjQ0NTU3NX0.vt01f-cymLgyCRcZ0d_zdv8Lu04yhiYg_F2kU08mX4c"

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
    df_old = pd.DataFrame(columns=["id","title","link","published","summary","source","category"])
    existing_ids = set()

new_rows = []

for source, categories in rss_config.items():
    for category, link in categories.items():
        print(f"📡 Fetching {source} - {category}")

        feed = feedparser.parse(link)

        for item in feed.entries:
            uid = hashlib.sha256(item.link.encode()).hexdigest()

            # Skip if exists in CSV cache
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

# ✅ Remove duplicates inside this batch too
df_new = pd.DataFrame(new_rows)
df_new = df_new.drop_duplicates(subset=["id"], keep="first")

# Save CSV
df_final = pd.concat([df_old, df_new], ignore_index=True)
df_final.to_csv(csv_file, index=False)

print(f"✅ Added {len(df_new)} new articles")

# Push to Supabase
if len(df_new) > 0:
    try:
        res = supabase.table("news").upsert(df_new.to_dict(orient="records")).execute()
        print("✅ Uploaded to Supabase")
    except Exception as e:
        print("❌ Upload error:", e)
else:
    print("⚠️ No new articles to upload")

print("Done ✅")
