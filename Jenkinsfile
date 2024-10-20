pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Wahab901278/stock-exchange-project.git', branch: 'main'
            }
        }
        stage('Set up Python') {
            steps {
                script {
                    // Install Python if needed (depends on your Jenkins setup)
                    sh 'sudo apt-get update'
                    sh 'sudo apt-get install -y python3.11 python3-pip'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m pytest testing/test_app.py'
                sh 'python -m pytest testing/test_flask_api.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t Wahab901278/stockexchange-app:latest .'
            }
        }

        stage('Log in to Docker Hub') {
            steps {
                script {
                    // Login to Docker Hub
                    def username = credentials('DOCKER_USERNAME') // Use Jenkins credentials store
                    def password = credentials('DOCKER_PASSWORD')
                    sh "echo ${password} | docker login -u ${username} --password-stdin"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push Wahab901278/stockexchange-app:latest'
            }
        }
    }

    post {
        always {
            echo 'This will always run after the pipeline stages'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
