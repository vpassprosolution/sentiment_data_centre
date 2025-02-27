import psycopg2

# Connect to Railway PostgreSQL
conn = psycopg2.connect("postgresql://postgres:lqXcYteJVjnFvaOOLUuVFLiqvkdIbFhC@crossover.proxy.rlwy.net:20588/railway")

# Create a cursor
cur = conn.cursor()

# Create the news_articles table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS news_articles (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT UNIQUE NOT NULL,
        source TEXT NOT NULL,
        published_at TIMESTAMP NOT NULL
    );
""")

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print("✅ Railway PostgreSQL database is ready! Table 'news_articles' created successfully.")
