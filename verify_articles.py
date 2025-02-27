import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Verify stored articles
def verify_articles():
    print("\n📰 Verifying Stored Financial News Articles...")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Get the total number of articles stored
        cur.execute("SELECT COUNT(*) FROM news_articles;")
        count = cur.fetchone()[0]
        print(f"✅ Total Financial News Articles Stored: {count}")

        # Preview the latest 5 articles
        cur.execute("SELECT * FROM news_articles ORDER BY published_at DESC LIMIT 5;")
        articles = cur.fetchall()

        print("\n📈 Preview of Latest 5 Articles:")
        for article in articles:
            print(f"ID: {article[0]} | Title: {article[1]} | URL: {article[2]} | Source: {article[3]} | Published At: {article[4]}")

        # Close the connection
        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

# Run the verification
verify_articles()
