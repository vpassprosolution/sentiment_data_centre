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
    
    # Make the API request
    try:
        response = requests.get(news_api_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

        # Print the full API response for debugging
        print("API Response:", response.json())  # Debugging: print the full response

        # Check if 'articles' exists in the response
        if "articles" not in response.json():
            print("❌ No 'articles' field found in the response.")
            print(f"Full API response: {response.json()}")
            return  # Exit the function if the 'articles' key is missing

        articles = response.json()["articles"]

        if not articles:
            print("❌ No articles found.")
            return  # Exit the function if no articles are found
        
        print(f"Fetched {len(articles)} articles.")

        # Connect to PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

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
            except Exception as e:
                print(f"❌ Error inserting article into the database: {e}")
                continue  # Skip this article and move to the next one

        # Commit the changes to the database
        conn.commit()
        print("✅ Articles fetched and stored successfully!")

        # Close the connection
        cur.close()
        conn.close()

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data from NewsAPI: {e}")
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# Run the fetch_news function every 2 hours
while True:
    fetch_news()
    time.sleep(7200)  # Wait for 2 hours
