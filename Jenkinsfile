pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 15, unit: 'MINUTES')
    }

    environment {
        STUDENT_NAME = 'Temirlan'
        STUDENT_SURNAME = 'Alzhan'
        STUDENT_GROUP = 'IT2-2307'
        STUDENT_ID = '38372'
        IMAGE_NAME = 'alzhan-temirlan-devops'
        CONTAINER_NAME = 'alzhan-temirlan-container'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.SOURCE_COMMIT = sh(
                        script: 'git rev-parse HEAD',
                        returnStdout: true
                    ).trim()
                    env.IMAGE_TAG = env.SOURCE_COMMIT.take(12)
                }
                sh '''
                    set -eu
                    echo "Source commit: $SOURCE_COMMIT"
                    echo "Student: $STUDENT_NAME $STUDENT_SURNAME"
                    echo "Group: $STUDENT_GROUP"
                    echo "Student ID: $STUDENT_ID"
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'python3 -m compileall -q app'
            }
        }

        stage('Test') {
            steps {
                sh "python3 -m unittest discover -s app -p 'test_*.py' -v"
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -eu
                    docker build --progress=plain \
                      --label "org.opencontainers.image.revision=$SOURCE_COMMIT" \
                      -t "$IMAGE_NAME:$IMAGE_TAG" \
                      -t "$IMAGE_NAME:latest" .
                    docker images "$IMAGE_NAME"
                '''
            }
        }

        stage('Docker Run') {
            steps {
                sh '''
                    set -eu

                    if docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
                        docker rm -f "$CONTAINER_NAME"
                    fi

                    docker run -d --name "$CONTAINER_NAME" \
                      -p 127.0.0.1:8000:8000 \
                      -e STUDENT_NAME -e STUDENT_SURNAME \
                      -e STUDENT_GROUP -e STUDENT_ID \
                      "$IMAGE_NAME:$IMAGE_TAG"

                    curl --fail --silent --show-error \
                      --retry 10 --retry-connrefused \
                      --retry-delay 1 --max-time 3 \
                      http://127.0.0.1:8000/ \
                      -o application-response.txt

                    cat application-response.txt
                    grep -Fx "Name: $STUDENT_NAME" application-response.txt
                    grep -Fx "Surname: $STUDENT_SURNAME" application-response.txt
                    grep -Fx "Group: $STUDENT_GROUP" application-response.txt
                    grep -Fx "Student ID: $STUDENT_ID" application-response.txt
                    grep -Fx "Application is running successfully!" application-response.txt

                    curl -fsS --max-time 3 http://127.0.0.1:8000/health

                    docker ps --filter "name=^/$CONTAINER_NAME$"
                    docker logs "$CONTAINER_NAME"
                    docker image inspect "$IMAGE_NAME:$IMAGE_TAG" --format '{{.Id}}'
                    docker inspect "$CONTAINER_NAME" --format '{{.Image}}'
                    echo "Deployed source commit: $SOURCE_COMMIT"
                '''
            }
        }
    }

    post {
        failure {
            sh 'docker logs "$CONTAINER_NAME" 2>/dev/null || true'
        }
    }
}
