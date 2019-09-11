milestone()
stage ('Build Images') {
    // make sure we should continue
    if ( config.require_tag ) {
        try {
            sh 'docker/bin/check_if_tag.sh'
        } catch(err) {
            utils.slackNotification([stage: 'Git Tag Check', status: 'failure'])
            throw err
        }
    }
    utils.slackNotification([stage: 'Test & Deploy', status: 'starting'])
    lock ("bedrock-docker-build") {
        try {
            sh "make clean build-ci"
        } catch(err) {
            utils.slackNotification([stage: 'Docker Build', status: 'failure'])
            throw err
        }
        // save the files for later
        stash 'workspace'
    }
}

// test this way to default to true for undefined
if ( config.push_public_registry != false ) {
    milestone()
    stage ('Push Public Images') {
        try {
            if (config.demo) {
                utils.pushDockerhub('mozorg/bedrock')
            }
            else {
                utils.pushDockerhub('mozorg/bedrock_test')
                utils.pushDockerhub('mozorg/bedrock_assets')
                utils.pushDockerhub('mozorg/bedrock_code')
                utils.pushDockerhub('mozorg/bedrock_build')
                utils.pushDockerhub('mozorg/bedrock')
                // also upload static files to s3 bucket
                // the script itself decides if this is a prod push or not
                sh "bin/upload-staticfiles.sh"
            }
        } catch(err) {
            utils.slackNotification([stage: 'Dockerhub Push Failed', status: 'failure'])
            throw err
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
    // default to oregon-b only
    def regions = config.regions ?: ['oregon-b']
    for (regionId in regions) {
        def region = global_config.regions[regionId]
        for (appname in config.apps) {
            if ( config.demo ) {
                appURL = utils.demoAppURL(appname, region)
                namespace = 'bedrock-demo'
            } else {
                appURL = "https://${appname}.${region.name}.moz.works"
                namespace = appname
            }
            stageName = "Deploy ${appname}-${region.name}"
            // ensure no deploy/test cycle happens in parallel for an app/region
            lock (stageName) {
                milestone()
                stage (stageName) {
                    if ( region.deis_bin ) {
                        utils.pushDeis(region, config, appname, stageName)
                    } else if (region.config_repo){
                        utils.deploy(region, config, appname, stageName, namespace)
                    }
                    utils.slackNotification([message: appURL, status: 'shipped'])
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
                            utils.slackNotification([stage: "Integration Tests ${appname}-${region.name}", status: 'failure'])
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
        utils.slackNotification([message: "All tests passed: ${tested_apps.join(', ')}", status: 'success'])
    }
}
