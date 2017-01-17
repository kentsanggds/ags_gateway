node {

    stage("Source") {
        checkout scm
    }

    stage("Build") {

        stage("Initialize virtualenv") {
            sh "rm -rf venv"
            sh "python3 -m venv venv"
            sh "venv/bin/pip install -U wheel pip cffi"
            sh "venv/bin/pip install -r requirements.txt"
        }

        stage("Build GOV.UK assets") {
            ansiColor("xterm") {
                sh "./install-govuk-assets"
            }
        }

    }

    stage("Test") {

        stage("Unit tests") {
            ansiColor("xterm") {
                sh "venv/bin/pytest --eradicate --flake8 --cov-report xml --cov=app --junitxml=results.xml --pyargs tests || true"
                junit 'results.xml'
            }
        }

    }

}
