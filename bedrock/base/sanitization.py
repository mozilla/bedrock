# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Shared HTML sanitization utilities using justhtml.
"""

from justhtml import JustHTML, SanitizationPolicy, UrlPolicy, UrlRule

# URL policy that allows common schemes for href and src attributes.
# Using default_handling="strip" ensures any URL attributes not explicitly
# listed are removed, preventing potential javascript: or other dangerous schemes.
_URL_RULE = UrlRule(allowed_schemes=["http", "https", "mailto", "tel"])
_URL_POLICY = UrlPolicy(
    default_handling="strip",
    allow_rules={
        ("a", "href"): _URL_RULE,
        ("img", "src"): _URL_RULE,
        ("img", "srcset"): _URL_RULE,
    },
)


def strip_all_tags(html: str) -> str:
    """Remove all HTML tags, returning only text content."""
    policy = SanitizationPolicy(
        allowed_tags=set(),
        allowed_attributes={"*": []},
        disallowed_tag_handling="unwrap",
        drop_content_tags=set(),  # Preserve content from all tags (bleach compat)
    )
    return JustHTML(html, safe=True, policy=policy, fragment=True).to_html(pretty=False)


def sanitize_html(html: str, allowed_tags: set, allowed_attributes: dict) -> str:
    """Sanitize HTML using an allowlist of tags and attributes.

    Disallowed tags are escaped (converted to &lt;tag&gt;).
    """
    policy = SanitizationPolicy(
        allowed_tags=allowed_tags,
        allowed_attributes=allowed_attributes,
        disallowed_tag_handling="escape",
        url_policy=_URL_POLICY,
    )
    return JustHTML(html, safe=True, policy=policy, fragment=True).to_html(pretty=False)
