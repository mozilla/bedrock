#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -euo pipefail

moz_git_remote="${MOZ_GIT_REMOTE:-origin}"
do_push=false
ci_mode=false

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
    -c|--ci)
      ci_mode=true
      ;;
  esac
  shift # past argument or value
done

write_output() {
    if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
        echo "$1" >> "$GITHUB_OUTPUT"
    fi
}

git fetch "$moz_git_remote"

if [[ "$ci_mode" == true ]]; then
    # A re-run of the release job must not mint a new tag for a SHA that is
    # already tagged: no new integration tests are dispatched for a SHA that's
    # already on prod. Reuse the oldest tag, the one that actually deployed it.
    # This runs before the stage check so a retry works even if stage has moved.
    git fetch --tags "$moz_git_remote"
    existing_tag=$(git tag --points-at HEAD | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}(\.[0-9]+)?$' | sort -V | head -n 1 || true)
    if [[ -n "$existing_tag" ]]; then
        echo "✓ HEAD is already tagged; reusing existing tag $existing_tag"
        write_output "tag=${existing_tag}"
        write_output "reused=true"
        prod_updated=false
        if [[ "$do_push" == true && "$(git rev-parse "${moz_git_remote}/prod")" != "$(git rev-parse HEAD)" ]]; then
            # Prod isn't on this SHA (a previous run failed before updating
            # prod, or prod was rolled back), so this push redeploys it and the
            # caller must ignore integration runs from before now.
            git push "$moz_git_remote" HEAD:prod
            prod_updated=true
        fi
        write_output "prod_updated=${prod_updated}"
        exit 0
    fi
fi

# compare main and stage
echo "Comparing main branch to staging..."
stage_hash=$(git rev-parse "${moz_git_remote}/stage")
if [[ "$ci_mode" == true ]]; then
    # In CI mode we check out a specific SHA (detached HEAD), so 'main' branch
    # reference is unavailable. Compare HEAD directly against origin/stage.
    main_hash=$(git rev-parse HEAD)
else
    main_hash=$(git rev-parse main)
fi
if [[ "$stage_hash" != "$main_hash" ]]; then
    if [[ "$ci_mode" == true ]]; then
        echo "ERROR: Main branch does NOT match stage branch. Aborting release."
        echo "  main:  $main_hash"
        echo "  stage: $stage_hash"
        exit 1
    fi
    read -p "Main branch does NOT match stage branch! Are you sure you want to continue? (Type Override to continue, n to cancel)" no_match
    if [ "$no_match" == "${no_match#[Override]}" ]; then
        # do not continue tagging release
        echo "Cancelled."
        exit
    fi
else
    echo "✓ Main branch matches staging."
fi

if [[ "$ci_mode" != true ]]; then
    # prompt for confirmation, evaluate after first letter typed
    read -p "Did the tests pass on staging? (y to continue, n to cancel)" -n 1 stage
    echo    # because the user doesn't press enter after answering we have to add a new line here for readability
    if [ "$stage" == "${stage#[Yy]}" ]; then
        # $stage doesn't start with y or Y
        echo "Cancelled."
        exit
    fi
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

# Output the tag name for CI systems to capture
write_output "tag=${tag_value}"
write_output "reused=false"

if [[ "$do_push" == true ]]; then
  git push "$moz_git_remote" "$tag_value"
  git push "$moz_git_remote" HEAD:prod
fi
