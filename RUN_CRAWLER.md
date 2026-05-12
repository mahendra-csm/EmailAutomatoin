# Email Crawler - Docker + Jenkins Setup

## 📋 Project Overview
- **Input:** Upload `websites.txt` via Flask web UI
- **Process:** Scrapy crawler extracts emails from URLs
- **Output:** Results in `extracted_emails.txt` and `output/results.json`
- **Schedule:** Runs automatically every night at 10 PM (via Jenkins)
- **Deployment:** Dockerized for consistency across environments

---

## 🚀 Quick Start - Local Testing

### 1️⃣ Build Docker Image
```bash
docker build -t email-crawler:latest .
```

### 2️⃣ Run Crawler Manually
```bash
docker run --rm \
  -v $(pwd)/AICrawler2/AICrawler2/emailcrawler/emailcrawler/websites.txt:/app/crawler/websites.txt \
  -v $(pwd)/output:/app/output \
  email-crawler:latest
```

### 3️⃣ Use Docker Compose (Web + Jenkins)
```bash
docker-compose up -d
```
- Web UI: http://localhost:5000
- Jenkins: http://localhost:8080

---

## 📝 Setup Guide - Production

### Prerequisites
- Docker installed
- Jenkins server running
- Git repository configured
- AWS EC2 or Linux server (recommended)

### Step 1: Initialize Git Repository
```bash
cd EmailDocker
git init
git add .
git commit -m "Initial commit: Email crawler with Docker"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/EmailDocker.git
git push -u origin main
```

### Step 2: Install Jenkins on Server
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y jenkins docker.io

# Add Jenkins user to docker group
sudo usermod -aG docker jenkins

# Start services
sudo systemctl start jenkins
sudo systemctl start docker
```

### Step 3: Configure Jenkins Pipeline
1. Open Jenkins at `http://your-server:8080`
2. Click "New Item" → Enter "Email Crawler Pipeline"
3. Select "Pipeline" → Click "OK"
4. In "Pipeline" section:
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: Your GitHub repo URL
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
5. Click "Save"
6. Click "Build Now" to test

### Step 4: Set Up Nightly Schedule
1. In Jenkins job → "Configure"
2. Scroll to "Build Triggers"
3. Check "Build periodically"
4. Enter cron: `0 22 * * *` (10 PM every day)
5. Save

---

## 📂 File Structure
```
EmailDocker/
├── app.py                          # Flask web app
├── dashboard.html                  # Upload dashboard
├── login.html                      # Login page
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container config
├── Jenkinsfile                     # CI/CD pipeline
├── docker-compose.yml              # Local dev setup
├── .gitignore                      # Git ignore rules
│
├── AICrawler2/
│   └── AICrawler2/
│       └── emailcrawler/
│           ├── websites.txt        # Input URLs
│           └── emailcrawler/
│               ├── spiders/
│               │   └── email_spider.py
│               ├── settings.py
│               ├── pipelines.py
│               └── items.py
│
├── uploads/                        # Uploaded files (git ignored)
└── output/                         # Crawl results (git ignored)
```

---

## 🔄 Workflow

### For Users (Web UI)
1. Go to http://your-server:5000
2. Login (admin/admin123)
3. Upload `websites.txt` with URLs
4. System automatically commits to Git
5. Jenkins runs crawler at 10 PM
6. Results available by morning in Git repo

### For Jenkins (Automated)
```
10:00 PM → Jenkins trigger
    ↓
Pull latest code from Git
    ↓
Build Docker image
    ↓
Run Scrapy crawler
    ↓
Extract emails
    ↓
Commit results to Git
    ↓
Morning → Download results
```

---

## 📊 Monitoring

### Check Crawler Status
```bash
# View Docker container logs
docker logs email-crawler:latest

# Check if container ran successfully
docker ps -a | grep email-crawler
```

### Jenkins Logs
1. Open Jenkins → Click job
2. Click "Build History" → Select build number
3. Click "Console Output"

### Git Verification
```bash
git log --oneline | head -10  # See latest commits
```

---

## 🛠️ Customization

### Change Crawler Schedule
Edit `Jenkinsfile` → Line: `cron('0 22 * * *')`
- `0 22 * * *` → 10 PM daily
- `0 6 * * *` → 6 AM daily
- `0 */4 * * *` → Every 4 hours
- `0 0 * * 0` → Sunday at midnight

### Increase Crawler Timeout
Edit `Jenkinsfile` → `timeout(time: 2, unit: 'HOURS')`

### Add Email Notifications
Uncomment in `Jenkinsfile`:
```groovy
emailext(
    subject: "✅ Email Crawler Success",
    body: "Results: ${BUILD_LOG_EXCERPT}",
    to: "your-email@example.com"
)
```

---

## ⚠️ Troubleshooting

### Docker build fails
```bash
# Clear cache and rebuild
docker system prune -a
docker build --no-cache -t email-crawler:latest .
```

### Jenkins can't connect to Docker
```bash
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Git push fails in Jenkins
```bash
# Configure Git credentials in Jenkins:
# Manage Jenkins → Credentials → Add SSH key or Token
```

### Crawler finds no emails
1. Check `websites.txt` format (one URL per line)
2. Verify URLs are accessible
3. Check `output/results.json` for raw data
4. Review logs: `docker logs email-crawler:latest`

---

## 📞 Support
For issues, check:
- Jenkins console logs
- Docker container logs
- Git commit history
- `output/results.json` for data structure

Good luck! 🚀
