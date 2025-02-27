import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect("postgresql://postgres:lqXcYteJVjnFvaOOLUuVFLiqvkdIbFhC@crossover.proxy.rlwy.net:20588/railway")


# Create a cursor
cur = conn.cursor()

# Count the number of stored articles
cur.execute("SELECT COUNT(*) FROM news_articles;")
article_count = cur.fetchone()[0]

print(f"\n📰 Total Financial News Articles Stored: {article_count}")

# Retrieve the latest 5 articles for preview
cur.execute("SELECT * FROM news_articles ORDER BY published_at DESC LIMIT 5;")
articles = cur.fetchall()

print("\n📈 Preview of Latest 5 Articles:")
for article in articles:
    print(f"ID: {article[0]}")
    print(f"Title: {article[1]}")
    print(f"URL: {article[2]}")
    print(f"Source: {article[3]}")
    print(f"Published At: {article[4]}")
    print("-" * 40)

# Close connection
cur.close()
conn.close()
