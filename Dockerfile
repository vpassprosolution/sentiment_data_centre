# Use official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Railway
EXPOSE 8080

# Run the simple test script to confirm the container keeps running
CMD ["python", "test_start.py"]
