# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.fixtures.base_fixtures import get_placeholder_image, get_test_index_page
from bedrock.mozorg.models import AboutUsPage


def get_showcase_gallery_variants(image_id: int) -> list[dict]:
    """Return list of ShowcaseGalleryBlock data variants for testing.

    Args:
        image_id: ID of the placeholder image to use

    Returns:
        List of block data dictionaries representing different configurations
    """
    return [
        # Variant 1: Default white background, no anchor, multiple tiles
        {
            "type": "showcase_gallery_block",
            "value": {
                "settings": {
                    "background_color": "",
                    "anchor_id": "",
                },
                "heading": "Working at Mozilla",
                "tiles": [
                    {"image": image_id, "image_alt": "Mozilla team working together"},
                    {"image": image_id, "image_alt": "Mozilla office space"},
                    {"image": image_id, "image_alt": "Mozilla team event"},
                    {"image": image_id, "image_alt": ""},
                ],
                "body": "Join a team that believes the internet is for everyone.",
                "cta_text": "See open roles",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://www.mozilla.org/careers",
                    "new_window": False,
                },
            },
            "id": "showcase-gallery-variant-1",
        },
        # Variant 2: Dark background
        {
            "type": "showcase_gallery_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-dark",
                    "anchor_id": "",
                },
                "heading": "Our Culture",
                "tiles": [
                    {"image": image_id, "image_alt": "Mozilla culture photo"},
                    {"image": image_id, "image_alt": ""},
                ],
                "body": "A mission-driven organization where your work matters.",
                "cta_text": "Learn about our culture",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://www.mozilla.org/about/culture",
                    "new_window": False,
                },
            },
            "id": "showcase-gallery-variant-2",
        },
        # Variant 3: Green background with anchor_id
        {
            "type": "showcase_gallery_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-green",
                    "anchor_id": "careers-section",
                },
                "heading": "Benefits and Perks",
                "tiles": [
                    {"image": image_id, "image_alt": "Employee benefits"},
                    {"image": image_id, "image_alt": "Flexible working"},
                ],
                "body": "We offer competitive benefits that support your whole life.",
                "cta_text": "View benefits",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://www.mozilla.org/careers/benefits",
                    "new_window": False,
                },
            },
            "id": "showcase-gallery-variant-3",
        },
        # Variant 4: Orange background, new_window=True
        {
            "type": "showcase_gallery_block",
            "value": {
                "settings": {
                    "background_color": "m24-t-orange",
                    "anchor_id": "",
                },
                "heading": "Join Mozilla",
                "tiles": [
                    {"image": image_id, "image_alt": "Mozilla team photo"},
                    {"image": image_id, "image_alt": "Mozilla campus"},
                ],
                "body": "Help us keep the internet open and accessible.",
                "cta_text": "Apply now",
                "cta_link": {
                    "link_to": "custom_url",
                    "custom_url": "https://www.mozilla.org/careers/apply",
                    "new_window": True,
                },
            },
            "id": "showcase-gallery-variant-4",
        },
    ]


def get_showcase_gallery_test_page() -> AboutUsPage:
    """Create an AboutUsPage with all showcase gallery block variants for testing.

    Returns:
        AboutUsPage instance with showcase gallery blocks populated
    """
    placeholder_image = get_placeholder_image()
    variants = get_showcase_gallery_variants(placeholder_image.id)
    index_page = get_test_index_page()

    test_page = AboutUsPage.objects.filter(slug="showcase-gallery-block-test").first()
    if test_page:
        return test_page

    test_page = AboutUsPage(
        title="Showcase Gallery Block Test Page",
        slug="showcase-gallery-block-test",
        content=variants,
    )

    index_page.add_child(instance=test_page)
    test_page.save_revision().publish()

    return test_page
