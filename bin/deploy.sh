#!/bin/bash
set -ex
# required env vars: CONFIG_BRANCH, CONFIG_REPO, NAMESPACE, DEPLOYMENT_YAML
# DEPLOYMENT_LOG_BASE_URL, DEPLOYMENT_NAME, DEPLOYMENT_VERSION

pushd $(mktemp -d)
git clone --depth=1 -b ${CONFIG_BRANCH:=master} ${CONFIG_REPO} config_checkout
cd config_checkout

. ../docker/bin/set_git_env_vars.sh # sets DEPLOYMENT_DOCKER_IMAGE
set -u
sed -i -e "s|image: .*|image: ${DEPLOYMENT_DOCKER_IMAGE}|" ${NAMESPACE}/${DEPLOYMENT_YAML:=deploy.yaml}
git add ${NAMESPACE}/${DEPLOYMENT_YAML}
git commit -m "set image to ${DEPLOYMENT_DOCKER_IMAGE}" || echo "nothing new to commit"
git push
DEPLOYMENT_VERSION=$(git rev-parse --short HEAD)

DEPLOYMENT_NAME=$(python3 -c "import yaml; print(yaml.load(open(\"$NAMESPACE/$DEPLOYMENT_YAML\"))['metadata']['name'])")
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
