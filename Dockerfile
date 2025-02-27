# Use the official Python 3.9 image from DockerHub
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory into /app in the container
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the news_scheduler.py script when the container starts
CMD ["python", "news_scheduler.py"]
