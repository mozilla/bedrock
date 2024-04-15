#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
from collections import defaultdict

import requests


def check_for_report_uri(url, sample_size):
    print(f"Checking {url}")
    results = defaultdict(int)
    for _ in range(sample_size):
        resp = requests.get(url)

        if "Content-Security-Policy" in resp.headers:
            header = resp.headers["Content-Security-Policy"]
            if "report-uri" in header:
                results["report-uri present"] += 1
            else:
                results["report-uri not present"] += 1
        else:
            results["No CSP header"] += 1

    print(f"{sample_size} requests made")
    print(results)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "Usage: seek_scp_report_uri.py URL OPTIONAL_SAMPLE_SIZE\n",
            "e.g. seek_scp_report_uri.py https://example.com/path/ 200",
        )
        sys.exit(1)

    try:
        url = sys.argv[1]
    except IndexError:
        print("A URL must be provided to check, ideally one not behind a CDN")
        sys.exit(1)

    try:
        sample_size = int(sys.argv[2])
    except ValueError:
        print("A sample size must be provided as an integer")
        sys.exit(1)
    except IndexError:
        sample_size = 100

    check_for_report_uri(url, sample_size)
