# 6. Revise tooling for Python dependency management

Date: 2022-02-25

## Status

Superseded by 0007, but the context in this ADR is still useful

## Context

At the moment of revisiting our dependency-management approach, Bedrock's Python dependencies were installed from a hand-cut `requirements/*.txt` files which (sensibly) included hashes so that we could be sure about what our Python package installer, `pip`, was actually installing.

However, this process was onerous:
* We had a number of requirements files, `base`, `prod`, `dev`, `migration` (no longer required but still being processed at installation time) and `docs` - all of which had to be hand-maintained.
* Hashes needed to be generated when adding/updating a dependency. This was done with a specific tool [`hashin`](https://github.com/peterbe/hashin) and needed to be done for each requirement.
* When `pip` detects hashes in a requirements file, it automatically requires hashes for _all_ packages it installs, including subdependencies of dependecies mentioned in `requirements/*.txt`. This in turn meant that adding or updating a new dep often required hashing-in one or more subdeps -- and at worst, a change or niggle with `pip` would result in a new subdep being implicitly required, which would then fail to install because it was not hashed in to the requirements file.

Other projects (both within MEAO and across Mozilla) used more sophisticated dependency management tools, including:
* `pip-tools` - which draws reqs from an input file and generates a requirements.txt complete with hashes
* `pip-compile-multi` - which extends pip-tools' behaviour to support multiple output files and shared input files
* `poetry` - which combines a lockfile approach with a standalone virtual environment
* `pipenv` - which similarly combines a lockfile with a virtual environment
* `conda` - a language-agnostic package manager and environment management system
* simply `pip`

The ideal solution would support all of the following:
* Simple input file format/syntax
* Ability to pin dependencies
* Support for installing with hash-checking of packages
* Automatic hashing of requirements, rather than having to manually do it with `hashin` et al.
* Support for multiple build configurations (eg prod, dev, docs)
* Dependabot compatibility, so we still get alerts and updates
* An unopinionated approach to virtualenvs – can work with and without them, so that developers can use the virtualenv tooling they prefer and we don't have to use a virtualenv in our containers if we don't want to
* Sufficiently active maintenance of the project
* Use/knowledge of the tooling elsewhere in the broader organisation

## Decision

After evaluating the above, including `pip-tools`, `pip-compile-multi` and `poetry` in greater depth, `pip-compile-multi` was selected.

Significant factors were how allows us to pin our top-level dependencies in a clutter-free input format, supports inheritance between files and miltiple output files with ease, and it automatically generates hashes for subdependencies.

## Consequences

`pip-compile-multi` has been easily integrated into the Bedrock workflow, but there is one non-trivial downside: Github's Dependabot service does not play well with the combination of multiple requirements files and inheritance between them. As such, does not currently produce reliable updates (either partial updates or some requirements files seem to be ignored entirely). See https://github.com/dependabot/dependabot-core/issues/536

Strictly, though, we don't _need_ the convenience of Dependabot - we have a `make` command to identify stale deps and recompiling is another, single, `make` command. Also, we're more likely to compile a bunch of Dependabot PRs into one changeset (eg with [`paul-mclendahand`](https://github.com/willkg/paul-mclendahand)), than to merge them straight to `master`/`main` one at at time. As long as we're getting Github security alerts for vulnerable dependencies, we'll be OK.

That said, if we did find we needed Dependabot compatibility, `pip-tools` and some extra legwork in the Makefile to deal with prod, dev and docs deps separately would likely be a viable alternative.
