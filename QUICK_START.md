# 🚀 Email Crawler - Quick Start Guide

**Repository:** https://github.com/mahendra-csm/EmailAutomatoin

---

## ✅ Status: READY FOR DEPLOYMENT

All files have been pushed to GitHub. Your infrastructure is now:
- ✅ Docker containerized
- ✅ Jenkins-ready
- ✅ Git integrated
- ✅ Production-configured

---

## 🎯 LOCAL TESTING (Windows/Mac/Linux)

### Option 1: Test with Docker Locally

```bash
# Navigate to your project
cd c:\Users\WELCOME\OneDrive\Desktop\EmailDocker\temp_repo

# Build Docker image
docker build -t email-crawler:latest .

# Test the crawler (requires websites.txt in the right path)
docker run --rm ^
  -v "%cd%\AICrawler2\AICrawler2\emailcrawler\emailcrawler\websites.txt:/app/crawler/websites.txt" ^
  -v "%cd%\output:/app/output" ^
  email-crawler:latest
```

### Option 2: Use Docker Compose (Recommended)

```bash
# Start Flask web + Jenkins
docker-compose up -d

# Access:
# - Flask UI: http://localhost:5000 (Login: admin/admin123)
# - Jenkins: http://localhost:8080
# - Stop: docker-compose down
```

---

## 🖥️ PRODUCTION SETUP (Linux Server / AWS EC2)

### Step 1: Clone Repository on Server

```bash
cd /home/ubuntu
git clone https://github.com/mahendra-csm/EmailAutomatoin.git EmailCrawler
cd EmailCrawler
```

### Step 2: Install Docker

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io docker-compose git

# Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Step 3: Install Jenkins

```bash
# Install Java (required for Jenkins)
sudo apt-get install -y openjdk-11-jdk

# Install Jenkins
sudo apt-get install -y jenkins

# Start Jenkins service
sudo systemctl start jenkins
sudo systemctl enable jenkins  # Auto-start on reboot

# Check status
sudo systemctl status jenkins

# Get initial password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Step 4: Configure Jenkins

1. **Open Jenkins:**
   ```
   http://your-server-ip:8080
   ```

2. **Paste the initial password** from the output above

3. **Install suggested plugins** (recommended)

4. **Create admin account**

5. **Create new Pipeline job:**
   - Click **"New Item"**
   - Name: `EmailCrawler-Pipeline`
   - Select **Pipeline**
   - Click **OK**

6. **Configure Pipeline:**

   In the **Pipeline** section, select:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/mahendra-csm/EmailAutomatoin.git`
   - Credentials: Add GitHub credentials (if private repo)
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`

7. **Set Build Triggers:**

   Check `Build periodically` and enter cron:
   ```
   0 22 * * *    # 10 PM daily
   ```

   Other examples:
   ```
   0 6 * * *     # 6 AM daily
   0 0 * * *     # Midnight daily
   0 */4 * * *   # Every 4 hours
   H H * * *     # Random time daily
   ```

8. **Save** and test by clicking **Build Now**

---

## 📋 DIRECTORY STRUCTURE

```
EmailAutomatoin/
├── app.py                          # Flask web application
├── Dockerfile                      # Docker container config
├── Jenkinsfile                     # CI/CD pipeline
├── docker-compose.yml              # Local dev environment
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── .env.example                    # Configuration template
│
├── HTML Templates/
├── dashboard.html                  # Upload dashboard
├── login.html                      # Login page  
├── success.html                    # Success page
│
├── AICrawler2/                     # Scrapy project
│   └── AICrawler2/emailcrawler/
│       ├── websites.txt            # URLs to crawl (INPUT)
│       ├── extracted_emails.txt    # Results (OUTPUT)
│       └── emailcrawler/
│           ├── spiders/
│           │   └── email_spider.py # Main crawler
│           ├── settings.py
│           ├── pipelines.py
│           └── items.py
│
├── output/                         # Crawl results (git ignored)
└── uploads/                        # Uploaded files (git ignored)
```

---

## 🔄 WORKFLOW

### Daily Automation:

```
10:00 PM (Nightly)
  ↓
Jenkins trigger activates
  ↓
Clone latest repo from GitHub
  ↓
Build Docker image
  ↓
Run Scrapy crawler
  ↓
Extract emails from websites.txt
  ↓
Save results to output/results.json
  ↓
Auto-commit results to GitHub
  ↓
MORNING: Download results!
```

### Manual Upload (via Web UI):

```
1. Go to http://your-server:5000
2. Login with credentials
3. Upload websites.txt
4. Flask automatically:
   - Copies file to crawler
   - Commits to GitHub
   - Ready for next nightly run
```

---

## ⚙️ CONFIGURATION

### Edit Environment Variables

```bash
# Copy example to actual config
cp .env.example .env

# Edit with your values
nano .env
```

Key variables:
```
SECRET_KEY=your-secret-key           # Flask session key
USERNAME=admin                       # Web UI username
PASSWORD=admin123                    # Web UI password
CRAWLER_PATH=/path/to/crawler        # Where Scrapy project lives
WEBSITES_FILE=/path/to/websites.txt  # Input file for URLs
```

### Change Crawler Schedule

Edit `Jenkinsfile` line with cron schedule:
```groovy
cron('0 22 * * *')  # Change the time here
```

---

## 📊 MONITORING

### Check Last 10 Git Commits

```bash
git log --oneline -10
```

### View Jenkins Build Logs

1. Go to Jenkins job
2. Click on build number
3. Click **Console Output**

### Check Docker Container Status

```bash
docker ps -a | grep email-crawler
docker logs email-crawler:latest
```

### View Crawl Results

```bash
# JSON results
cat output/results.json

# Extracted emails
cat AICrawler2/AICrawler2/emailcrawler/emailcrawler/extracted_emails.txt
```

---

## 🆘 TROUBLESHOOTING

### Problem: Docker image won't build
```bash
docker system prune -a
docker build --no-cache -t email-crawler:latest .
```

### Problem: Jenkins can't connect to Docker
```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Problem: Git push fails in Jenkins
```bash
# Configure SSH key or token in Jenkins:
# Manage Jenkins → Credentials → Add SSH key
# OR use GitHub token (Settings → Developer settings → Personal access tokens)
```

### Problem: Crawler finds no emails
1. Check `websites.txt` format (one URL per line)
2. Verify URLs are valid and accessible
3. Check if Scrapy settings in `settings.py` need adjustment
4. Review `output/results.json` for raw data

### Problem: Permission denied on Linux
```bash
sudo chown -R $USER:$USER /path/to/EmailCrawler
chmod -R u+w /path/to/EmailCrawler
```

---

## 🎓 WHAT HAPPENS EACH NIGHT AT 10 PM

1. **Jenkins Trigger** → Pipeline starts
2. **Git Checkout** → Pulls latest code
3. **Docker Build** → Creates container image
4. **Crawler Run** → Reads `websites.txt`, extracts emails
5. **Results Save** → Outputs to `results.json`
6. **Git Commit** → Commits results with timestamp
7. **Git Push** → Pushes to GitHub
8. **Cleanup** → Removes old Docker images

**Result:** By morning, you have `extracted_emails.txt` ready to download!

---

## 📝 NEXT ACTIONS

### Immediate (Today):
- [ ] Test Docker locally with `docker-compose up`
- [ ] Verify Flask UI works at http://localhost:5000
- [ ] Upload test `websites.txt` via UI

### This Week:
- [ ] Set up Linux server or AWS EC2
- [ ] Install Docker + Jenkins
- [ ] Create Pipeline job in Jenkins
- [ ] Configure nightly trigger (cron)
- [ ] Test first automated run

### For Production:
- [ ] Update `.env` with production values
- [ ] Add SSL certificate (HTTPS)
- [ ] Set up email notifications
- [ ] Configure backups for results
- [ ] Monitor Jenkins logs

---

## 📞 QUICK REFERENCE

| Task | Command |
|------|---------|
| View git log | `git log --oneline` |
| Check Docker status | `docker ps -a` |
| Stop all containers | `docker stop $(docker ps -aq)` |
| Clean up Docker | `docker system prune` |
| View Flask logs | `docker logs flask-app` |
| Rebuild image | `docker build -t email-crawler:latest .` |
| Test crawler | `docker run --rm -v ...` |
| Check Jenkins status | `sudo systemctl status jenkins` |
| View Jenkins logs | `sudo tail -f /var/log/jenkins/jenkins.log` |

---

## 🎉 YOU'RE ALL SET!

Your Email Crawler is now:
- ✅ Containerized with Docker
- ✅ Automated with Jenkins
- ✅ Version controlled with Git
- ✅ Production-ready

**Repository:** https://github.com/mahendra-csm/EmailAutomatoin

Good luck! 🚀
