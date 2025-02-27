import requests
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Fetch news from an API (replace with your actual API call)
news_api_url = "https://newsapi.org/v2/everything?q=financial&apiKey=YOUR_API_KEY"
response = requests.get(news_api_url)

# Print the full API response for debugging
print("API Response:", response.json())

# Check if 'articles' exists in the response
try:
    articles = response.json()["articles"]
    print(f"Fetched {len(articles)} articles.")
except KeyError as e:
    print(f"❌ KeyError: The key 'articles' does not exist in the response.")
    print(f"Full response: {response.json()}")
    exit()  # Exit if the articles are not found
