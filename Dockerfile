FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the crawler project
COPY AICrawler2/AICrawler2/emailcrawler /app/crawler

# Create output directory
RUN mkdir -p /app/output

WORKDIR /app/crawler

# Run the Scrapy spider
CMD ["scrapy", "crawl", "email_spider", "-o", "/app/output/results.json"]
