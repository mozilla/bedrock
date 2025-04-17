#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import argparse
import os
import sys
from pathlib import Path

from moz.l10n.paths import L10nConfigPaths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", dest="repo_path", help="Path to repository clone", required=True)
    args = parser.parse_args()

    # Find all TOML files in l10n/configs
    repo_path = args.repo_path
    config_path = Path(os.path.join(repo_path, "l10n", "configs"))
    config_files = list(config_path.glob("*.toml"))

    errors = []
    for config in config_files:
        toml_path = os.path.join(repo_path, config)
        project_config_paths = L10nConfigPaths(toml_path)
        reference_files = [os.path.abspath(ref_path) for ref_path in project_config_paths.ref_paths]

        for file in reference_files:
            if not os.path.exists(file):
                errors.append(f"[{config}] {os.path.relpath(file, repo_path)}")

    if errors:
        print("Missing reference files:")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("No missing reference files.")


if __name__ == "__main__":
    main()
