# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.fixtures.article_fixtures import get_article_test_page
from bedrock.mozorg.fixtures.base_fixtures import get_placeholder_image
from bedrock.mozorg.models import ArticlePage


def get_image_caption_variants(image_id: int) -> list[dict]:
    """Return list of ImageCaptionBlock data variants for testing.

    Args:
        image_id: ID of the placeholder image to use

    Returns:
        List of block data dictionaries representing different configurations
    """
    return [
        # Variant 1: Alt text and a formatted caption with a link
        {
            "type": "image_caption",
            "value": {
                "image": {"image": image_id, "image_alt": "Mozillians at a community event"},
                "caption": '<p>Community members at <em>MozFest</em>. <a href="https://www.mozillafestival.org/">Learn more</a>.</p>',
            },
            "id": "image-caption-variant-1",
        },
        # Variant 2: Decorative image with no alt text and no caption
        {
            "type": "image_caption",
            "value": {
                "image": {"image": image_id, "image_alt": ""},
                "caption": "",
            },
            "id": "image-caption-variant-2",
        },
    ]


def get_image_caption_test_page() -> ArticlePage:
    """Create an ArticlePage with all image caption variants for testing.

    Returns:
        ArticlePage instance with image caption blocks in its content
    """
    variants = get_image_caption_variants(get_placeholder_image().id)
    return get_article_test_page(slug="image-caption-block-test", title="Image Caption Block Test Page", content=variants)
