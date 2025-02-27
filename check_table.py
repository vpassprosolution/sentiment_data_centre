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

# Check if the table exists
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
tables = cur.fetchall()

# Print tables found
print("Tables in sentiment_db:")
for table in tables:
    print(table[0])

# Close connection
cur.close()
conn.close()
