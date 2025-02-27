from flask import Flask
import threading
import time

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Background Worker is Running!"

# Function to keep the background job running
def start_background_job():
    while True:
        print("\n🔄 Fetching latest financial news...")
        # Call your news-fetching function here (like fetch_news.py)
        time.sleep(7200)  # Sleep for 2 hours

if __name__ == "__main__":
    # Start background job in a separate thread
    threading.Thread(target=start_background_job).start()

    # Start Flask app on port 8080
    app.run(host='0.0.0.0', port=8080)
