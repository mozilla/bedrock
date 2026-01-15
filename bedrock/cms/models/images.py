# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models

from wagtail.images.models import AbstractImage, AbstractRendition, Image

from bedrock.base.tasks import defer_task

AUTOMATIC_RENDITION_FILTER_SPECS = [
    # Generate agreed step sizes:
    f"width-{size}"
    for size in range(2400, 0, -200)
] + [
    # Add agreed smallest size
    "width-100",
    # Add the size that the Wagtail Image Library uses for its listing page - we make sure we
    # regenerate it, if needed, so that the image library is updated locally after
    # downloading images from Dev, Stage or Prod
    "max-165x165",
    # 2:1 aspect ratio renditions for homepage donate block (and similar uses)
    "fill-400x200",
    "fill-600x300",
    "fill-800x400",
    "fill-1000x500",
    "fill-1200x600",
    "fill-1400x700",
]


def _make_renditions(image_id, filter_specs):
    image = BedrockImage.objects.get(id=image_id)
    image.get_renditions(*filter_specs)


class BedrockImage(AbstractImage):
    """
    Custom image model from which we can hang extra methods, such as the one that
    pre-generates custom renditions for the image.

    While the docs show how we can add extra fields on this model
    (https://docs.wagtail.org/en/stable/advanced_topics/images/custom_image_model.html)
    we should NOT add caption or alt-text fields here, because that makes them
    per-image, not per-use-case. Instead, the blocks/pages where we use the image
    should have fields for such things.
    """

    admin_form_fields = Image.admin_form_fields

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._pre_generate_expected_renditions()

    def _pre_generate_expected_renditions(self):
        """We can't make renditions on the fly in production because the
        public deployment will not have write access to the DB or storage.

        To cope with this, we pre-generate the expected renditions for each image.
        The simple algorithm is:

        * For every step from 2400px wide down to 200px wide, generate a rendition
          with that width, plus a rendition that's 100px wide

        And then, in template markup, we'll ensure that developers ONLY use rendtions
        that are width-2400, width-2200, width-2000... width-100px

        Note that Wagtail does NOT upsize an image, but it will still create an
        image as large as it can, in the same aspect ratio. So if the image
        uploaded is 1600px wide, the renditions for 2400px, 2000px.... 1600px will
        all be 1600px wide. Yes, this is wasteful, but it's the price we pay for
        having to pre-generate renditions that match a certain set of possible
        sizes we'll be expecting in template markup.
        """

        # If a background worker queue is available, this call will use it
        # to generate renditions, else it will immediately generate them
        defer_task(
            _make_renditions,
            queue_name="image_renditions",
            func_kwargs={
                "image_id": self.id,
                "filter_specs": AUTOMATIC_RENDITION_FILTER_SPECS,
            },
        )


class BedrockRendition(AbstractRendition):
    image = models.ForeignKey(
        BedrockImage,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
