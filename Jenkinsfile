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
            runTests('unit')
        }

        stage("Integration tests") {
            runTests('integration')
        }

        stage("Functional tests") {
            runTests('functional')
        }

    }

    stage("Deploy") {
        def app_name = "ags-gateway-${BRANCH_NAME.replace('_', '-')}"

        if (BRANCH_NAME == 'master') {
            app_name = "ags-gateway"
        }

        deployToPaaS(app_name)
        slackSend(color: '#78b037', message: "Deployed ${BRANCH_NAME} branch of Gateway to https://${app_name}.cloudapps.digital")
    }
}


def runTests(path) {

    ansiColor("xterm") {
        try {
            sh "venv/bin/pytest --eradicate --flake8 --cov-report xml --cov=app --junitxml=results.xml --pyargs tests/${path}"

        } catch(err) {
            junit "results.xml"

            if (currentBuild.result == 'UNSTABLE') {
                currentBuild.result = 'FAILURE'
            }

            throw err
        }

        junit "results.xml"
    }
}


def deployToPaaS(app_name) {
    def paasUser ='f8b4788a-0383-4c2a-ba4f-64415628debb'

    withEnv(["CF_APPNAME=${app_name}"]) {
        withCredentials([
            usernamePassword(
                credentialsId: paasUser,
                usernameVariable: 'CF_USER',
                passwordVariable: 'CF_PASSWORD'),
            file(
                credentialsId: 'environment.sh',
                variable: 'ENV_FILE')]) {

            ansiColor("xterm") {
                sh "./deploy-to-paas"
            }
        }
    }
}
