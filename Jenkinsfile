pipeline {
    agent any
    options {
        disableConcurrentBuilds()
    }
    stages {
        stage('Build') {
			      when {
                expression {
                    GIT_BRANCH = 'origin/' + sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
                    return env.GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                sh 'docker-compose -f docker-compose-beta.yml build'
            }
        }
        stage('Delivery') {
			      when {
                expression {
                    GIT_BRANCH = 'origin/' + sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
                    return env.GIT_BRANCH == 'origin/master'
                }
            }
            steps {
                sh 'docker-compose -f docker-compose-beta.yml up -d'
            }
        }
    }
    post {
        always {
            dir("${env.WORKSPACE}base-django@tmp") {
                deleteDir()
            }
        }
    }
}
