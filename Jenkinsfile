#!groovy

@Library('github.com/mozmeao/jenkins-pipeline@20170315.1')

def loadBranch(String branch) {
    // load the utility functions used below
    utils = load 'jenkins/utils.groovy'
    is_demo_branch = ( env.BRANCH_NAME ==~ /^demo\/[\w-]+$/ )
    if ( fileExists("./jenkins/branches/${branch}.yml") ) {
        config = readYaml file: "./jenkins/branches/${branch}.yml"
        if ( !config.apps && is_demo_branch ) {
            config.apps = [utils.demoAppName(env.BRANCH_NAME)]
        }
        println "config ==> ${config}"
    } else if ( is_demo_branch ) {
        config = readYaml file: "./jenkins/branches/demo/default.yml"
        config.apps = [utils.demoAppName(env.BRANCH_NAME)]
        println "config ==> ${config}"
    } else {
        println "No config for ${branch}. Nothing to do. Good bye."
        return
    }

    if ( config.apps ) {
        for ( app in config.apps ) {
            if ( app.length() > 63 ) {
                err_msg = "App name exceeds 63 char limit: ${app}"
                utils.ircNotification([message: err_msg, status: 'failure'])
                throw new Exception(err_msg)
            }

        }
    }

    // load the global config
    global_config = readYaml file: 'jenkins/global.yml'
    // defined in the Library loaded above
    setGitEnvironmentVariables()
    setConfigEnvironmentVariables(global_config)

    if ( config.pipeline && config.pipeline.script ) {
        println "Loading ./jenkins/${config.pipeline.script}.groovy"
        load "./jenkins/${config.pipeline.script}.groovy"
    } else {
        println "Loading ./jenkins/default.groovy"
        load "./jenkins/default.groovy"
    }
}

node {
    stage ('Prepare') {
        checkout scm
        sh 'git submodule sync'
        sh 'git submodule update --init --recursive'
        // clean up
        sh 'make clean'
        // save the files for later
        stash name: 'scripts', includes: 'bin/,docker/'
        stash name: 'tests', includes: 'tests/,requirements/'
        stash 'workspace'
    }
    loadBranch(env.BRANCH_NAME)
}
