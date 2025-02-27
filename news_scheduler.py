import time
import requests
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")  # Load API key from .env file

# List of financial instruments
financial_instruments = [
    "Gold", "Bitcoin", "Ethereum", "US30", "NASDAQ 100", "EUR/USD", "GBP/USD"
]

# Function to fetch news articles and store them in the database
def fetch_news():
    print("\n🔄 Fetching latest financial news...")

    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Loop through each financial instrument and fetch articles
    for instrument in financial_instruments:
        # Update the API request to fetch 50 articles for each instrument
        news_api_url = f"https://newsapi.org/v2/everything?q={instrument}&apiKey={NEWSAPI_KEY}&pageSize=50"
        
        try:
            # Fetch the news articles
            response = requests.get(news_api_url)
            response.raise_for_status()  # Raise an exception for invalid responses
            
            # Print the full API response for debugging
            print(f"API Response for {instrument}: {response.json()}")  # Debugging: print the full response

            # Check if 'articles' is present in the response
            if "articles" not in response.json():
                print(f"❌ No 'articles' field found for {instrument}.")
                continue  # Skip this instrument and move to the next one

            articles = response.json()["articles"]

            if not articles:
                print(f"❌ No articles found for {instrument}.")
                continue  # Skip this instrument if no articles are found

            print(f"Fetched {len(articles)} articles for {instrument}.")

            # Insert each article into the database
            for article in articles:
                title = article.get("title", "No Title")
                url = article.get("url", "No URL")
                source = article.get("source", {}).get("name", "Unknown Source")
                published_at = article.get("publishedAt", "Unknown Date")

                # Insert data into PostgreSQL
                try:
                    cur.execute("""
                        INSERT INTO news_articles (title, url, source, published_at)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (url) DO NOTHING;
                    """, (title, url, source, published_at))
                    print(f"✅ Inserted article for {instrument}: {title}")
                except Exception as e:
                    print(f"❌ Error inserting article '{title}' for {instrument}: {e}")
                    continue  # Skip this article and move to the next one

            # Commit the changes after processing all articles for this instrument
            conn.commit()

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data for {instrument}: {e}")

    # Close the connection
    cur.close()
    conn.close()

    print("✅ Articles fetched and stored successfully!")

# Run the fetch_news function every 2 hours
while True:
    fetch_news()
    time.sleep(7200)  # Wait for 2 hours
