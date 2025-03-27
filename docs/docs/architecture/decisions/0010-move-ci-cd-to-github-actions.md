# 10. Move CI to Github Actions for Unit and Integration tests

Date: 2023-04-06

## Status

Accepted

## Context

Prior to this work, Bedrock's CI/CD pipeline involved Github, Gitlab and CircleCI. We were mirroring from Github to Gitlab to benefit from Gitlab's CI tooling for our functional integration tests, including private (i.e. Mozilla-managed) runners.

Additionally, we were using a third party (CircleCI) to run our Python and JS unit tests.

Since then, two things have changed:

1. Github Actions (GHA) have arrived
2. We are now able to use private runners with GHA

## Decision

We will move our CI/CD pipeline from being a combination of Github + Gitlab + CircleCI to just Github, using GHA.

This will mean:

1. The mirroring to Gitlab will no longer be necessary.
2. Unit tests move from CircleCI to GHA. They will continue to be run on every PR raised against `mozilla/bedrock`.
3. Functional/integration tests move from Gitlab to GHA. They will still be triggered by a successful deployment to dev/test/stage/prod.

This work will be carried out in parallel with changes to how our deployment pipeline works, as that side is also being moved out of Gitlab and into GHA + GCP. When a deployment succeeds, a GHA in the deployment repo will trigger a GHA in `mozilla/bedrock`, which will then run the functional integration tests.

## Consequences

### Pros

* We're no longer mirroring from Github to Gitlab, which will make understanding the deployment pipeline easier for new (and current) developers
* We will no longer have Gitlab in our pipeline, removing a potential point of failure that could block releases
* We can still use private runners for our functional integration tests and more (just via GHA instead of Gitlab), giving us control over security and machine resource spec

### Cons

* There's a risk that there will still be new race conditions or CI kick-off failures if the webhook from the deployment repo to mozilla/bedrock fails.
* We will not all get visibility of a failed webhook ping from the deployment repo's GHA, because that's locked down to be private. We can mitigate this risk with a sensible pattern of Slack notifications (e.g. Start, Success, Failure), so a missing notification will itself be a significant thing.
