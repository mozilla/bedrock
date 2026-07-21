# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.fixtures.base_fixtures import get_test_index_page
from bedrock.mozorg.models import AboutUsPage


def get_prose_variants() -> list[dict]:
    """Return list of ProseBlock data variants for testing.

    Returns:
        List of block data dictionaries representing different configurations
    """
    return [
        # Variant 1: Two-column layout (default), no reverse, white background
        {
            "type": "prose_block",
            "value": {
                "settings": {
                    "background_color": "",
                    "two_column_layout": True,
                    "reverse": False,
                    "anchor_id": "",
                },
                "heading": "Our Mission",
                "sub_heading": "",
                "body": "<p>Mozilla works to ensure the internet remains a public resource that is open and accessible to all.</p>",
                "cta_text": "",
                "cta_link": {},
            },
            "id": "prose-variant-1",
        },
        # Variant 2: Single column, dark background
        {
            "type": "prose_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-dark",
                    "two_column_layout": False,
                    "reverse": False,
                    "anchor_id": "",
                },
                "heading": "Our Values",
                "sub_heading": "",
                "body": "<p>We believe in an internet that is open, safe, and accessible to everyone.</p>",
                "cta_text": "",
                "cta_link": {},
            },
            "id": "prose-variant-2",
        },
        # Variant 3: Two-column, reversed, green background, with anchor_id
        {
            "type": "prose_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-green",
                    "two_column_layout": True,
                    "reverse": True,
                    "anchor_id": "pledge",
                },
                "heading": "Our Pledge",
                "sub_heading": "",
                "body": "<p>We pledge to keep fighting for a healthier internet.</p>",
                "cta_text": "",
                "cta_link": {},
            },
            "id": "prose-variant-3",
        },
        # Variant 4: Two-column, with sub_heading, orange background
        {
            "type": "prose_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-orange",
                    "two_column_layout": True,
                    "reverse": False,
                    "anchor_id": "",
                },
                "heading": "Our Work",
                "sub_heading": "What we do every day",
                "body": "<p>We advocate, research, build, and fund work that keeps the internet healthy.</p>",
                "cta_text": "",
                "cta_link": {},
            },
            "id": "prose-variant-4",
        },
        # Variant 5: With section CTA
        {
            "type": "prose_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-pink",
                    "two_column_layout": True,
                    "reverse": False,
                    "anchor_id": "",
                },
                "heading": "Read More",
                "sub_heading": "",
                "body": "<p>Learn more about what we do and why it matters.</p>",
                "cta_text": "Read the report",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://www.mozilla.org/report",
                    "new_window": False,
                },
            },
            "id": "prose-variant-5",
        },
        # Variant 6: With section CTA, new_window=True
        {
            "type": "prose_block",
            "value": {
                "settings": {
                    "background_color": "",
                    "two_column_layout": True,
                    "reverse": False,
                    "anchor_id": "",
                },
                "heading": "External Link",
                "sub_heading": "",
                "body": "<p>This block has a CTA that opens in a new window.</p>",
                "cta_text": "Visit site",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://foundation.mozilla.org",
                    "new_window": True,
                },
            },
            "id": "prose-variant-6",
        },
    ]


def get_prose_test_page() -> AboutUsPage:
    """Create an AboutUsPage with all prose block variants for testing.

    Returns:
        AboutUsPage instance with prose blocks populated
    """
    variants = get_prose_variants()
    index_page = get_test_index_page()

    test_page = AboutUsPage.objects.filter(slug="prose-block-test").first()
    if test_page:
        return test_page

    test_page = AboutUsPage(
        title="Prose Block Test Page",
        slug="prose-block-test",
        content=variants,
    )

    index_page.add_child(instance=test_page)
    test_page.save_revision().publish()

    return test_page
