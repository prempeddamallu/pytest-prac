pipeline {
    agent any

    environment {
        // Set the name of the Docker image
        IMAGE_NAME = 'my-python-app'
        IMAGE_TAG = 'latest'
        // Set the container name (you can change this in Jenkins job configuration or set a default value)
        CONTAINER_NAME = 'python-app-container'  // Default container name
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout the code from your repository
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile in the repository
                    echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the Docker container with the specified container name
                    echo "Running Docker container with name: ${CONTAINER_NAME}"
                    sh "docker run --name ${CONTAINER_NAME} ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker images and containers after the build (optional)
            echo "Cleaning up Docker images and containers"
            sh "docker rm ${CONTAINER_NAME} || true"  // Remove the container if it exists
            sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"  // Remove the image if it exists
        }

        success {
            echo "Build and tests were successful"
        }

        failure {
            echo "Build or tests failed"
        }
    }
}
