pipeline {
    agent any

    environment {
        IMAGE_NAME = "cicd-demo"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        K8S_NAMESPACE = "cicd"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/mylab12345/cicd-demo.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                python3 -m venv venv
                ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                ./venv/bin/pytest test_app.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                '''
            }
        }

        stage('Load Image into Minikube') {
            steps {
                sh '''
                # Ensure Minikube is running
                minikube status || minikube start --driver=docker

                # Load images into Minikube’s Docker
                minikube image load $IMAGE_NAME:$IMAGE_TAG
                minikube image load $IMAGE_NAME:latest
                '''
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                sh '''
                # Create namespace if not exists
                kubectl get ns $K8S_NAMESPACE || kubectl apply -f k8s/namespace.yaml

                # Apply deployment and service manifests
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml

                # Wait for rollout to complete
                kubectl rollout status deployment/$IMAGE_NAME -n $K8S_NAMESPACE --timeout=120s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                kubectl get pods -n $K8S_NAMESPACE
                kubectl get svc -n $K8S_NAMESPACE
                '''
            }
        }
    }
}
