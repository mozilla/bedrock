# 5. Use a Single Docker Image For All Deployments

Date: 2020-07-07

## Status

Accepted

## Context

We currently build an individual docker image for each deployment (dev, stage, and prod) that contains the
proper data for that environment. It would save time and testing if we only built a single image that could
be promoted to each environment and loaded with the proper data at startup.

## Decision

We will use a Kubernetes DaemonSet to ensure that a data updater pod is running on each node in a cluster. This
pod will keep the database and l10n files updated in a volume that will be used by the other bedrock pods to
access the data.

[GitHub issue](https://github.com/mozmeao/infra/issues/1306)

## Consequences

This change means that bedrock will be more simple to run because each pod will no longer need to be responsible for
keeping its data updated, and so it will run only the bedrock web process and not also the updater daemon. It also
means that there is a risk of a bedrock pod being run on a node that hasn't had the updater pod run yet, so there
would be no available data. We will handle this by ensuring that bedrock won't start when the data isn't available,
and so k8s will not send traffic to those pods until they're successfully up and responding, and will keep trying
to start pods on the node untill they succeed.
