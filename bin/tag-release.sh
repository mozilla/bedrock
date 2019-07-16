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

# compare master and stage
echo "Comparing master branch to staging..."
git fetch "$moz_git_remote"
stage_hash=$(git rev-parse "${moz_git_remote}/stage")
master_hash=$(git rev-parse master)
if [[ "$stage_hash" != "$master_hash" ]]; then
    read -p "Master branch does NOT match stage branch! Are you sure you want to continue? (Type Override to continue, n to cancel)" no_match
    if [ "$no_match" == "${no_match#[Override]}" ]; then
        # do not continue tagging release
        echo "Cancelled."
        exit
    fi
else
    echo "✓ Master branch matches staging."
fi

# prompt for confirmation, evaluate after first letter typed
read -p "Did the tests pass on staging? (y to continue, n to cancel)" -n 1 stage
echo    # because the user doesn't press enter after answering we have to add a new line here for readability
if [ "$stage" == "${stage#[Yy]}" ]; then
    # $stage doesn't start with y or Y
    echo "Cancelled."
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
