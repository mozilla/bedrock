# Pipelines!

Goal of this document is to explain how end users can use the pipelines we've written for bedrock.

# Overview
We define the gitlab based pipeline in '.gitlab-ci.yml'. For code reuse there are few jobs/stages defined [here](https://github.com/mozmeao/gitlab-library/).

# Special Temporary Pipelines

### Demos

Push a branch to `demo/*` for example `demo/test`. Then, we slugify the name of the branch (using the python library slugify) and host the website (via k8s) at `www-demo-test.mozmar.org` where it ought to act like bedrock.  Gitlab is building per branch, so if you have any issues check there for the logs.


### Functional Test

Given that a branch is pushed to 'run-integration-tests'

Does a standard deploy in the model described below in the Standard CI/CD section. Then

# Standard CI/CD

In general, does make build-ci to build some containers.
Then pushes them to a bunch of docker repositories.
Then uploads some static files to s3 buckets.

Uses the oregon-b runner.

The `.update-config` job is the primary 'doer' for these pipelines.
Targets `master|stage|prod` named branches only

### Dev

Targets iowa-a (gcp).  Deploys to k8s in namespace bedrock-dev.

### Stage

Targets iowa-a (gcp).  Deploys to k8s in namespace bedrock-stage.

### Prod

Targets frankfurt (aws) and iowa-a (gcp).  Deploys to k8s in namespace bedrock-prod.

