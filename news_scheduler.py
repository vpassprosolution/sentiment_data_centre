import schedule
import time
import subprocess

# Function to run the fetch_news.py script
def fetch_news():
    print("\n🔄 Fetching latest financial news...")
    subprocess.run(["python", "fetch_news.py"])

# Schedule the script to run every 2 hours
schedule.every(2).hours.do(fetch_news)

print("✅ News fetcher is running. It will update every 2 hours.")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
