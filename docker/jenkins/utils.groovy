/**
 * Define utility functions.
 */

def demoAppName(branchname) {
    def appname = branchname[5..-1].replaceAll('_', '-')
    return "bedrock-demo-${appname}".toString()
}

/**
 * Send a notice to #www on irc.mozilla.org with the build result
 *
 * @param stage step of build/deploy
 * @param result outcome of build (will be uppercased)
*/
def ircNotification(config, Map args) {
    def command = "bin/irc-notify.sh --irc_nick '${config.irc.nick}' --irc_channel '${config.irc.channel}'"
    for (arg in args) {
        command += " --${arg.key} '${arg.value}'"
    }
    sh command
}

def buildDockerImage(Map kwargs) {
    def update = kwargs.update ? 'true' : 'false'
    def repo = kwargs.dockerRepo ?: 'mozorg'
    def script = kwargs.script ?: 'build_image.sh'
    def environs = ["UPDATE_DOCKER_IMAGES=${update}",
                    "DOCKERFILE=${kwargs.dockerfile}",
                    "DOCKER_REPOSITORY=${repo}/${kwargs.dockerfile}"]
    if (kwargs.fromDockerfile) {
        environs << "FROM_DOCKER_REPOSITORY=${repo}/${kwargs.fromDockerfile}"
    }
    withEnv(environs) {
        sh "docker/jenkins/${script}"
    }
}

def pushDockerhub(from_repo, to_repo='') {
    to_repo = to_repo ?: from_repo
    withCredentials([[$class: 'StringBinding',
                      credentialsId: 'DOCKER_PASSWORD',
                      variable: 'DOCKER_PASSWORD']]) {
        withEnv(['DOCKER_USERNAME=mozjenkins',
                 "FROM_DOCKER_REPOSITORY=${from_repo}",
                 "DOCKER_REPOSITORY=${to_repo}"]) {
            retry(2) {
                sh 'docker/jenkins/push2dockerhub.sh'
            }
        }
    }
}

def pushPrivateReg(port) {
    retry(3) {
        // TODO Fix DEIS_APPS before merge
        // DEIS_APPS=bedrock-dev,bedrock-stage,bedrock-prod
        withEnv(['FROM_DOCKER_REPOSITORY=mozorg/bedrock_l10n',
                 "PRIVATE_REGISTRIES=localhost:${port}",
                 'DEIS_APPS=bedrock-jenkinsfile-test']) {
            sh 'docker/jenkins/push2privateregistries.sh'
        }
    }
}

def integrationTestJob(propFileName, appName, region) {
    def testsBaseDir = 'docker/jenkins/properties/integration_tests'
    def testsFileExt = '.properties'
    return {
        node {
            unstash 'scripts'
            unstash 'tests'
            def fullFilename = "${testsBaseDir}/${propFileName}${testsFileExt}"
            def testScript = "docker/jenkins/run_integration_tests.sh ${fullFilename}".toString()
            withCredentials([[$class: 'UsernamePasswordMultiBinding',
                              credentialsId: 'SAUCELABS_CREDENTIALS',
                              usernameVariable: 'SAUCELABS_USERNAME',
                              passwordVariable: 'SAUCELABS_API_KEY']]) {
                withEnv(["BASE_URL=https://${appName}.${region}.moz.works",
                         "SELENIUM_VERSION=2.52.0"]) {
                    try {
                        retry(2) {
                            sh testScript
                        }
                    }
                    finally {
                        junit 'results/*.xml'
                    }
                }
            }
        }
    }
}

return this;
