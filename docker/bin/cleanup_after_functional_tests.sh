#!/bin/bash -x

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

docker stop bedrock-code-${GIT_COMMIT_SHORT}

for NODE_NUMBER in `seq ${NUMBER_OF_NODES:-5}`;
do
    docker stop bedrock-selenium-node-${NODE_NUMBER}-${GIT_COMMIT_SHORT}
done;

docker stop bedrock-selenium-hub-${GIT_COMMIT_SHORT}

# always report success
exit 0
