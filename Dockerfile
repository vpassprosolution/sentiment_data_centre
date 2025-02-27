# Use official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a dummy port to prevent Railway from shutting down the container
EXPOSE 8080

# Run the news_scheduler.py script as a background job
CMD ["python", "news_scheduler.py"]

