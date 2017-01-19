#!groovy

@Library('github.com/mozmar/jenkins-pipeline@master')

def config
def utils

/**
 * Do the work.
 *
 * Below here is the definition of all of deployment and testing.
 */

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
    stage ('Build') {
        node {
            unstash 'workspace'
            utils.ircNotification(config, 'Test & Deploy', 'starting')
            try {
                utils.buildDockerImage(dockerfile: 'bedrock_base', update: true)
            } catch(err) {
                utils.ircNotification(config, 'Base Build', 'failure')
                throw err
            }
        }
        parallel build: {
            node {
                unstash 'workspace'
                try {
                    utils.buildDockerImage(dockerfile: 'bedrock_code', fromDockerfile: 'bedrock_base')
                } catch(err) {
                    utils.ircNotification(config, 'Code Build', 'failure')
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
                    utils.ircNotification(config, 'Dockerhub Base Push', 'warning')
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
                    utils.ircNotification(config, 'Unit Test Code Image', 'failure')
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
                    utils.ircNotification(config, 'Dockerhub Code Push', 'warning')
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
                utils.ircNotification(config, 'L10n Build', 'failure')
                throw err
            }
            utils.ircNotification(config, 'Docker Builds', 'complete')
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
                    utils.ircNotification(config, 'Dockerhub Push Failed', 'warning')
                }
            }
        },
        registry_usw: {
            node {
                unstash 'scripts'
                try {
                    utils.pushPrivateReg(config.regions.usw.registry_port)
                } catch(err) {
                    utils.ircNotification(config, 'US-West Registry Push', 'failure')
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
                    utils.ircNotification(config, 'EU-West Registry Push', 'failure')
                    throw err
                }
            }
        }
        node {
            unstash 'scripts'
            unstash 'tests'
            // prep for next stage
            sh 'docker/jenkins/build_integration_test_image.sh'
            utils.ircNotification(config, 'Docker Image Pushes', 'complete')
        }
    }

    def branchConfig = config.branches[env.BRANCH_NAME]
    for (appname in branchConfig.apps) {
        for (regionId in branchConfig.regions) {
            region = config.regions[regionId]
            def stageName = "Deploy ${appname}-${region.name}"
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
                            utils.ircNotification(config, stageName, 'failure')
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
                        utils.ircNotification(config, "Integration Tests ${region.name}", 'failure')
                    }
                    throw err
                }
            }
            node {
                unstash 'scripts'
                utils.ircNotification(config, stageName, 'success')
            }
        }
    }
}
/**
 * Deploy demo branches
 */
else if ( env.BRANCH_NAME ==~ /^demo__[\w-]+$/ ) {
    node {
        utils.ircNotification(config, 'Demo Deploy', 'starting')
        try {
            stage ('build') {
                sh 'make clean'
                sh 'make sync-all'
                sh 'echo "ENV GIT_SHA ${GIT_COMMIT}" >> docker/dockerfiles/bedrock_dev_final'
                sh 'echo "RUN echo ${GIT_COMMIT} > static/revision.txt" >> docker/dockerfiles/bedrock_dev_final'
                sh 'make build-final'
            }
        } catch(err) {
            utils.ircNotification(config, 'Demo Build', 'failure')
            throw err
        }

        try {
            stage ('deploy') {
                withCredentials([[$class: 'StringBinding',
                                  credentialsId: 'SENTRY_DEMO_DSN',
                                  variable: 'SENTRY_DEMO_DSN']]) {
                    withEnv(['DEIS_PROFILE=usw', 'PRIVATE_REGISTRY=localhost:5001']) {
                        sh './docker/jenkins/demo_deploy.sh'
                    }
                }
            }
        } catch(err) {
            utils.ircNotification(config, 'Demo Deploy', 'failure')
            throw err
        }
    }
}
else {
    echo "Doing nothing for ${env.BRANCH_NAME}"
}
