---
title: Continuous Integration & Deployment
---

Bedrock runs a series of automated tests as part of continuous
integration workflow and deployment pipeline. You can learn more about
each of the individual test suites by reading their respective pieces of
documentation:

-   Python unit tests (see [Run the tests](install.md#run-the-tests)).
-   JavaScript unit tests (see [Frontend testing](testing.md)).
-   Redirect tests (see [Testing redirects](redirects.md#testing-redirects)).
-   Functional tests (see [Frontend testing](testing.md)).

# Deployed site URLs

Note that a deployment of Bedrock will actually trigger two separate
deployments: one serving all of `mozilla.org` and another serving
certain parts of `getpocket.com`

## Dev

-   *Mozorg URL:* <https://www-dev.allizom.org/>
-   *Pocket Marketing pages URL:* <https://dev.tekcopteg.com/>
-   *Bedrock locales:* dev repo
-   *Bedrock Git branch:* main, deployed on git push

## Staging

-   *Mozorg URL:* <https://www.allizom.org/>
-   *Pocket Marketing pages URL:* <https://www.tekcopteg.com/>
-   *Bedrock locales:* prod repo
-   *Bedrock Git branch:* stage, deployed on git push

## Production

-   *Mozorg URL:* <https://www.mozilla.org/>
-   *Pocket Marketing pages URL:* <https://getpocket.com/>
-   *Bedrock locales:* prod repo
-   *Bedrock Git branch:* prod, deployed on git push with date-tag

You can check the currently deployed git commit by checking
/revision.txt on any of these URLs.

# Tests in the lifecycle of a change

Below is an overview of the tests during the lifecycle of a change to
bedrock:

## Local development

The change is developed locally, and page specific integration tests can
be executed against a locally running instance of the application. If
testing changes to the website as a whole is required, then pushing
changes to the special `run-integration-tests` branch (see below) is
much faster than running the full test suite locally.

## Pull request

Once a pull request is submitted, a [Unit Tests Github
Action](https://github.com/mozilla/bedrock/actions/workflows/pull_request_tests.yml)
will run both the Python and JavaScript unit tests, as well as the suite
of redirect headless HTTP(s) response checks.

## Push to main branch

Whenever a change is pushed to the main branch, a new image is built and
deployed to the dev environment, and the full suite of headless and UI
tests are run. This is handled by the pipeline, and is subject to change
according to the settings in the Github Action workflow defined in
`bedrock/.github/workflows/integration_tests.yml`.

The tests for the dev environment are currently configured as follows:

-   Chrome (latest) via local Selenium grid.
-   Firefox (latest) via local Selenium grid.
-   Internet Explorer 11 (smoke tests) via [Sauce
    Labs](https://saucelabs.com/).
-   Internet Explorer 9 (sanity tests) via [Sauce
    Labs](https://saucelabs.com/).
-   Headless tests.

Note that now we have Mozorg mode and Pocket mode, we actually stand up
two dev, two stage and two test deployments and we run the appropriate
integration tests against each deployment: most tests are written for
Mozorg, but there are some for Pocket mode that also get run.

!!! info "The deployment workflow runs like this"

    1. A push to the `main`/`stage`/`prod`/`run-integration-tests` branch
    of `mozilla/bedrock` triggers a webhook ping to the (private)
    `mozilla-sre-deploy/deploy-bedrock` repo.
    2. A Github Action (GHA) in `mozilla-sre-deploy/deploy-bedrock` builds
    a "release"-ready Bedrock container image, which it stores in a
    private container registry (private because our infra requires
    container-image access to be locked down). Using the same commit, the
    workflow also builds an equivalent set of public Bedrock container
    images, which are pushed to Docker Hub.
    3. The GHA deploys the relevant container image to the appropriate environment.
    4. The GHA pings a webhook back in `mozilla/bedrock` to run integration
    tests against the environment that has just been deployed.

## Push to stage branch

Whenever a change is pushed to the stage branch, a production docker
image is built, published to [Docker
Hub](https://hub.docker.com/r/mozmeao/bedrock/tags), and deployed to a
[public staging environment](https://www.allizom.org). Once the new
image is deployed, the full suite of UI tests is run against it again,
but this time with the addition of the [headless download
tests]{.title-ref}.

## Push to prod branch (tagged) {#tagged-commit}

When a tagged commit is pushed to the `prod` branch, a production
container image (private, see above) is built, and a set of public
images is also built and pushed to [Docker
Hub](https://hub.docker.com/r/mozmeao/bedrock/tags) if needed (usually
this will have already happened as a result of a push to the `main` or
`stage` branch). The production image is deployed to each
[production](https://www.mozilla.org) deployment.

**Push to prod cheat sheet**

1.  Check out the `main` branch

2.  Make sure the `main` branch is up to date with
    `mozilla/bedrock main`

3.  Check that dev deployment is green:

    1.  View the [Integration Tests Github
        Action](https://github.com/mozilla/bedrock/actions/workflows/integration_tests.yml)
        and look at the run labelled
        `Run Integration tests for main`

4.  Check that stage deployment is also green
    (`Run Integration tests for stage`)

5.  Tag and push the deployment by running `bin/tag-release.sh --push`

!!! note

    By default the `tag-release.sh` script will push to the `origin` git
    remote. If you'd like for it to push to a different remote name you can
    either pass in a `-r` or `--remote` argument, or set the
    `MOZ_GIT_REMOTE` environment variable. So the following are equivalent:

    ``` bash
    bin/tag-release.sh --push -r mozilla
    ```

    ``` bash
    MOZ_GIT_REMOTE=mozilla bin/tag-release.sh --push
    ```

    And if you'd like to just tag and not push the tag anywhere, you may
    omit the `--push` parameter.

# What Is Currently Deployed?

You can look at the git log of the `main` branch to find the last commit
with a date-tag on it (e.g. 2022-05-05): this commit will be the last
one that was deployed to production. You can also use the
whatsdeployed.io service to get a nice view of what is actually
currently deployed to Dev, Stage, and Prod:

[![image](https://img.shields.io/badge/whatsdeployed-dev,stage,prod-green.svg)](https://whatsdeployed.io/s/RuO/mozilla/bedrock)

# Instance Configuration & Switches

We have a [separate repo](https://github.com/mozmeao/www-config) for
configuring our primary instances (dev, stage, and prod). The [docs for
updating configurations](https://mozmeao.github.io/www-config/) in that
repo are on their own page, but there is a way to tell what version of
the configuration is in use on any particular instance of bedrock. You
can go to the `/healthz-cron/` URL on an instance ([see
prod](https://www.mozilla.org/healthz-cron/) for example) to see the
current commit of all of the external Git repos in use by the site and
how long ago they were updated. The info on that page also includes the
latest version of the database in use, the git revision of the bedrock
code, and how long ago the database was updated. If you recently made a
change to one of these repos and are curious if the changes have made it
to production, this is the URL you should check.

# Updating Selenium

There are several components for Selenium, which are independently
versioned. The first is the Python client, and this can be updated via
the [test
dependencies](https://github.com/mozilla/bedrock/blob/main/requirements/dev.txt).
The other components are the Selenium versions used in both SauceLabs
and the local Selenium grid. These versions are selected automatically
based on the required OS / Browser configuration, so they should not
need to be updated or specified independently.

# Adding test runs

Test runs can be added by creating a new job in
`bedrock/.github/workflows/integration_tests.yml` with the desired
variables and pushing that branch to Github. For example, if you wanted
to run the smoke tests in IE10 (using Saucelabs) you could add the
following clause to the matrix:

``` yaml
- LABEL: test-ie10-saucelabs
  BROWSER_NAME: internet explorer
  BROWSER_VERSION: "10.0"
  DRIVER: SauceLabs
  PYTEST_PROCESSES: "8"
  PLATFORM: Windows 8
  MARK_EXPRESSION: smoke
```

You can use [Sauce Labs platform
configurator](https://wiki.saucelabs.com/display/DOCS/Platform+Configurator/)
to help with the parameter values.

# Pushing to the integration tests branch

If you have commit rights to our Github repo (mozilla/bedrock) you can
simply push your branch to the branch named `run-integration-tests`, and
the app will be deployed and the full suite of integration tests for
that branch will be run. Please announce in our Slack channel (#www on
mozilla.slack.com) that you'll be doing this so that we don't get
conflicts. Also remember that you'll likely need to force push, as
there may be commits on that branch which aren't in yours -- so, if you
have the `mozilla/bedrock` remote set as `mozilla`:

``` bash
git push -f mozilla $(git branch --show-current):run-integration-tests
```
