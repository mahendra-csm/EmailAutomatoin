import os
import shutil
import subprocess
from datetime import datetime

from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "supersecretkey")

USERNAME = os.getenv('USERNAME', "admin")
PASSWORD = os.getenv('PASSWORD', "admin123")

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
CRAWLER_PATH = os.getenv('CRAWLER_PATH', "/home/ubuntu/EmailScrapy-OG")
WEBSITES_FILE = os.getenv('WEBSITES_FILE', os.path.join(CRAWLER_PATH, "emailcrawler/websites.txt"))

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():

    username = request.form['username']
    password = request.form['password']
    if username == USERNAME and password == PASSWORD:
        session['user'] = username
        return redirect('/dashboard')

    return render_template('login.html', error='Invalid username or password')


@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/')

    return render_template('dashboard.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect('/')

    file = request.files.get('file')
    message = request.form.get('message', 'Upload via web UI')
    
    if not file or file.filename == '':
        return render_template('dashboard.html', error='No file selected')

    try:
        # Save uploaded file
        upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(upload_path)
        logger.info(f"File uploaded: {upload_path}")

        # Copy to crawler directory
        os.makedirs(os.path.dirname(WEBSITES_FILE), exist_ok=True)
        shutil.copy(upload_path, WEBSITES_FILE)
        logger.info(f"File copied to: {WEBSITES_FILE}")

        # Git operations
        try:
            subprocess.run(["git", "config", "user.email", "webapp@example.com"], cwd=CRAWLER_PATH, check=True)
            subprocess.run(["git", "config", "user.name", "Web App"], cwd=CRAWLER_PATH, check=True)
            subprocess.run(["git", "add", "."], cwd=CRAWLER_PATH, check=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"📤 {message} - {timestamp}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=CRAWLER_PATH, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=CRAWLER_PATH, check=True)
            
            logger.info("Git push successful")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git operation warning: {e}")
            # Don't fail the upload if git has issues

        return render_template(
            'success.html',
            filename=file.filename,
            message=message,
            timestamp=timestamp
        )

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return render_template('dashboard.html', error=f'Upload failed: {str(e)}'), 400
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/health')
def health():
    """Health check endpoint for Docker/Kubernetes"""
    return {'status': 'ok'}, 200


@app.errorhandler(404)
def not_found(error):
    return render_template('login.html', error='Page not found'), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {error}")
    return render_template('login.html', error='Server error'), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)