create-deis-app() {
  if deis apps:create ${DEIS_APP_NAME} --no-remote; then
    deis config:push -a "$DEIS_APP_NAME" -p .bedrock_demo_env
    REPO=${REPO:-mozilla/bedrock}
    COMMIT=${COMMIT:-$(git rev-parse --short HEAD)}
    COMMIT_AUTHOR=$(curl https://api.github.com/repos/${REPO}/commits/${COMMIT} | jq .author.login)
    if [[ -n "${COMMIT_AUTHOR}" ]]; then
      deis perms:create ${CI_DEIS_USER:-jenkins} -a ${DEIS_APP_NAME}
      deis apps:transfer ${COMMIT_AUTHOR} -a ${DEIS_APP_NAME}
    fi
  fi
}
check-branch-commit() {
  rm -f .new_commit_*
  BRANCH=${GIT_BRANCH#origin/}
  COMMIT=$(git rev-parse --short HEAD)
  if [[ ! -e .latest_commit_${BRANCH} || "$(< .latest_commit_${BRANCH})" != "${COMMIT}" ]]; then
    echo new commit ${COMMIT} on ${BRANCH}
    echo ${COMMIT} > .new_commit_${BRANCH}
    if [[ "${BRANCH}" =~ "demo__" ]]; then
      echo DEIS_APP_NAME=bedrock-demo-${BRANCH#demo__} | tr "_" "-" > .new_commit_deis_app_name
    fi
  fi
  echo ${COMMIT} > .latest_commit_${BRANCH}
}

check-tag() {
  rm -f .new_tag
  LATEST_TAG=$(git describe --abbrev=0 --tags)
  if [[ ! -e .latest_tag || "$(< .latest_tag)" != "${LATEST_TAG}" ]]; then
    echo ${LATEST_TAG} > .new_tag
    echo new tag ${LATEST_TAG}
  fi
  echo ${LATEST_TAG} > .latest_tag
}
