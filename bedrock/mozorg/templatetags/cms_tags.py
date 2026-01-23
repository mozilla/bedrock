# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from django_jinja import library
from jinja2 import pass_context


@pass_context
@library.filter
def add_utm_parameters(context: dict, value: str) -> str:
    """
    Appends UTM parameters to URLs pointing to *.mozilla.org,
    *.mozillafoundation.org, and *.firefox.com (except www.mozilla.org itself).
    """
    utm_parameters = context.get("utm_parameters", {})
    if utm_parameters and value:
        parsed_url = urlparse(value)
        host = parsed_url.netloc if value.startswith(("http://", "https://", "//")) else ""

        pattern = re.compile(
            r"^(\w+\.)?((mozilla\.org)|(mozillafoundation\.org)|(firefox\.com))",
            re.IGNORECASE,
        )
        # Exclude www.mozilla.org (the current site) from UTM modification
        if host and host not in ["www.mozilla.org", "mozilla.org"] and pattern.match(host):
            query = parse_qs(parsed_url.query)
            query.update(utm_parameters)
            new_query = urlencode(query, doseq=True)
            return urlunparse(parsed_url._replace(query=new_query))
    return value
