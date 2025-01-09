pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
    }
    environment {
        DOCKER_TESTS_DIR = 'docker/tests'
        BACKEND_TESTS_DIR = 'backend/tests'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Branch name: ${env.gitlabSourceBranch}"
            }
        }
        stage('Setup Docker Tests Environment') {
            steps {
                echo 'Installing requirements for docker tests...'
                dir("${DOCKER_TESTS_DIR}") {
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Run Docker Tests') {
            steps {
                echo 'Running unit tests with unittest...'
                dir("${DOCKER_TESTS_DIR}") {
                    sh 'python -m unittest discover -s . -p "*.py"'
                }
            }
        }
        stage('Setup Backend Tests Environment') {
            steps {
                echo 'Installing requirements for backend tests...'
                dir("${BACKEND_TESTS_DIR}") {
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Run Backend Tests') {
            steps {
                echo 'Running backend tests with pytest...'
                dir("${BACKEND_TESTS_DIR}") {
                    sh 'pytest'
                }
            }
        }
    }
    post {
        success {
            updateGitlabCommitStatus(name: 'Pipeline', state: 'success')
        }
        failure {
            updateGitlabCommitStatus(name: 'Pipeline', state: 'failed')
        }
        always {
            echo 'Pipeline completed.'
            cleanWs()
        }
    }
}

