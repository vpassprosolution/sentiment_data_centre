# Use official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a dummy port (since Railway might expect one)
EXPOSE 8080

# Start the news_scheduler.py script and keep it running
CMD ["python", "news_scheduler.py"]
