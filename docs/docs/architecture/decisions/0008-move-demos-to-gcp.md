# 8. Move Demos To GCP

Date: 2022-07-14

## Status

Accepted

## Context

Previously, demos for Bedrock were run on Heroku. This worked fine, but Heroku's
recent security incident there meant our integration had to be disabled,
prompting discussion of self-managed demo instances.

In addition, while it was possible to demo Bedrock in Pocket Mode on Heroku, by
amending the settings via the Heroku web UI, the domains set up
(www-demoX.allizom.org) were originally set up for Mozorg, and as such may be
confusing for colleagues reviewing Pocket changes. Flipping and un-flipping
settings in Heroku to enable Mozorg Mode or Pocket Mode was also extra legwork
that we ideally would do without, too.

## Decision

We have implemented a new, self-managed, approach to running demos, using a
handful of Google Cloud Platform services. Cloud Build and Cloud Run are the
most significant ones.

Cloud Build has triggers which monitor pushes to specific branches, then
builds a Bedrock container from the branch, using the appropriate env vars
for Pocket or Mozorg use, including the SITE_MODE env var that specifies the
mode Bedrock runs in.

Cloud Run then deploys the built container as a 'serverless' webapp. By
default, supervisord runs in the container, so it updates DB and L10N files
automatically.

This process is triggered by a simple push to a specific target branch. e.g.
pushing code to mozorg-demo-2 will result in the relevant code being deployed in
Mozorg mode to www-demo2.allizom.org, while pushing to pocket-demo-4 will deploy
it to www-demo4.tekcopteg.com in Pocket mode.

Environment variables can also be configured by developers, via two dedicated
env files in the Bedrock codebase, which are only used for demo services.
Clashes are unlikely, and can still be managed with common sense.

## Consequences

Upsides:

It is now easier to stand up Pocket demos in addition to existing Mozorg demos,
plus we have full control over the infrastructure our demos are run on.

We will no longer need to use Heroku for demos. In the future, we may also be
able to support ad-hoc 'review apps', which we have also used Heroku for in
the past.

Downsides:

1) If a new secret value is required on a demo instance, and so that value
cannot go into the demo env vars file because our codebase is public, some
SRE-like devops is needed to add that secret value to GCP's Secret Manager
Service. This can be quick, but requires understanding how that side fits
together, plus access, so may need a backender to add them.

2) At the moment, only the MEAO Backend team have GCP access, which is handy
to monitor whether a demo has successfull be pushed out, or to amend secrets,
etc. Both of these issues can be addressed without a lot of work.
