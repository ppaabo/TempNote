pipeline {
    agent any

    environment {
        PYTHON_ENV = 'venv'
        BACKEND_PATH = '/workspace/backend'
        NGINX_CONF = '/workspace/deploy/nginx/nginx.conf'
        DB_IMAGE_PATH = '/workspace/deploy/docker/db'
    }

    tools {
        nodejs 'NodeJS 22'
    }

    stages {

        stage('Python: Bandit & Safety Scans') {
            steps {
                sh '''
                    echo "Creating Python virtual environment..."
                    python3 -m venv ${PYTHON_ENV}
                    . ${PYTHON_ENV}/bin/activate

                    echo "Installing bandit and safety..."
                    pip install -r ${BACKEND_PATH}/requirements.txt
                    pip install bandit safety

                    echo "Running Bandit..."
                    bandit -r ${BACKEND_PATH} || true

                    echo "Running Safety ('safety scan' requires login)..."
                    safety check -r ${BACKEND_PATH}/requirements.txt || true
                '''
            }
        }

        stage('Frontend: Dependency Scan') {
            steps {
                dir('/workspace/frontend') {
                    sh '''
                        echo "Running npm audit..."
                        npm install
                        npm audit --audit-level=moderate || true

                        echo "Running retire.js..."
                        retire || true
                    '''
                }
            }
        }

        stage('Nginx: Config Scan') {
            steps {
                sh '''
                    echo "Running Gixy on nginx.conf..."
                    gixy ${NGINX_CONF} || true
                '''
            }
        }

        stage('PostgreSQL: Docker Image Scan') {
            steps {
                sh '''
                    echo "Building PostgreSQL image locally..."
                    docker build -t local-postgres-image /workspace/deploy/docker/db

                    echo "Running Trivy image scan..."
                    trivy image local-postgres-image || true

                    echo "Running Trivy config scan..."
                    trivy config /workspace/deploy/docker/db || true
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
    }
}