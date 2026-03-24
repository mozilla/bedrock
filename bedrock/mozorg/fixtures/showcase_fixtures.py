# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.fixtures.base_fixtures import get_placeholder_image, get_test_index_page
from bedrock.mozorg.models import HomePage


def get_showcase_variants(image_id: int) -> list[dict]:
    """Return list of ShowcaseBlock data variants for testing.

    Args:
        image_id: ID of the placeholder image to use

    Returns:
        List of block data dictionaries representing different configurations
    """
    return [
        # Variant 1: Default white background, no anchor
        {
            "type": "showcase_block",
            "value": {
                "settings": {
                    "background_color": "",
                    "anchor_id": "",
                },
                "heading": "State of Mozilla 2024",
                "body": "<p>Read our annual report on Mozilla's mission and impact.</p>",
                "image": image_id,
                "image_alt": "State of Mozilla report cover",
                "sub_heading": "Supporting a healthy internet",
                "cta_text": "Read the report",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://www.mozilla.org/state-of-mozilla",
                    "new_window": False,
                },
            },
            "id": "showcase-variant-1",
        },
        # Variant 2: Dark background
        {
            "type": "showcase_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-dark",
                    "anchor_id": "",
                },
                "heading": "Firefox Innovations",
                "body": "<p>Discover the <strong>latest features</strong> in Firefox.</p><p>Built for privacy and speed.</p>",
                "image": image_id,
                "image_alt": "",
                "sub_heading": "Browse with confidence",
                "cta_text": "Learn more",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://www.mozilla.org/firefox/features",
                    "new_window": False,
                },
            },
            "id": "showcase-variant-2",
        },
        # Variant 3: Green background with anchor_id
        {
            "type": "showcase_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-green",
                    "anchor_id": "showcase-section",
                },
                "heading": "Open Source Leadership",
                "body": "<p>How Mozilla champions open source technology.</p>",
                "image": image_id,
                "image_alt": "Open source community collaboration",
                "sub_heading": "Building together",
                "cta_text": "Explore our work",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://www.mozilla.org/open-source",
                    "new_window": False,
                },
            },
            "id": "showcase-variant-3",
        },
        # Variant 4: Orange background with new_window=True
        {
            "type": "showcase_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-orange",
                    "anchor_id": "",
                },
                "heading": "Community Impact",
                "body": "<p>See how our community is making a difference.</p>",
                "image": image_id,
                "image_alt": "Mozilla community event",
                "sub_heading": "Join the movement",
                "cta_text": "View impact report",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://foundation.mozilla.org/impact",
                    "new_window": True,
                },
            },
            "id": "showcase-variant-4",
        },
    ]


def get_showcase_test_page() -> HomePage:
    """Create a HomePage with all showcase block variants for testing.

    Returns:
        HomePage instance with showcase blocks populated
    """
    # Ensure we have a placeholder image
    placeholder_image = get_placeholder_image()

    # Get variants with the image ID
    variants = get_showcase_variants(placeholder_image.id)

    # Get the index page as parent
    index_page = get_test_index_page()

    # Check if test page already exists
    test_page = HomePage.objects.filter(slug="showcase-block-test").first()
    if test_page:
        return test_page

    # Create the test page with all variants
    test_page = HomePage(
        title="Showcase Block Test Page",
        slug="showcase-block-test",
        content=variants,
    )

    index_page.add_child(instance=test_page)
    test_page.save_revision().publish()

    return test_page
