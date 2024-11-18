pipeline {
    agent any

    environment {
        // Set the name of the Docker image
        IMAGE_NAME = 'my-python-app'
        IMAGE_TAG = 'latest'
        // Set the container name (you can change this in Jenkins job configuration or set a default value)
        CONTAINER_NAME = 'python-app-container'  // Default container name
        // Docker Hub credentials (configured in Jenkins)
        DOCKER_HUB_CREDENTIALS = 'dockerhub' // The Jenkins credential ID for Docker Hub
        DOCKER_USERNAME = 'your-docker-username'          // Docker Hub username
        DOCKER_REPO = 'premdatagrokr/my-python-app'  // Docker Hub repository name
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

        stage('Login to Docker Hub') {
            steps {
                script {
                    // Login to Docker Hub using Jenkins credentials
                    echo "Logging in to Docker Hub"
                    withCredentials([usernamePassword(credentialsId: DOCKER_HUB_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin"
                    }
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    // Tag the image with the Docker Hub repository name
                    echo "Tagging image for Docker Hub"
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REPO}:${IMAGE_TAG}"
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Push the image to Docker Hub
                    echo "Pushing Docker image to Docker Hub"
                    sh "docker push ${DOCKER_REPO}:${IMAGE_TAG}"
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
            sh "docker rmi ${DOCKER_REPO}:${IMAGE_TAG} || true" // Remove the tagged image locally
        }

        success {
            echo "Build, tests, and Docker push were successful"
        }

        failure {
            echo "Build, tests, or Docker push failed"
        }
    }
}
