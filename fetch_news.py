import requests
import psycopg2
from datetime import datetime

# Replace with your actual API keys
NEWSAPI_KEY = "8d2b07691ab54b1592d99b5fa6dcc948"
GNEWS_KEY = "dd0490acae3413a8b95335a8ace58347"

# PostgreSQL Connection
conn = psycopg2.connect("postgresql://postgres:lqXcYteJVjnFvaOOLUuVFLiqvkdIbFhC@crossover.proxy.rlwy.net:20588/railway")

cur = conn.cursor()

# Function to fetch news from NewsAPI (limit 50)
def fetch_newsapi():
    url = f"https://newsapi.org/v2/everything?q=gold OR bitcoin OR ethereum OR dowjones OR nasdaq OR eurusd OR gbpusd&language=en&pageSize=50&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("articles", [])

# Function to fetch news from GNews (limit 50)
def fetch_gnews():
    url = f"https://gnews.io/api/v4/search?q=gold OR bitcoin OR ethereum OR dowjones OR nasdaq OR eurusd OR gbpusd&lang=en&max=50&token={GNEWS_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("articles", [])

# Step 1: Remove older articles beyond the latest 50
cur.execute("""
    DELETE FROM news_articles 
    WHERE id NOT IN (
        SELECT id FROM news_articles ORDER BY published_at DESC LIMIT 50
    );
""")
conn.commit()

# Insert new articles
def store_articles(articles, source_name):
    for article in articles:
        title = article["title"]
        url = article["url"]
        published_at = article.get("publishedAt", datetime.now().isoformat())

        try:
            cur.execute("""
                INSERT INTO news_articles (title, url, source, published_at)
                VALUES (%s, %s, %s, %s)
            """, (title, url, source_name, published_at))
            conn.commit()  # Commit only when successful
        except psycopg2.errors.UniqueViolation:
            conn.rollback()  # Skip duplicate articles

# Fetch and store fresh news
newsapi_articles = fetch_newsapi()
gnews_articles = fetch_gnews()
store_articles(newsapi_articles, "NewsAPI")
store_articles(gnews_articles, "GNews")

# Step 2: Ensure only the latest 50 articles remain in the database
cur.execute("""
    DELETE FROM news_articles 
    WHERE id NOT IN (
        SELECT id FROM news_articles ORDER BY published_at DESC LIMIT 50
    );
""")
conn.commit()

# Close connection
cur.close()
conn.close()

print("✅ Old news removed! Only the latest 50 financial news articles are stored.")
