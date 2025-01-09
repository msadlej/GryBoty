pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Branch name: ${env.gitlabSourceBranch}"
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

