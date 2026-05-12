#!/bin/bash

# Email Crawler Setup Script
# Run this to set up Docker and prepare for Jenkins

set -e

echo "📦 Email Crawler - Setup Script"
echo "================================"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

echo "✅ Docker found: $(docker --version)"

# Check Git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git first."
    exit 1
fi

echo "✅ Git found: $(git --version)"

# Initialize Git repo if not already done
if [ ! -d ".git" ]; then
    echo ""
    echo "🔧 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Email crawler with Docker and Jenkins"
    echo "✅ Git repo initialized"
else
    echo "✅ Git repo already initialized"
fi

# Create .env from .env.example if not exists
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your configuration"
fi

# Build Docker image
echo ""
echo "🔨 Building Docker image..."
docker build -t email-crawler:latest .
echo "✅ Docker image built successfully"

# Create output directory
mkdir -p output
echo "✅ Output directory created"

# Test crawler locally
echo ""
read -p "🧪 Run a test crawl now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running test crawler..."
    mkdir -p AICrawler2/AICrawler2/emailcrawler/emailcrawler/{websites,output}
    
    # Create sample websites.txt if not exists
    if [ ! -f "AICrawler2/AICrawler2/emailcrawler/emailcrawler/websites.txt" ]; then
        echo "https://example.com" > AICrawler2/AICrawler2/emailcrawler/emailcrawler/websites.txt
    fi
    
    docker run --rm \
        -v "$(pwd)/AICrawler2/AICrawler2/emailcrawler/emailcrawler/websites.txt:/app/crawler/websites.txt" \
        -v "$(pwd)/output:/app/output" \
        email-crawler:latest
    
    echo "✅ Test crawl completed. Check output/ folder."
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📝 Next Steps:"
echo "1. Edit .env with your configuration"
echo "2. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/EmailDocker.git"
echo "   git push -u origin main"
echo "3. Set up Jenkins:"
echo "   - Create new Pipeline job"
echo "   - Point to Jenkinsfile in this repo"
echo "   - Configure triggers"
echo "4. Access Flask app:"
echo "   docker-compose up"
echo "   Open http://localhost:5000"
echo ""
echo "🚀 Good luck!"
