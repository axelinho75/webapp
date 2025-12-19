pipeline {
    agent {
        docker {
            image 'python:3.14-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    echo '========== Installation de UV et des dépendances =========='
                    sh '''
                        apt-get update
                        apt-get install -y \
                            curl \
                            wget \
                            gnupg \
                            unzip \
                            chromium-browser \
                            chromium-driver
                        
                        pip install --upgrade uv
                        uv sync --dev
                    '''
                }
            }
        }

        stage('Lint & Code Quality') {
            steps {
                script {
                    echo '========== Vérification du code =========='
                    sh '''
                        uv pip install flake8 pylint
                        uv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                        uv run pylint **/*.py || true
                    '''
                }
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    echo '========== Exécution des tests unitaires =========='
                    sh '''
                        uv run pytest unit_side_function.py -v --tb=short
                    '''
                }
            }
        }

        stage('Integration Tests') {
            steps {
                script {
                    echo '========== Exécution des tests d\'intégration =========='
                    sh '''
                        uv run pytest test_nowebrowserapp.py test_webapp.py -v --tb=short
                    '''
                }
            }
        }

        stage('Start Flask App') {
            steps {
                script {
                    echo '========== Démarrage de l\'application Flask =========='
                    sh '''
                        nohup uv run python main.py > flask_app.log 2>&1 &
                        sleep 3
                        curl -f http://localhost:5000/ || echo "Flask app not yet ready"
                    '''
                }
            }
        }

        stage('Selenium Tests') {
            steps {
                script {
                    echo '========== Exécution des tests Selenium =========='
                    sh '''
                        uv run pytest webapp_test.py -v --tb=short
                    '''
                }
            }
        }

        stage('Report') {
            steps {
                script {
                    echo '========== Génération des rapports =========='
                    sh '''
                        uv pip install pytest-html
                        uv run pytest . -v --html=report.html --self-contained-html || true
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                echo '========== Nettoyage =========='
                sh 'pkill -f "python main.py" || true'
            }
            
            junit allowEmptyResults: true, testResults: 'test-results.xml'
            
            archiveArtifacts artifacts: 'report.html,flask_app.log', 
                             allowEmptyArchive: true
        }

        success {
            echo '✅ Pipeline réussi !'
        }

        failure {
            echo '❌ Pipeline échoué - Vérifiez les logs'
        }

        cleanup {
            cleanWs()
        }
    }
}