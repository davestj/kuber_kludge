pipeline {
    agent any

    stages {
        stage('Delete Sidecar') {
            steps {
                script {
                    sh 'python3.11 kuber_kludge.py --kubeconfig ~/.kube/config --delete-sidecar'
                }
            }
        }
        stage('Delete Ingress') {
            steps {
                script {
                    sh 'python3.11 kuber_kludge.py --kubeconfig ~/.kube/config --delete-ingress'
                }
            }
        }
        stage('Delete Service') {
            steps {
                script {
                    sh 'python3.11 kuber_kludge.py --kubeconfig ~/.kube/config --delete-service'
                }
            }
        }
        stage('Delete Config Map') {
            steps {
                script {
                    sh 'python3.11 kuber_kludge.py --kubeconfig ~/.kube/config --delete-configmap'
                }
            }
        }
        stage('Delete Cron Job') {
            steps {
                script {
                    sh 'python3.11 kuber_kludge.py --kubeconfig ~/.kube/config --delete-cronjob'
                }
            }
        }
        stage('Show Log Results') {
            steps {
                echo 'Generating log result list...'
                sh 'ls -l logs/* && cat logs/*'
            }
        }
    }
}
