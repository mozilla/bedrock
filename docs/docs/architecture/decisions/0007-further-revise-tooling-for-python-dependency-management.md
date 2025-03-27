# 7. Further revise tooling for Python dependency management

Date: 2022-03-02

## Status

Proposed

## Context

While pip-compile-multi gave us plenty fot benefits (see ADR 0006) the lack
of Dependabot support was an annoyance and replacing it with alternatives
seemed fairly involved.
## Decision

We've downgraded to regular `pip-compile` and instead are doing the extra legwork in the Makefile instead. The input files are indentical, so we do not need to pin sub-dependencies, and we still
get automatic hash generation for all packages.
## Consequences

There should be no downsides to switching away from pip-compile-multi in this context. If Dependabot
still does not manage to parse our multiple requirements files, we should look to renaming them in case
that tips the balance (as has been suggested by a colleague)
