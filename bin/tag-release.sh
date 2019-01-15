#!/bin/bash
set -euo pipefail

moz_git_remote="${MOZ_GIT_REMOTE:-origin}"
do_push=false

# parse cli args
while [[ $# -ge 1 ]]; do
  key="$1"
  case $key in
    -p|--push)
      do_push=true
      ;;
    -r|--remote)
      moz_git_remote="$2"
      shift # past argument
      ;;
  esac
  shift # past argument or value
done

echo "Did you test on stage first? If not, are you sure you want to skip going to stage?"
read stage
if [ "$stage" == "${stage#[Yy]}" ]; then
    # $stage doesn't start with y or Y
    exit
fi

# ensure all tags synced
git fetch --tags "$moz_git_remote"
date_tag=$(date +"%Y-%m-%d")
tag_suffix=0
tag_value="$date_tag"
while ! git tag -a $tag_value -m "tag release $tag_value" 2> /dev/null; do
  tag_suffix=$(( $tag_suffix + 1 ))
  tag_value="${date_tag}.${tag_suffix}"
done
echo "tagged $tag_value"
if [[ "$do_push" == true ]]; then
  git push "$moz_git_remote" "$tag_value"
  git push "$moz_git_remote" HEAD:prod
fi
