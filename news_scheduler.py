import time
import requests
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Function to fetch news articles and store them in the database
def fetch_news():
    print("\n🔄 Fetching latest financial news...")

    # Fetch news from an API (replace with your actual API call)
    news_api_url = "https://newsapi.org/v2/everything?q=financial&apiKey=YOUR_API_KEY"
    response = requests.get(news_api_url)
    articles = response.json()["articles"]

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Insert each article into the database
        for article in articles:
            title = article["title"]
            url = article["url"]
            source = article["source"]["name"]
            published_at = article["publishedAt"]

            cur.execute("""
                INSERT INTO news_articles (title, url, source, published_at)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """, (title, url, source, published_at))

        conn.commit()
        print("✅ Articles fetched and stored successfully!")

        # Close the connection
        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

# Run the fetch_news function every 2 hours
while True:
    fetch_news()
    time.sleep(7200)  # Wait for 2 hours
