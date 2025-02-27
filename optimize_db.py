import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="sentiment_db",
    user="postgres",
    password="Didie555363!",
    host="localhost",
    port="5432"
)

# Create a cursor
cur = conn.cursor()

# Add an index on the published_at column to speed up queries
cur.execute("CREATE INDEX IF NOT EXISTS idx_published_at ON news_articles(published_at);")

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print("✅ Database optimization complete! Index added for faster queries.")
