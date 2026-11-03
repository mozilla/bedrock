#! /bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

# Re-resolve everything, so subdeps pick up updates too. The 7-day supply-chain
# delay is set via `exclude-newer` in `pyproject.toml`, which also explains how
# to exempt a single package for an urgent fix.
uv lock --upgrade
