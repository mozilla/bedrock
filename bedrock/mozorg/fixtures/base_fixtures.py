# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from io import BytesIO

from django.core.files.base import ContentFile

from PIL import Image
from wagtail.models import Site

from bedrock.cms.models import BedrockImage, StructuralPage


def get_placeholder_image(width=1400, height=700, color=(117, 79, 224)):
    """Create a placeholder image for testing.

    Args:
        width: Image width in pixels (default 1400 for 2:1 ratio)
        height: Image height in pixels (default 700 for 2:1 ratio)
        color: RGB tuple for fill color

    Returns:
        BedrockImage instance
    """
    image = Image.new("RGB", (width, height), color)
    image_buffer = BytesIO()
    image.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    bedrock_image, _ = BedrockImage.objects.get_or_create(
        title="Placeholder Image for Testing",
        defaults={
            "file": ContentFile(image_buffer.read(), "placeholder_image.png"),
        },
    )
    return bedrock_image


def get_test_index_page():
    """Get or create a test index page for block tests.

    Returns:
        StructuralPage instance to use as parent for test pages
    """
    site = Site.objects.get(is_default_site=True)
    root_page = site.root_page

    index_page = StructuralPage.objects.filter(slug="block-tests-index").first()
    if not index_page:
        index_page = StructuralPage(
            slug="block-tests-index",
            title="Block Tests Index Page",
        )
        root_page.add_child(instance=index_page)
        index_page.save_revision().publish()

    return index_page
