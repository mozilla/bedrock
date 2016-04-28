#!/bin/bash

moz_git_remote="${MOZ_GIT_REMOTE:-origin}"

# ensure all tags synced
git fetch --tags
date_tag=$(date +"%Y-%m-%d")
tag_suffix=0
tag_value="$date_tag"
while ! git tag -a $tag_value -m "tag release $tag_value" 2> /dev/null; do
  tag_suffix=$(( $tag_suffix + 1 ))
  tag_value="${date_tag}.${tag_suffix}"
done
echo "tagged $tag_value"
if [[ "$1" == "--push" ]]; then
  git push "$moz_git_remote" "$tag_value"
fi
