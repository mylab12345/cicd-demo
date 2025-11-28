pipeline {
    agent any

    environment {
        IMAGE_NAME = "cicd-demo"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKERHUB_USER = "mydockerkdb"   // replace with your Docker Hub username
        K8S_NAMESPACE = "cicd"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${env.BRANCH_NAME}", url: 'https://github.com/mylab12345/cicd-demo.git'
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

        stage('Code Quality') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh '''
                    ./venv/bin/pip install pylint
                    ./venv/bin/pylint app.py > pylint-report.txt || true
                    '''
                }
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

        stage('Blue/Green Deploy') {
            steps {
                script {
                    def activeColor = sh(script: "kubectl get svc cicd-demo -n $K8S_NAMESPACE -o=jsonpath='{.spec.selector.version}'", returnStdout: true).trim()
                    def newColor = (activeColor == "blue") ? "green" : "blue"

                    sh """
                    kubectl apply -f k8s/deployment-${newColor}.yaml
                    kubectl rollout status deployment/cicd-demo-${newColor} -n $K8S_NAMESPACE --timeout=120s
                    kubectl patch svc cicd-demo -n $K8S_NAMESPACE -p '{\"spec\":{\"selector\":{\"app\":\"cicd-demo\",\"version\":\"${newColor}\"}}}'
                    """
                }
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

    post {
        always {
            echo "Pipeline finished with status: ${currentBuild.currentResult}"
        }
    }
}
