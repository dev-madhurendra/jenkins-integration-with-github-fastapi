pipeline {
    agent any
    
    environment {
        PYTHON_BIN = '/usr/bin/python3'  // Path to Python binary
        VENV_DIR = 'venv'  // Virtual environment directory
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/dev-madhurendra/jenkins-integration-with-github-fastapi.git']]])
            }
        }
        
        stage('Setup') {
            steps {
                // Set up virtual environment
                sh "${PYTHON_BIN} -m venv ${VENV_DIR}"
                sh "${VENV_DIR}/bin/pip install -r requirements.txt"
            }
        }
        
        
        stage('Run Application') {
            steps {
                // Run FastAPI application
                sh "${VENV_DIR}/bin/python3 main.py"
                sh "${VENV_DIR}/bin/uvicorn main:app --reload"
            }
        }
    }
}
