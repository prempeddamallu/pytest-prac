pipeline {
    agent any

    environment {
        // Set the name of the Docker image
        IMAGE_NAME = 'my-python-app'
        IMAGE_TAG = 'latest'
        // Set the container name (you can change this in Jenkins job configuration or set a default value)
        CONTAINER_NAME = 'python-app-container'  // Default container name
        // Docker Hub credentials (configured in Jenkins)
        DOCKER_CREDENTIALS_ID = 'dockerhub' // The Jenkins credential ID for Docker Hub
        DOCKER_USERNAME = 'premdatagrokr' // Docker Hub username (replace with your actual username)
        DOCKER_REPO = 'premdatagrokr/my-python-app'  // Docker Hub repository name (replace with your actual repo)
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
                    sh "docker run --name ${CONTAINER_NAME} -d ${IMAGE_NAME}:${IMAGE_TAG}"

                    // Give it a moment to start
                    sleep(5)

                    // Fetch and print the logs
                    echo 'Container logs:'
                    sh "docker logs ${CONTAINER_NAME}" // Use double quotes to expand variables
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
                    
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                        // Push the Docker image
                        sh "docker push ${DOCKER_REPO}:${IMAGE_TAG}"// Use double quotes
                    }
                }
                
            }
        }
        stage('Clean Up') {
            steps {
                script {
                    try {
                        // Clean up Docker images and containers after the build (optional)
                        echo "Cleaning up Docker images and containers"
                        sh "docker stop ${CONTAINER_NAME} || true" // Stop the container
                        sh "docker rm ${CONTAINER_NAME} || true"  // Remove the container if it exists
                        sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"  // Remove the image if it exists
                        sh "docker rmi ${DOCKER_REPO}:${IMAGE_TAG} || true" // Remove the tagged image locally
                    } catch (Exception e) {
                        error "Failed to clean up Docker resources: ${e.message}"
                    }
                }
            }
        }
    }

    

    post {
        success {
            echo "Build, tests, and Docker push were successful"
        }

        failure {
            echo "Build, tests, or Docker push failed"
        }
    }
}
