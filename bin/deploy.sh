#!/bin/bash
set -ex
# required env vars: CLUSTER_NAME, CONFIG_BRANCH, CONFIG_REPO, NAMESPACE,
# DEPLOYMENT_YAML, DEPLOYMENT_LOG_BASE_URL, DEPLOYMENT_NAME, DEPLOYMENT_VERSION

. ${BASH_SOURCE%/*}/../docker/bin/set_git_env_vars.sh # sets DEPLOYMENT_DOCKER_IMAGE
pushd $(mktemp -d)
git clone --depth=1 -b ${CONFIG_BRANCH:=master} ${CONFIG_REPO} config_checkout
cd config_checkout

set -u
sed -i -e "s|image: .*|image: ${DEPLOYMENT_DOCKER_IMAGE}|" ${CLUSTER_NAME}/${NAMESPACE}/${DEPLOYMENT_YAML:=deploy.yaml}
git add ${CLUSTER_NAME}/${NAMESPACE}/${DEPLOYMENT_YAML}
git commit -m "set image to ${DEPLOYMENT_DOCKER_IMAGE} in ${CLUSTER_NAME}" || echo "nothing new to commit"
git push
DEPLOYMENT_VERSION=$(git rev-parse --short HEAD)

DEPLOYMENT_NAME=$(python3 -c "import yaml; print(yaml.load(open(\"$CLUSTER_NAME/$NAMESPACE/$DEPLOYMENT_YAML\"))['metadata']['name'])")
CHECK_URL=$DEPLOYMENT_LOG_BASE_URL/$NAMESPACE/$DEPLOYMENT_NAME/$DEPLOYMENT_VERSION
attempt_counter=0
max_attempts=120
set +x
until curl -sf $CHECK_URL; do
    if [ ${attempt_counter} -eq ${max_attempts} ]; then
        echo "Deployment incomplete"
        exit 1
    fi
    attempt_counter=$(($attempt_counter+1))
    sleep 10
done
popd
