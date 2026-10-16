#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import subprocess
import tomllib

# Allow `print` statements.
# ruff: noqa: T201


def extract_pinned(requirements):
    """Extract pinned dependencies from a list of PEP 508 requirement strings."""
    pinned_deps = {}
    for requirement in requirements:
        # Match requirements with version constraints (pinned dependencies), skipping any `[extras]`
        pinned_match = re.match(r"^([^=<>\[\s]+)(?:\[[^\]]*\])?(?:==|>=)([^,;\s]+)", requirement.strip().lower())
        if pinned_match:
            # Normalize the name the way `uv pip list` prints it, e.g. `fluent.runtime` -> `fluent-runtime`
            pkg_name = re.sub(r"[-_.]+", "-", pinned_match.group(1))
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


def check_outdated_for_requirements(requirement_groups):
    """Check outdated packages for each named group of requirements."""
    # Get outdated packages once for efficiency
    raw_outdated, outdated = get_outdated_packages()

    for group_name, requirements in requirement_groups.items():
        pinned = extract_pinned(requirements)

        outdated_dep = [p for p in outdated if p in pinned]

        print(f"\nOutdated pinned packages for {group_name}:")
        if outdated_dep:
            for pkg_name in sorted(outdated_dep):
                print(f"    {pkg_name} {pinned[pkg_name]} -> {outdated[pkg_name]}")
        else:
            print("  No outdated pinned packages.")

    print("\nAll outdated packages:")
    print("\n".join(raw_outdated))


def main():
    with open("pyproject.toml", "rb") as file:
        pyproject = tomllib.load(file)
    requirement_groups = {
        "project.dependencies": pyproject["project"]["dependencies"],
        "dependency-groups.dev": pyproject["dependency-groups"]["dev"],
        "dependency-groups.docs": pyproject["dependency-groups"]["docs"],
    }
    check_outdated_for_requirements(requirement_groups)


if __name__ == "__main__":
    main()
