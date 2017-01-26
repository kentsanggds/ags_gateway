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

    if (!BRANCH_NAME.startsWith('PR-')) {

        stage("Deploy") {
            def branch = "${BRANCH_NAME.replace('_', '-')}"
            def appName = cfAppName("ags-gateway", branch)
            def url = "https://${appName}.cloudapps.digital"

            parallel (

                "Deploy to PaaS": {
                    deployToPaaS(appName)

                    if (BRANCH_NAME == 'master') {
                        slackSend color: success, message: "Deployed ${BRANCH_NAME} branch of Gateway to ${url}"
                    }
                },

                "Deploy test client": {
                    build(
                        job: 'sue_my_brother/master',
                        parameters: [
                            string(name: 'OIDC_CLIENT_ISSUER', value: url),
                            string(name: 'GATEWAY_BRANCH', value: branch)
                        ]
                    )
                }
            )
        }

    }
}


def cfAppName(appName, branch) {

    if (branch != 'master') {
        appName = "${appName}-${branch}"
    }

    return appName
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

    withEnv(["CF_APPNAME=${app_name}"]) {
        withCredentials([
            usernamePassword(
                credentialsId: 'paas-deploy',
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
