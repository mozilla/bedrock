def branch = env.BRANCH_NAME
env.DEIS_PROFILE = 'usw'
env.PRIVATE_REGISTRY = 'localhost:5001'

/** Send a notice to #www on irc.mozilla.org with the build result
 *
 * @param stage step of build/deploy
 * @param result outcome of build (will be uppercased)
*/
def ircNotification(stage, result) {
    def nick = "bedrock-deployer-${env.BUILD_NUMBER}"
    def channel = '#www'
    result = result.toUpperCase()
    def message = "${stage}: ${result}: Branch ${env.BRANCH_NAME} build #${env.BUILD_NUMBER}: ${env.BUILD_URL}"
    sh """
        (
        echo NICK ${nick}
        echo USER ${nick} 8 * : ${nick}
        sleep 5
        echo "JOIN ${channel}"
        echo "NOTICE ${channel} :${message}"
        echo QUIT
        ) | openssl s_client -connect irc.mozilla.org:6697
    """
}

if ( branch == 'master') {
    ircNotification('Dev Deploy', 'starting')
    build 'bedrock_base_image'
}
else if ( branch == 'prod') {
    ircNotification('Prod Deploy', 'starting')
    build 'bedrock_base_image'
}
else if ( branch ==~ /^demo__[\w-]+$/ ) {
    node {
        ircNotification('Demo Deploy', 'starting')

        stage ('git') {
            checkout scm
            sh 'git submodule sync'
            sh 'git submodule update --init --recursive'
            env.GIT_COMMIT = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
        }

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

        ircNotification('Demo Deploy', 'success')
    }
}
else {
    echo "Doing nothing for ${branch}"
}
