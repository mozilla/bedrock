# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.fixtures.article_fixtures import get_article_test_page
from bedrock.mozorg.models import ArticlePage


def get_intro_variants() -> list[dict]:
    """Return list of IntroBlock data variants for testing.

    Returns:
        List of block data dictionaries representing different configurations
    """
    return [
        # Variant 1: Heading and body, white background, default (X large) heading
        {
            "type": "intro_block",
            "value": {
                "settings": {"background_color": "", "heading_size": ""},
                "heading": "Guard the internet",
                "body": "<p>Mozilla is working to put people <strong>back in charge</strong> of their online lives.</p>",
            },
            "id": "intro-variant-1",
        },
        # Variant 2: Heading only, dark background, 2X large heading
        {
            "type": "intro_block",
            "value": {
                "settings": {"background_color": "m24-t-dark", "heading_size": "m24-t-2xl"},
                "heading": "A heading with no body",
                "body": "",
            },
            "id": "intro-variant-2",
        },
        # Variant 3: Body with a link, green background, large heading
        {
            "type": "intro_block",
            "value": {
                "settings": {"background_color": "m24-t-green", "heading_size": "m24-t-lg"},
                "heading": "An intro with a link",
                "body": '<p>Read more <a href="https://www.mozilla.org/about/">about Mozilla</a>.</p>',
            },
            "id": "intro-variant-3",
        },
    ]


def get_intro_test_pages() -> list[ArticlePage]:
    """Create one ArticlePage per intro variant, since a page holds a single intro.

    Returns:
        List of ArticlePage instances, in the same order as get_intro_variants()
    """
    return [
        get_article_test_page(slug=f"intro-block-test-{index}", title=f"Intro Block Test Page {index}", intro=variant)
        for index, variant in enumerate(get_intro_variants(), start=1)
    ]
