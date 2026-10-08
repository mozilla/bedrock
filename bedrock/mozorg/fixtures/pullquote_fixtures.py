# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.fixtures.article_fixtures import get_article_test_page
from bedrock.mozorg.models import ArticlePage


def get_pullquote_variants() -> list[dict]:
    """Return list of PullquoteBlock data variants for testing.

    Returns:
        List of block data dictionaries representing different configurations
    """
    return [
        # Variant 1: Pullquote with author and a citation with a source link, white background
        {
            "type": "pullquote_block",
            "value": {
                "settings": {"background_color": ""},
                "quote": "<p>The internet is a <strong>global public resource</strong> that must remain open and accessible.</p>",
                "author": "Mozilla Manifesto",
                "citation": '<p>Principle 2, <a href="https://www.mozilla.org/about/manifesto/"><i>The Mozilla Manifesto</i></a>, 2007</p>',
            },
            "id": "pullquote-variant-1",
        },
        # Variant 2: Pullquote with author only, pink background
        {
            "type": "pullquote_block",
            "value": {
                "settings": {"background_color": "m24-t-pink"},
                "quote": "<p>A quote attributed to an author with no citation.</p>",
                "author": "Jane Doe",
                "citation": "",
            },
            "id": "pullquote-variant-2",
        },
        # Variant 3: Pullquote with no attribution, white background
        {
            "type": "pullquote_block",
            "value": {
                "settings": {"background_color": ""},
                "quote": "<p>An unattributed quote.</p>",
                "author": "",
                "citation": "",
            },
            "id": "pullquote-variant-3",
        },
    ]


def get_pullquote_test_page() -> ArticlePage:
    """Create an ArticlePage with all pullquote variants for testing.

    Returns:
        ArticlePage instance with pullquote blocks in its content
    """
    return get_article_test_page(slug="pullquote-block-test", title="Pullquote Block Test Page", content=get_pullquote_variants())
