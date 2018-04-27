#!/bin/bash -x

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

docker stop bedrock-code-${BRANCH_AND_COMMIT}

for NODE_NUMBER in `seq ${NUMBER_OF_NODES:-5}`;
do
    docker stop bedrock-selenium-node-${NODE_NUMBER}-${BRANCH_AND_COMMIT}
done;

docker stop bedrock-selenium-hub-${BRANCH_AND_COMMIT}

# always report success
exit 0
