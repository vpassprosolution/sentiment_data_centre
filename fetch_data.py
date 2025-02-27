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

# Retrieve data
cur.execute("SELECT * FROM news_articles;")
articles = cur.fetchall()

# Display results
print("\n📰 Stored Financial News Articles:")
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
