pipeline {
    agent any
    
    options {
        timeout(time: 2, unit: 'HOURS')
        timestamps()
    }
    
    triggers {
        // Runs every night at 10 PM
        cron('0 22 * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out repository...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🔨 Building Docker image...'
                script {
                    sh 'docker build -t email-crawler:${BUILD_NUMBER} .'
                }
            }
        }
        
        stage('Run Crawler') {
            steps {
                echo '🕷️ Running email crawler...'
                script {
                    sh '''
                        mkdir -p output
                        docker run --rm \
                            -v $(pwd)/AICrawler2/AICrawler2/emailcrawler/emailcrawler/websites.txt:/app/crawler/websites.txt \
                            -v $(pwd)/output:/app/output \
                            email-crawler:${BUILD_NUMBER}
                    '''
                }
            }
        }
        
        stage('Process Results') {
            steps {
                echo '📊 Processing results...'
                script {
                    sh '''
                        # Move results to output folder if crawler created them
                        if [ -f output/results.json ]; then
                            echo "✅ Crawler completed successfully"
                        else
                            echo "⚠️ No results found, checking extraction..."
                        fi
                    '''
                }
            }
        }
        
        stage('Commit & Push Results') {
            steps {
                echo '💾 Committing results to Git...'
                script {
                    sh '''
                        git config user.email "jenkins@example.com"
                        git config user.name "Jenkins Bot"
                        
                        git add output/
                        git add AICrawler2/AICrawler2/emailcrawler/emailcrawler/extracted_emails.txt
                        
                        if [ -n "$(git status --porcelain)" ]; then
                            git commit -m "🤖 Automated crawl results - $(date '+%Y-%m-%d %H:%M:%S')"
                            git push origin main || git push origin master
                            echo "✅ Results pushed to repository"
                        else
                            echo "⏭️ No changes to commit"
                        fi
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo '🧹 Cleaning up...'
            sh 'docker rmi email-crawler:${BUILD_NUMBER} || true'
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
            // Optional: Send email notification
            // emailext(subject: "✅ Email Crawler Success", body: "Crawling completed. Results available.")
        }
        
        failure {
            echo '❌ Pipeline failed!'
            // Optional: Send email notification
            // emailext(subject: "❌ Email Crawler Failed", body: "Check Jenkins logs for details.")
        }
    }
}
