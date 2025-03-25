# 2. Move CI/CD Pipelines to Gitlab

Date: 2019-10-09

## Status

Superseded by 0010

## Context

Our current CI/CD pipelines are implemented in Jenkins. We would like to decommission our Jenkins server by the end of this year. We have implemented CI/CD pipelines using Gitlab in other projects, including [basket](https://github.com/mozmeao/basket/blob/master/.gitlab-ci.yml), [nucleus](https://github.com/mozilla/nucleus/blob/master/.gitlab-ci.yml) and the [snippets-service](https://github.com/mozmeao/snippets-service/blob/master/.gitlab-ci.yml).

## Decision

We will move our existing CI/CD pipeline implementation from Jenkins to Gitlab.

## Consequences

We will continue to use [www-config](https://github.com/mozmeao/www-config) to version control our Kubernetes yaml files, but we will replace the use of [git-sync-operator](https://github.com/mozmeao/git-sync-operator) and its [branch](https://github.com/mozmeao/www-config/tree/git-sync-operator) with self-managed instances of [gitlab runner](https://docs.gitlab.com/runner/) executing jobs defined in a new .gitlab-ci.yml file leveraging what we have learned implementing similar solutions in [nucleus-config](https://github.com/mozmeao/nucleus-config/blob/master/.gitlab-ci.yml), [basket-config](https://github.com/mozmeao/basket-config/blob/master/.gitlab-ci.yml), and [snippets-config](https://github.com/mozmeao/snippets-config/blob/master/.gitlab-ci.yml). We will also eliminate our last dependency on Deis Workflow, which we have been using for dynamic demo deployments based on the branch name, in favor of a fixed number of pre-configured demo deployments, potentially supplemented by [Heroku Review Apps](https://github.com/mozilla/bedrock/pull/7849).
