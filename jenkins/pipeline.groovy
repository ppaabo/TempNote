pipeline {
    agent any

    environment {
        PYTHON_ENV = 'venv'
        BACKEND_PATH = '/workspace/backend'
        NGINX_CONF = '/workspace/prod/frontend/nginx.conf'
        DB_IMAGE_PATH = '/workspace/prod/db'
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
                    bandit -r ${BACKEND_PATH} -f json -o bandit-report.json || true

                    echo "Running Safety ('safety scan' requires login)..."
                    safety check -r ${BACKEND_PATH}/requirements.txt --json > safety-report.json || true
                '''
            }
        }

        stage('Frontend: Dependency Scan') {
            steps {
                dir('/workspace/frontend') {
                    sh '''
                        echo "Running npm audit..."
                        npm install
                        npm audit --audit-level=moderate --json > audit-report.json || true

                        echo "Running retire.js..."
                        retire --outputformat cyclonedx  > /workspace/frontend/retire-report.json || true
                        cp /workspace/frontend/*-report.* ${WORKSPACE}/
                    '''
                }
            }
        }

        stage('Nginx: Config Scan') {
            steps {
                sh '''
                    echo "Running Gixy on nginx.conf..."
                    gixy -f json -o gixy-report.json ${NGINX_CONF} || true
                '''
            }
        }

        stage('Backend & Frontend: Docker Image Scan') {
            steps {
                sh '''
                    echo "Building Backend image..."
                    docker build -t local-backend-image -f /workspace/prod/backend/Dockerfile /workspace

                    echo "Scanning Backend image with Trivy..."
                    trivy image --format template --template '@/usr/local/share/trivy/templates/html.tpl' -o backend-image-report.html local-backend-image || true

                    echo "Building Frontend image..."
                    docker build -t local-frontend-image -f /workspace/prod/frontend/Dockerfile /workspace

                    echo "Scanning Frontend image with Trivy..."
                    trivy image --format template --template '@/usr/local/share/trivy/templates/html.tpl' -o frontend-image-report.html local-frontend-image || true
                '''
            }
        }

        stage('PostgreSQL: Docker Image & Config Scan') {
                steps {
                    sh '''
                        echo "Building PostgreSQL image locally..."
                        docker build -t local-postgres-image -f ${DB_IMAGE_PATH}/Dockerfile /workspace

                        echo "Running Trivy image scan..."
                        trivy image --format template --template '@/usr/local/share/trivy/templates/html.tpl' -o db-image-report.html local-postgres-image || true

                        echo "Running Trivy config scan..."
                        trivy config --format template --template '@/usr/local/share/trivy/templates/html.tpl' -o db-config-report.html ${DB_IMAGE_PATH} || true
                    '''
                }
        }
    }
        post {
            always {
                echo 'Pipeline completed.'
                archiveArtifacts artifacts: '**/*-report.json, **/*-report.html', allowEmptyArchive: true
            }
        }
}