import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Try connecting to the PostgreSQL database
try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Check if the news_articles table exists
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()

    if ("news_articles",) in tables:
        print("✅ The 'news_articles' table exists.")
    else:
        print("❌ The 'news_articles' table does not exist.")
    
    # Check the record count if the table exists
    if ("news_articles",) in tables:
        cur.execute("SELECT COUNT(*) FROM news_articles;")
        count = cur.fetchone()[0]
        print(f"Total articles: {count}")

    # Close the connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")
