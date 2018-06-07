/**
 * Define utility functions.
 */

def demoAppName(branchname) {
    def appname = branchname[5..-1].replaceAll('_', '-')
    return "bedrock-demo-${appname}".toString()
}

def demoAppURL(appname, region) {
    if ( appname ==~ /^bedrock-demo-[1-5]$/ ) {
        return "https://www-demo${appname[-1]}.allizom.org"
    }
    return "https://${appname}.${region.name}.moz.works"
}

/**
 * Send a notice to #www-notify on irc.mozilla.org with the build result
 *
 * @param stage step of build/deploy
 * @param result outcome of build (will be uppercased)
*/
def ircNotification(Map args) {
    def command = "bin/irc-notify.sh"
    for (arg in args) {
        command += " --${arg.key} '${arg.value}'"
    }
    sh command
}

def pushDockerhub(from_repo) {
    withCredentials([[$class: 'StringBinding',
                      credentialsId: 'DOCKER_PASSWORD',
                      variable: 'DOCKER_PASSWORD']]) {
        withEnv(['DOCKER_USERNAME=mozjenkins',
                 "FROM_DOCKER_REPOSITORY=${from_repo}"]) {
            retry(2) {
                sh 'docker/bin/push2dockerhub.sh'
            }
        }
    }
}

def integrationTestJob(propFileName, appURL='') {
    return {
        node {
            unstash 'workspace'
            def testScript = "docker/bin/run_integration_tests.sh ${propFileName}".toString()
            withCredentials([[$class: 'UsernamePasswordMultiBinding',
                              credentialsId: 'SAUCELABS_CREDENTIALS',
                              usernameVariable: 'SAUCELABS_USERNAME',
                              passwordVariable: 'SAUCELABS_API_KEY']]) {
                withEnv(["BASE_URL=${appURL}"]) {
                    retry(2) {
                        try {
                            sh testScript
                        }
                        finally {
                            junit 'results/*.xml'
                            if ( propFileName == 'smoke' ) {
                                sh 'docker/bin/cleanup_after_functional_tests.sh'
                            }
                        }
                    }
                }
            }
        }
    }
}

return this;
