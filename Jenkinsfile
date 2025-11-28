pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/mylab12345/cicd-demo.git'
            }
        }

        stage('Build') {
            steps {
                sh '''#!/bin/bash
                python3 -m venv venv
                ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''#!/bin/bash
                ./venv/bin/pytest test_app.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker build -t cicd-demo .
                docker stop cicd-demo || true
                docker rm cicd-demo || true
                docker run -d --name cicd-demo -p 5010:5000 cicd-demo
                '''
            }
        }
    }
}
