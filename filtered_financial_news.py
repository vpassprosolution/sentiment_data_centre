import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect("postgresql://postgres:lqXcYteJVjnFvaOOLUuVFLiqvkdIbFhC@crossover.proxy.rlwy.net:20588/railway")


# Create a cursor
cur = conn.cursor()

# List of financial keywords (market-related)
financial_keywords = [
    "gold price", "gold market", "bitcoin", "ethereum", 
    "dow jones", "nasdaq", "eur/usd", "gbp/usd", "forex", "stock market", "crypto", "trading"
]

# List of trusted financial news sources
financial_sources = [
    "Bloomberg", "Reuters", "CNBC", "Financial Times", "MarketWatch", "Yahoo Finance", "Investing.com"
]

# Query to fetch only relevant financial news
query = """
SELECT * FROM news_articles
WHERE (
    {}
) AND (
    {}
)
ORDER BY published_at DESC
LIMIT 5;
""".format(
    " OR ".join(["LOWER(title) LIKE '%{}%'".format(k) for k in financial_keywords]),
    " OR ".join(["LOWER(source) LIKE '%{}%'".format(s.lower()) for s in financial_sources])
)

# Execute query
cur.execute(query)
articles = cur.fetchall()

# Display results
print("\n📈 Latest 5 Trading-Related Financial News Articles:")
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
