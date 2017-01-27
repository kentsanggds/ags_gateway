#!groovy

def success = '#78b037'
def fail = '#D54C53'

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

        parallel (
            "Unit tests": {
                runTests('unit')
            },

            "Integration tests": {
                runTests('integration')
            },

            "Functional tests": {
                runTests('functional')
            }
        )
    }

    if (!BRANCH_NAME.startsWith('PR-')) {

        stage("Deploy") {
            def app_name = "ags-gateway"

            if (BRANCH_NAME != 'master') {
                app_name = "${app_name}-${BRANCH_NAME.replace('_', '-')}"
            }

            retry(2) {
                deployToPaaS(app_name)
            }

            if (BRANCH_NAME == 'master') {
                def url = "https://${app_name}.cloudapps.digital"
                slackSend color: success, message: "Deployed ${BRANCH_NAME} branch of Gateway to ${url}"
            }
        }

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

            if (BRANCH_NAME == 'master') {
                slackSend(color: fail, message: "${path.capitalize()} tests failed on ${BRANCH_NAME} branch of Gateway")
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
