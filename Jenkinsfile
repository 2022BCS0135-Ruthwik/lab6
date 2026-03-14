pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "2022bcs0135/wine-mlops-2022bcs0135_lab6"
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the GitHub repository using Jenkins SCM.
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python scripts/train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    env.CURRENT_ACCURACY = sh(script: "jq '.accuracy' app/artifacts/metrics.json", returnStdout: true).trim()
                    echo "Current Accuracy: ${env.CURRENT_ACCURACY}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                withCredentials([string(credentialsId: 'best-accuracy', variable: 'BASELINE')]) {
                    script {
                        def isBetter = sh(script: "echo \"${env.CURRENT_ACCURACY} > ${BASELINE}\" | bc", returnStdout: true).trim()
                        if (isBetter == "0") {
                            echo "Current accuracy (${env.CURRENT_ACCURACY}) is not better than baseline (${BASELINE}). Skipping Docker build."
                            env.SKIP_DOCKER = "true"
                        } else {
                            echo "Current accuracy (${env.CURRENT_ACCURACY}) is better than baseline (${BASELINE}). Proceeding with Docker build."
                            env.SKIP_DOCKER = "false"
                        }
                    }
                }
            }
        }

        stage('Build Docker Image (Conditional)') {
            when {
                environment name: 'SKIP_DOCKER', value: 'false'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker build -t ${DOCKER_IMAGE}:latest -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .
                    '''
                }
            }
        }

        stage('Push Docker Image (Conditional)') {
            when {
                environment name: 'SKIP_DOCKER', value: 'false'
            }
            steps {
                sh '''
                    docker push ${DOCKER_IMAGE}:latest
                    docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', allowEmptyArchive: false
        }
    }
}
