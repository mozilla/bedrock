#!groovy

@Library('github.com/mozmar/jenkins-pipeline@20170214.1')

def config
def utils

stage ('Checkout') {
    node {
        checkout scm
        sh 'git submodule sync'
        sh 'git submodule update --init --recursive'
        // clean up
        sh 'make clean'
        // load the config
        config = readYaml file: 'jenkins.yml'
        // load the utility functions used below
        utils = load 'docker/jenkins/utils.groovy'
        // defined in the Library loaded above
        setGitEnvironmentVariables()
        setConfigEnvironmentVariables(config)
        // save the files for later
        stash name: 'scripts', includes: 'bin/,docker/'
        stash name: 'tests', includes: 'tests/,requirements/'
        stash 'workspace'
    }
}

if ( config.branches.containsKey(env.BRANCH_NAME) ) {
    def branchConfig = config.branches[env.BRANCH_NAME]
    milestone()
    stage ('Build Images') {
        node {
            unstash 'workspace'
            // make sure we should continue
            if ( branchConfig.require_tag ) {
                try {
                    sh 'docker/jenkins/check_if_tag.sh'
                } catch(err) {
                    utils.ircNotification(config, [stage: 'Git Tag Check', status: 'failure'])
                    throw err
                }
            }
            utils.ircNotification(config, [stage: 'Test & Deploy', status: 'starting'])
            lock ("bedrock-docker-${env.GIT_COMMIT}") {
                try {
                    sh 'docker/jenkins/build_images.sh --prod --test'
                } catch(err) {
                    utils.ircNotification(config, [stage: 'Docker Build', status: 'failure'])
                    throw err
                }
            }
        }
    }

    milestone()
    stage ('Test Images') {
        parallel([
            integration_tests: utils.integrationTestJob('local'),
            unit_tests: {
                node {
                    unstash 'scripts'
                    try {
                        sh 'docker/jenkins/run_tests.sh'
                    } catch(err) {
                        utils.ircNotification(config, [stage: 'Unit Test', status: 'failure'])
                        throw err
                    }
                }
            },
        ])
    }

    milestone()
    stage ('Push Public Images') {
        node {
            unstash 'scripts'
            try {
                utils.pushDockerhub('mozorg/bedrock_base')
                utils.pushDockerhub('mozorg/bedrock_code')
                utils.pushDockerhub('mozorg/bedrock_l10n', 'mozorg/bedrock')
            } catch(err) {
                utils.ircNotification(config, [stage: 'Dockerhub Push Failed', status: 'warning'])
            }
        }
    }

    /**
     * Do region first because deployment and testing should work like this:
     * region1:
     *   push image -> deploy app1 -> test app1 -> deploy app2 -> test app2
     * region2:
     *   push image -> deploy app1 -> test app1 -> deploy app2 -> test app2
     *
     * A failure at any step of the above should fail the entire job
     */
    milestone()
    for (regionId in branchConfig.regions) {
        def region = config.regions[regionId]
        def stageName = "Private Push: ${region.name}"
        stage (stageName) {
            node {
                unstash 'scripts'
                try {
                    utils.pushPrivateReg(region.registry_port, branchConfig.apps)
                } catch(err) {
                    utils.ircNotification(config, [stage: stageName, status: 'failure'])
                    throw err
                }
            }
        }
        for (appname in branchConfig.apps) {
            def appSuffix = branchConfig.app_name_suffix ?: ''
            def appURL = "https://${appname}${appSuffix}.${region.name}.moz.works"
            stageName = "Deploy ${appname}-${region.name}"
            // ensure no deploy/test cycle happens in parallel for an app/region
            lock (stageName) {
                milestone()
                stage (stageName) {
                    node {
                        unstash 'scripts'
                        withEnv(["DEIS_PROFILE=${region.deis_profile}",
                                 "DOCKER_REPOSITORY=${appname}",
                                 "DEIS_APPLICATION=${appname}"]) {
                            try {
                                retry(3) {
                                    sh 'docker/jenkins/push2deis.sh'
                                }
                            } catch(err) {
                                utils.ircNotification(config, [stage: stageName, status: 'failure'])
                                throw err
                            }
                        }
                    }
                }
                // queue up test closures
                def allTests = [:]
                for (filename in branchConfig.integration_tests) {
                    allTests[filename] = utils.integrationTestJob(filename, appURL)
                }
                stage ("Test ${appname}-${region.name}") {
                    try {
                        // wait for server to be ready
                        sleep(time: 10, unit: 'SECONDS')
                        parallel allTests
                    } catch(err) {
                        node {
                            unstash 'scripts'
                            utils.ircNotification(config, [stage: "Integration Tests ${appname}-${region.name}", status: 'failure'])
                        }
                        throw err
                    }
                }
                node {
                    unstash 'scripts'
                    // huge success \o/
                    utils.ircNotification(config, [message: appURL, status: 'shipped'])
                }
            }
        }
    }
}
/**
 * Deploy demo branches
 */
else if ( env.BRANCH_NAME ==~ /^demo__[\w-]+$/ ) {
    node {
        utils.ircNotification(config, [stage: 'Demo Deploy', status: 'starting'])
        stage ('build') {
            lock ("bedrock-docker-${env.GIT_COMMIT}") {
                milestone()
                try {
                    sh 'docker/jenkins/build_images.sh --demo'
                } catch(err) {
                    utils.ircNotification(config, [stage: 'Demo Build', status: 'failure'])
                    throw err
                }
            }
        }

        def appname = utils.demoAppName(env.BRANCH_NAME)
        stage ('deploy') {
            lock (appname) {
                milestone()
                try {
                    withCredentials([[$class: 'StringBinding',
                                      credentialsId: 'SENTRY_DEMO_DSN',
                                      variable: 'SENTRY_DEMO_DSN']]) {
                        withEnv(['DEIS_PROFILE=usw',
                                 "DEIS_APP_NAME=${appname}",
                                 "PRIVATE_REGISTRY=localhost:${config.regions.usw.registry_port}"]) {
                            sh './docker/jenkins/demo_deploy.sh'
                        }
                    }
                } catch(err) {
                    utils.ircNotification(config, [stage: 'Demo Deploy', status: 'failure'])
                    throw err
                }
            }
        }
        utils.ircNotification(config, [message: utils.demoAppURL(appname), status: 'shipped'])
    }
}
else {
    echo "Doing nothing for ${env.BRANCH_NAME}"
}
