milestone()
stage ('Build Images') {
    // make sure we should continue
    if ( config.require_tag ) {
        try {
            sh 'docker/bin/check_if_tag.sh'
        } catch(err) {
            utils.ircNotification([stage: 'Git Tag Check', status: 'failure'])
            throw err
        }
    }
    utils.ircNotification([stage: 'Test & Deploy', status: 'starting'])
    lock ("bedrock-docker-${env.GIT_COMMIT}") {
        command = "docker/bin/build_images.sh"
        if (config.smoke_tests || config.integration_tests) {
            command += ' --test'
        }
        try {
            sh command
        } catch(err) {
            utils.ircNotification([stage: 'Docker Build', status: 'failure'])
            throw err
        }
    }
}

if ( config.smoke_tests ) {
    milestone()
    stage ('Test Images') {
        try {
            parallel([
                smoke_tests: utils.integrationTestJob('smoke'),
                unit_tests: {
                    node {
                        unstash 'scripts'
                        sh 'docker/bin/run_tests.sh'
                    }
                },
            ])
        } catch(err) {
            utils.ircNotification([stage: 'Unit Test', status: 'failure'])
            throw err
        }
    }
}

// test this way to default to true for undefined
if ( config.push_public_registry != false ) {
    milestone()
    stage ('Push Public Images') {
        try {
            if (config.demo) {
                utils.pushDockerhub('mozorg/bedrock_l10n', 'mozorg/bedrock')
            }
            else {
                utils.pushDockerhub('mozorg/bedrock_base')
                utils.pushDockerhub('mozorg/bedrock_build')
                utils.pushDockerhub('mozorg/bedrock_test')
                utils.pushDockerhub('mozorg/bedrock_code')
                utils.pushDockerhub('mozorg/bedrock_l10n', 'mozorg/bedrock')
            }
        } catch(err) {
            utils.ircNotification([stage: 'Dockerhub Push Failed', status: 'warning'])
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
if ( config.apps ) {
    milestone()
    tested_apps = []
    // default to usw only
    def regions = config.regions ?: ['usw']
    for (regionId in regions) {
        def region = global_config.regions[regionId]
        if (region.registry_port) {
            def stageName = "Private Push: ${region.name}"
            stage (stageName) {
                try {
                    utils.pushPrivateReg(region.registry_port, config.apps)
                } catch(err) {
                    utils.ircNotification([stage: stageName, status: 'failure'])
                    throw err
                }
            }
        }
        for (appname in config.apps) {
            if ( config.demo ) {
                appURL = utils.demoAppURL(appname, region)
            } else {
                appURL = "https://${appname}.${region.name}.moz.works"
            }
            stageName = "Deploy ${appname}-${region.name}"
            // ensure no deploy/test cycle happens in parallel for an app/region
            lock (stageName) {
                milestone()
                stage (stageName) {
                    withEnv(["DEIS_PROFILE=${region.deis_profile}",
                             "DEIS_BIN=${region.deis_bin}",
                             "DOCKER_PRIVATE_REPO=${appname}",
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
                            utils.ircNotification([stage: stageName, status: 'failure'])
                            throw err
                        }
                    }
                    utils.ircNotification([message: appURL, status: 'shipped'])
                }
                if ( config.integration_tests ) {
                    // queue up test closures
                    def allTests = [:]
                    def regionTests = config.integration_tests[regionId]
                    for (filename in regionTests) {
                        allTests[filename] = utils.integrationTestJob(filename, appURL)
                    }
                    stage ("Test ${appname}-${region.name}") {
                        try {
                            // wait for server to be ready
                            sleep(time: 10, unit: 'SECONDS')
                            if ( allTests.size() == 1 ) {
                                allTests[regionTests[0]]()
                            } else {
                                parallel allTests
                            }
                        } catch(err) {
                            utils.ircNotification([stage: "Integration Tests ${appname}-${region.name}", status: 'failure'])
                            throw err
                        }
                        tested_apps << "${appname}-${region.name}".toString()
                    }
                }
            }
        }
    }
    if ( tested_apps ) {
        // huge success \o/
        utils.ircNotification([message: "All tests passed: ${tested_apps.join(', ')}", status: 'success'])
    }
}
