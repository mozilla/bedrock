#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections import defaultdict

import click
import requests


@click.command()
@click.option("-n", type=click.IntRange(0, 100, clamp=True), default=100, help="Number of requests to make")
@click.argument("url", type=str, required=True)
def check_for_report_uri(url, n=100):
    """
    Check if a URL has a Content-Security-Policy header with a report-uri directive.
    """
    print(f"Checking {url}")
    results = defaultdict(int)
    for _ in range(n):
        resp = requests.get(url)

        if "Content-Security-Policy" in resp.headers:
            header = resp.headers["Content-Security-Policy-Report-Only"]
            if "report-uri" in header:
                results["report-uri present"] += 1
            else:
                results["report-uri not present"] += 1
        else:
            results["No CSP header"] += 1

    print(f"{n} requests made")
    print(results)


if __name__ == "__main__":
    check_for_report_uri()
