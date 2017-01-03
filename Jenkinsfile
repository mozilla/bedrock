env.DEIS_PROFILE = 'usw'
env.PRIVATE_REGISTRY = 'localhost:5001'

/** Send a notice to #www on irc.mozilla.org with the build result
 *
 * @param stage step of build/deploy
 * @param result outcome of build (will be uppercased)
*/
def ircNotification(stage, status) {
    sh "bin/irc-notify.sh --stage '${stage}' --status '${status}'"
}

node {
    def branch = env.BRANCH_NAME

    stage ('git') {
        checkout scm
        sh 'git submodule sync'
        sh 'git submodule update --init --recursive'
        env.GIT_COMMIT = sh([returnStdout: true, script: 'git rev-parse HEAD']).trim()
    }

    if ( branch == 'master') {
        ircNotification('Dev Deploy', 'starting')
        build 'bedrock_base_image'
    }
    else if ( branch == 'prod') {
        ircNotification('Stage & Prod Deploys', 'starting')
        build 'bedrock_base_image'
    }
    else if ( branch ==~ /^demo__[\w-]+$/ ) {
        ircNotification('Demo Deploy', 'starting')
        try {
            stage ('build') {
                sh 'make clean'
                sh 'make sync-all'
                sh 'echo "ENV GIT_SHA ${GIT_COMMIT}" >> docker/dockerfiles/bedrock_dev_final'
                sh 'echo "RUN echo ${GIT_COMMIT} > static/revision.txt" >> docker/dockerfiles/bedrock_dev_final'
                sh 'make build-final'
            }
        } catch(err) {
            ircNotification('Demo Build', 'failure')
            throw err
        }

        try {
            stage ('deploy') {
                withCredentials([[$class: 'StringBinding',
                                  credentialsId: 'SENTRY_DEMO_DSN',
                                  variable: 'SENTRY_DEMO_DSN']]) {
                    sh './docker/jenkins/demo_deploy.sh'
                }
            }
        } catch(err) {
            ircNotification('Demo Deploy', 'failure')
            throw err
        }
    }
    else {
        echo "Doing nothing for ${branch}"
    }
}
