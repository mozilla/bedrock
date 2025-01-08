#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import subprocess

# Allow `print` statements.
# ruff: noqa: T201


def extract_pinned(requirements_file):
    """Extract pinned dependencies from a requirements file."""
    pinned_deps = {}
    with open(requirements_file) as file:
        for line in file:
            line = line.strip().lower()
            # Skip comments and empty lines
            if line and not line.startswith("#"):
                # Match lines with version constraints (pinned dependencies) using non-capturing groups for the operator
                pinned_match = re.match(r"^(\S+)(?:==|>=)(\S+)", line)
                if pinned_match:
                    pkg_name = pinned_match.group(1)
                    version = pinned_match.group(2)
                    pinned_deps[pkg_name] = version
    return pinned_deps


def get_outdated_packages():
    """Get a list of outdated packages and their latest versions using `uv`."""
    result = subprocess.run(["uv", "pip", "list", "--no-cache", "--outdated"], capture_output=True, text=True)
    outdated = {}
    raw = result.stdout.splitlines()
    for line in raw[2:]:  # Skip header lines
        if line:
            parts = line.split()
            if len(parts) >= 3:
                package_name = parts[0].lower()
                latest_version = parts[2]
                outdated[package_name] = latest_version
    return raw, outdated


def check_outdated_for_requirements(requirements_files):
    """Check outdated packages for each requirements file."""
    # Get outdated packages once for efficiency
    raw_outdated, outdated = get_outdated_packages()

    for req_file in requirements_files:
        # Extract pinned and unpinned dependencies for the current requirements file
        pinned = extract_pinned(req_file)

        outdated_dep = [p for p in outdated if p in pinned]

        print(f"\nOutdated pinned packages for {req_file}:")
        if outdated_dep:
            for pkg_name in sorted(outdated_dep):
                print(f"    {pkg_name} {pinned[pkg_name]} -> {outdated[pkg_name]}")
        else:
            print("  No outdated pinned packages.")

    print("\nAll outdated packages:")
    print("\n".join(raw_outdated))


def main():
    requirements_files = [f"requirements/{f}" for f in ("prod.in", "dev.in", "docs.in")]
    check_outdated_for_requirements(requirements_files)


if __name__ == "__main__":
    main()
