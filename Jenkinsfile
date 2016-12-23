def branch = env.BRANCH_NAME

if ( branch == 'master') {
    echo "Building master"
    build 'bedrock_base_image'
}
else if ( branch == 'prod') {
    echo "Building prod"
    build 'bedrock_base_image'
}
else if ( branch ==~ /^demo__[a-z_-]+$/ ) {
    echo "Building a demo: ${branch} (just for testing. does not work yet.)"
    echo "TODO: make this work"
}
else {
    echo "Doing nothing for ${branch}"
}
