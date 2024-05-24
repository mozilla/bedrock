# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models

from wagtail.images.models import AbstractImage, AbstractRendition, Image


class BedrockImage(AbstractImage):
    """
    Custom image model from which we can hang extra methods.

    While the docs show how we can add extra fields on this model
    (https://docs.wagtail.org/en/stable/advanced_topics/images/custom_image_model.html)
    we should NOT add caption or alt-text fields here, because that makes them
    per-image, not per-use-case. Instead, the blocks/pages where we use the image
    should have fields for such things.
    """

    admin_form_fields = Image.admin_form_fields


class BedrockRendition(AbstractRendition):
    image = models.ForeignKey(
        BedrockImage,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
