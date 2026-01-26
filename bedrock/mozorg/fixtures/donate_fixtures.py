# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.fixtures.base_fixtures import get_placeholder_image, get_test_index_page
from bedrock.mozorg.models import HomePage


def get_donate_variants(image_id: int) -> list[dict]:
    """Return list of DonateBlock data variants for testing.

    Args:
        image_id: ID of the placeholder image to use

    Returns:
        List of block data dictionaries representing different configurations
    """
    return [
        # Variant 1: Default gray background, no anchor
        {
            "type": "donate_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-gray",
                    "anchor_id": "",
                },
                "heading": "Support Mozilla",
                "body": "<p>Help us build a better internet for everyone.</p>",
                "image": image_id,
                "image_alt": "Mozilla community event",
                "cta_text": "Donate Now",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://foundation.mozilla.org/donate",
                    "new_window": False,
                },
            },
            "id": "donate-variant-1",
        },
        # Variant 2: Pink background
        {
            "type": "donate_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-pink",
                    "anchor_id": "",
                },
                "heading": "Join the Movement",
                "body": "<p>Your donation powers our mission.</p><p>Every contribution counts.</p>",
                "image": image_id,
                "image_alt": "",
                "cta_text": "Give Today",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://foundation.mozilla.org/give",
                    "new_window": False,
                },
            },
            "id": "donate-variant-2",
        },
        # Variant 3: With anchor_id
        {
            "type": "donate_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-green",
                    "anchor_id": "donate-section",
                },
                "heading": "Make a Difference",
                "body": "<p>Support open source.</p>",
                "image": image_id,
                "image_alt": "Open source illustration",
                "cta_text": "Contribute",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://foundation.mozilla.org/contribute",
                    "new_window": False,
                },
            },
            "id": "donate-variant-3",
        },
        # Variant 4: With new_window=True
        {
            "type": "donate_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-orange",
                    "anchor_id": "",
                },
                "heading": "Support Our Work",
                "body": "<p>Opens in a <strong>new window</strong>.</p>",
                "image": image_id,
                "image_alt": "",
                "cta_text": "Donate (New Window)",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://foundation.mozilla.org/external",
                    "new_window": True,
                },
            },
            "id": "donate-variant-4",
        },
    ]


def get_donate_test_page() -> HomePage:
    """Create a HomePage with all donate block variants for testing.

    Returns:
        HomePage instance with donate blocks populated
    """
    # Ensure we have a placeholder image
    placeholder_image = get_placeholder_image()

    # Get variants with the image ID
    variants = get_donate_variants(placeholder_image.id)

    # Get the index page as parent
    index_page = get_test_index_page()

    # Check if test page already exists
    test_page = HomePage.objects.filter(slug="donate-block-test").first()
    if test_page:
        return test_page

    # Create the test page with all variants
    test_page = HomePage(
        title="Donate Block Test Page",
        slug="donate-block-test",
        content=variants,
    )

    index_page.add_child(instance=test_page)
    test_page.save_revision().publish()

    return test_page
