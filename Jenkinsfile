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
            def branch = "${BRANCH_NAME.replace('_', '-')}"
            def appName = cfAppName("ags-gateway-proxied", branch)
            def url = "https://${appName}.cloudapps.digital"

            parallel (

                "Deploy Gateway to PaaS": {

                    stash(
                        name: "app",
                        includes: ".cfignore,Procfile,app/**,deploy-to-paas,lib/**,*.yml,*.txt,*.pem"
                    )

                    node('master') {

                        unstash "app"

                        deployToPaaS(appName)
                    }
                },

                "Deploy proxy to PaaS": {
                    build(
                        job: 'keycloak-proxy/ags',
                        parameters: [
                            string(name: 'GATEWAY_BRANCH', value: branch)
                        ]
                    )                    
                },

                "Deploy test client to PaaS": {
                    build(
                        job: 'sue_my_brother/kc-proxy',
                        parameters: [
                            string(name: 'GATEWAY_BRANCH', value: branch)
                        ]
                    )
                }
            )
            if (BRANCH_NAME == 'master') {
                slackSend color: success, message: "Deployed ${BRANCH_NAME} branch of Gateway to ${url}"
            }
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
                slackSend(color: fail, message: "${path.capitalize()} tests failed on ${BRANCH_NAME} branch of Proxied Gateway")
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
