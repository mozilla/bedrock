milestone()

utils.slackNotification([stage: 'Test', status: 'starting'])

env.GIT_COMMIT = "latest"

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
            } else {
                appURL = "https://${appname}.${region.name}.moz.works"
            }
            if ( config.demo ) {
                appURL = utils.demoAppURL(appname, region)
            } else {
                appURL = "https://${appname}.${region.name}.moz.works"
            }
            stageName = "Deploy ${appname}-${region.name}"
            // ensure no deploy/test cycle happens in parallel for an app/region
            lock (stageName) {
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
}
if ( tested_apps ) {
    // huge success \o/
    utils.slackNotification([message: "All tests passed: ${tested_apps.join(', ')}", status: 'success'])
}
