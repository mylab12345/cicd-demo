pipeline {
    agent any

    environment {
        IMAGE_NAME = "cicd-demo"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKERHUB_USER = "dockerhub_mydockerkdb"   // replace with your Docker Hub username
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

        stage('Docker Build & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                    docker build -t $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG .
                    docker tag $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG $DOCKERHUB_USER/$IMAGE_NAME:latest

                    docker push $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG
                    docker push $DOCKERHUB_USER/$IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                sh '''
                # Create namespace if not exists
                kubectl get ns $K8S_NAMESPACE || kubectl apply -f k8s/namespace.yaml

                # Update manifests to use Docker Hub image
                sed -i "s|image:.*|image: $DOCKERHUB_USER/$IMAGE_NAME:latest|" k8s/deployment.yaml

                # Apply manifests
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml

                # Wait for rollout
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
