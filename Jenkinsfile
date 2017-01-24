#!groovy

@Library('github.com/mozmar/jenkins-pipeline@master')

def config
def utils

stage ('Checkout') {
    node {
        checkout scm
        sh 'git submodule sync'
        sh 'git submodule update --init --recursive'
        // defined in the Library loaded above
        setGitEnvironmentVariables()
        // load the config
        config = readYaml file: 'jenkins.yml'
        // load the utility functions used below
        utils = load 'docker/jenkins/utils.groovy'
        // save the files for later
        stash name: 'scripts', includes: 'bin/,docker/'
        stash name: 'tests', includes: 'tests/,requirements/'
        stash 'workspace'
    }
}

if ( config.branches.containsKey(env.BRANCH_NAME) ) {
    def branchConfig = config.branches[env.BRANCH_NAME]
    stage ('Build') {
        node {
            unstash 'workspace'
            utils.ircNotification(config, [stage: 'Test & Deploy', status: 'starting'])
            try {
                utils.buildDockerImage(dockerfile: 'bedrock_base', update: true)
            } catch(err) {
                utils.ircNotification(config, [stage: 'Base Build', status: 'failure'])
                throw err
            }
        }
        parallel build: {
            node {
                unstash 'workspace'
                try {
                    utils.buildDockerImage(dockerfile: 'bedrock_code', fromDockerfile: 'bedrock_base')
                } catch(err) {
                    utils.ircNotification(config, [stage: 'Code Build', status: 'failure'])
                    throw err
                }
            }
        },
        push: {
            node {
                unstash 'scripts'
                try {
                    utils.pushDockerhub('mozorg/bedrock_base')
                } catch(err) {
                    utils.ircNotification(config, [stage: 'Dockerhub Base Push', status: 'warning'])
                }
            }
        }
    }

    stage ('Unit Test') {
        parallel build: {
            node {
                unstash 'scripts'
                try {
                    withEnv(['DOCKER_REPOSITORY=mozorg/bedrock_code']) {
                        sh 'docker/jenkins/run_tests.sh'
                    }
                } catch(err) {
                    utils.ircNotification(config, [stage: 'Unit Test Code Image', status: 'failure'])
                    throw err
                }
            }
        },
        push: {
            node {
                unstash 'scripts'
                try {
                    utils.pushDockerhub('mozorg/bedrock_code')
                } catch(err) {
                    utils.ircNotification(config, [stage: 'Dockerhub Code Push', status: 'warning'])
                }
            }
        }
    }

    stage ('Build L10n') {
        node {
            unstash 'scripts'
            try {
                utils.buildDockerImage(dockerfile: 'bedrock_l10n', fromDockerfile: 'bedrock_code', script: 'include_l10n.sh')
            } catch(err) {
                utils.ircNotification(config, [stage: 'L10n Build', status: 'failure'])
                throw err
            }
            utils.ircNotification(config, [stage: 'Docker Builds', status: 'complete'])
        }
    }

    stage ('Push Images') {
        // push images to docker hub and internal registries
        // FIXME(pmac) this should be dynamic based on which regions to which
        //             this branch will be deployed
        parallel dockerhub: {
            node {
                unstash 'scripts'
                try {
                    utils.pushDockerhub('mozorg/bedrock_l10n', 'mozorg/bedrock')
                } catch(err) {
                    utils.ircNotification(config, [stage: 'Dockerhub Push Failed', status: 'warning'])
                }
            }
        },
        registry_usw: {
            node {
                unstash 'scripts'
                try {
                    utils.pushPrivateReg(config.regions.usw.registry_port)
                } catch(err) {
                    utils.ircNotification(config, [stage: 'US-West Registry Push', status: 'failure'])
                    throw err
                }
            }
        },
        registry_euw: {
            node {
                unstash 'scripts'
                try {
                    utils.pushPrivateReg(config.regions.euw.registry_port)
                } catch(err) {
                    utils.ircNotification(config, [stage: 'EU-West Registry Push', status: 'failure'])
                    throw err
                }
            }
        }
        node {
            unstash 'scripts'
            unstash 'tests'
            // prep for next stage
            sh 'docker/jenkins/build_integration_test_image.sh'
            utils.ircNotification(config, [stage: 'Docker Image Pushes', status: 'complete'])
        }
    }

    for (appname in branchConfig.apps) {
        for (regionId in branchConfig.regions) {
            def region = config.regions[regionId]
            def appURL = "https://${appname}.${region.name}.moz.works"
            def stageName = "Deploy ${appname}-${region.name}"
            // ensure no deploy/test cycle happens in parallel for an app/region
            lock (stageName) {
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
                    allTests[filename] = utils.integrationTestJob(filename, appname, region.name)
                }
                stage ("Test ${appname}-${region.name}") {
                    try {
                        // wait for server to be ready
                        sleep(time: 10, unit: 'SECONDS')
                        parallel allTests
                    } catch(err) {
                        node {
                            unstash 'scripts'
                            utils.ircNotification(config, [stage: "Integration Tests ${region.name}", status: 'failure'])
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
        appname = utils.demoAppName(env.BRANCH_NAME)
        try {
            stage ('build') {
                sh 'make clean'
                sh 'make sync-all'
                sh 'echo "ENV GIT_SHA ${GIT_COMMIT}" >> docker/dockerfiles/bedrock_dev_final'
                sh 'echo "RUN echo ${GIT_COMMIT} > static/revision.txt" >> docker/dockerfiles/bedrock_dev_final'
                sh 'make build-final'
            }
        } catch(err) {
            utils.ircNotification(config, [stage: 'Demo Build', status: 'failure'])
            throw err
        }

        try {
            lock (appname) {
                stage ('deploy') {
                    withCredentials([[$class: 'StringBinding',
                                      credentialsId: 'SENTRY_DEMO_DSN',
                                      variable: 'SENTRY_DEMO_DSN']]) {
                        withEnv(['DEIS_PROFILE=usw',
                                 "DEIS_APP_NAME=${appname}",
                                 "PRIVATE_REGISTRY=localhost:${config.regions.usw.registry_port}"]) {
                            sh './docker/jenkins/demo_deploy.sh'
                        }
                    }
                    utils.ircNotification(config, [app_url: "https://${appname}.us-west.moz.works/"])
                }
            }
        } catch(err) {
            utils.ircNotification(config, [stage: 'Demo Deploy', status: 'failure'])
            throw err
        }
    }
}
else {
    echo "Doing nothing for ${env.BRANCH_NAME}"
}
