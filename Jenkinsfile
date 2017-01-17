#!groovy

node {

    stage("Source") {
        checkout scm
    }

    stage("Build") {

        parallel (

            "Initialize virtualenv": {
                sh "rm -rf venv"
                sh "python3 -m venv venv"
                sh "venv/bin/pip install -U wheel pip cffi"
                sh "venv/bin/pip install -r requirements.txt"
            },


            "Build GOV.UK assets": {
                ansiColor("xterm") {
                    sh "./install-govuk-assets"
                }
            }
        )

    }

    stage("Test") {

        stage("Unit tests") {
            ansiColor("xterm") {
                try {
                    sh "venv/bin/pytest --eradicate --flake8 --cov-report xml --cov=app --junitxml=results.xml --pyargs tests"
                } catch(err) {
                    junit 'results.xml'
                    if (currentBuild.result == 'UNSTABLE') {
                        currentBuild.result = 'FAILURE'
                    }
                    throw err
                }
                junit 'results.xml'
            }
        }

    }

    stage("Deploy") {
        withEnv(["CF_APPNAME=ags-gateway-${BRANCH_NAME.replace('_', '-')}"]) {
            withCredentials([
                usernamePassword(credentialsId: 'f8b4788a-0383-4c2a-ba4f-64415628debb', usernameVariable: 'CF_USER', passwordVariable: 'CF_PASSWORD'),
                file(credentialsId: 'environment.sh', variable: 'ENV_FILE')]) {
                        ansiColor("xterm") {
                            sh "./deploy-to-paas"
                        }
            }
            slackSend(color: '#78b037', message: "Deployed Gateway to https://${CF_APPNAME}.cloudapps.digital")
        }
    }

}
