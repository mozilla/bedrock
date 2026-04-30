# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.fixtures.base_fixtures import get_test_index_page
from bedrock.mozorg.models import HomePage


def get_springboard_variants() -> list[dict]:
    """Return list of SpringboardBlock data variants for testing.

    Returns:
        List of block data dictionaries representing different configurations
    """
    return [
        # Variant 1: With heading and anchor_id
        {
            "type": "springboard_block",
            "value": {
                "settings": {
                    "anchor_id": "resources",
                    "background_color": "",
                },
                "heading": "Latest Resources",
                "column_one": "Type",
                "column_two": "Author",
                "column_three": "Topic",
                "column_four": "Preview",
                "springboard_items": [
                    {
                        "url": "https://example.com/article1",
                        "link_attributes": "Understanding privacy in the digital age",
                        "type": "Article",
                        "icon": "article",
                        "topic": "Privacy & Security",
                        "author": "Jane Doe",
                        "preview": "Understanding privacy in the digital age",
                    },
                    {
                        "url": "https://example.com/video1",
                        "link_attributes": "How to secure your online accounts",
                        "type": "Video",
                        "icon": "video",
                        "topic": "Privacy & Security",
                        "author": "John Smith",
                        "preview": "How to secure your online accounts",
                    },
                ],
            },
            "id": "springboard-variant-1",
        },
        # Variant 2: Without heading, different items
        {
            "type": "springboard_block",
            "value": {
                "settings": {
                    "anchor_id": "",
                    "background_color": "",
                },
                "heading": "",
                "column_one": "Format",
                "column_two": "Creator",
                "column_three": "Category",
                "column_four": "Description",
                "springboard_items": [
                    {
                        "url": "https://example.com/podcast1",
                        "link_attributes": "Latest tech trends discussion",
                        "type": "Podcast",
                        "icon": "podcast",
                        "topic": "",
                        "author": "Mozilla Team",
                        "preview": "Latest tech trends discussion",
                    },
                    {
                        "url": "https://example.com/blog1",
                        "link_attributes": "The future of open source software",
                        "type": "Article",
                        "icon": "article",
                        "topic": "",
                        "author": "Alice Johnson",
                        "preview": "The future of open source software",
                    },
                    {
                        "url": "https://example.com/webinar1",
                        "link_attributes": "Teaching coding to beginners",
                        "type": "Video",
                        "icon": "video",
                        "topic": "",
                        "author": "Bob Williams",
                        "preview": "Teaching coding to beginners",
                    },
                ],
            },
            "id": "springboard-variant-2",
        },
    ]


def get_springboard_test_page() -> HomePage:
    """Create a HomePage with all springboard block variants for testing.

    Returns:
        HomePage instance with springboard blocks populated
    """
    # Get variants
    variants = get_springboard_variants()

    # Get the index page as parent
    index_page = get_test_index_page()

    # Check if test page already exists
    test_page = HomePage.objects.filter(slug="springboard-block-test").first()
    if test_page:
        return test_page

    # Create the test page with all variants
    test_page = HomePage(
        title="Springboard Block Test Page",
        slug="springboard-block-test",
        content=variants,
    )

    index_page.add_child(instance=test_page)
    test_page.save_revision().publish()

    return test_page
