/**
 * Define utility functions.
 */

def appNameFromDemoBranch(branchname){
    return branchname[5..-1].replaceAll('_', '-')
}

def demoAppName(branchname) {
    def appname = appNameFromDemoBranch(branchname)
    return "bedrock-demo-${appname}"
}

def demoDeployYaml(branchname) {
    def appname = appNameFromDemoBranch(branchname)
    return "${appname}-deploy.yaml"
}

def demoAppURL(appname, region) {
    if ( appname ==~ /^bedrock-demo-[1-5]$/ ) {
        return "https://www-demo${appname[-1]}.allizom.org"
    }
    return "https://${appname}.${region.name}.moz.works"
}

/**
 * Send a notice to #www-notify on mozilla.slack.com with the build result
 *
 * @param stage step of build/deploy
 * @param result outcome of build (will be uppercased)
*/
def slackNotification(Map args) {
    def command = "bin/slack-notify.sh"
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
                        }
                    }
                }
            }
        }
    }
}

def pushDeis(region, config, appname, stageName) {
    withEnv(["DEIS_PROFILE=${region.name}",
            "DEIS_BIN=${region.deis_bin}",
            "DEIS_APPLICATION=${appname}"]) {
        try {
            retry(3) {
                if (config.demo) {
                    withCredentials([[$class: 'StringBinding',
                                      credentialsId: 'SENTRY_DEMO_DSN',
                                      variable: 'SENTRY_DEMO_DSN']]) {
                        sh 'docker/bin/prep_demo.sh'
                    }
                }
                sh 'docker/bin/push2deis.sh'
            }
        } catch(err) {
            slackNotification([stage: stageName, status: 'failure'])
            throw err
        }
    }
}

def deploy(region, config, appname, stageName, namespace) {

    def deployYaml = ""
    if (config.demo) {
        deployYaml = demoDeployYaml(env.BRANCH_NAME)
    } else {
        deployYaml = "deploy.yaml"
    }

    withEnv(["CLUSTER_NAME=${region.get('cluster_name', region.name)}",
             "CONFIG_REPO=${region.config_repo}",
             "CONFIG_BRANCH=${region.config_branch}",
             "NAMESPACE=${namespace}",
             "DEPLOYMENT_LOG_BASE_URL=${region.deployment_log_base_url}",
             "DEPLOYMENT_YAML=${deployYaml}"]) {
        try {
            sh 'bin/deploy.sh'
        } catch(err) {
            slackNotification([stage: stageName, status: 'failure'])
            throw err
        }
    }
}

return this;
