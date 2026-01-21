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
    # 2:1 aspect ratio (wide landscape)
    "fill-100x50",
    "fill-200x100",
    "fill-400x200",
    "fill-600x300",
    "fill-800x400",
    "fill-1000x500",
    "fill-1200x600",
    "fill-1400x700",
    "fill-1600x800",
    "fill-1800x900",
    "fill-2000x1000",
    "fill-2200x1100",
    "fill-2400x1200",
    # 1:1 aspect ratio (square)
    "fill-100x100",
    "fill-200x200",
    "fill-400x400",
    "fill-600x600",
    "fill-800x800",
    "fill-1000x1000",
    "fill-1200x1200",
    "fill-1400x1400",
    "fill-1600x1600",
    "fill-1800x1800",
    "fill-2000x2000",
    "fill-2200x2200",
    "fill-2400x2400",
    # 5:4 aspect ratio (landscape)
    "fill-100x80",
    "fill-200x160",
    "fill-400x320",
    "fill-600x480",
    "fill-800x640",
    "fill-1000x800",
    "fill-1200x960",
    "fill-1400x1120",
    "fill-1600x1280",
    "fill-1800x1440",
    "fill-2000x1600",
    "fill-2200x1760",
    "fill-2400x1920",
    # 22:9 aspect ratio (ultra-wide)
    "fill-100x41",
    "fill-200x82",
    "fill-400x164",
    "fill-600x245",
    "fill-800x327",
    "fill-1000x409",
    "fill-1200x491",
    "fill-1400x573",
    "fill-1600x655",
    "fill-1800x736",
    "fill-2000x818",
    "fill-2200x900",
    "fill-2400x982",
    # 4:5 aspect ratio (portrait)
    "fill-100x125",
    "fill-200x250",
    "fill-400x500",
    "fill-600x750",
    "fill-800x1000",
    "fill-1000x1250",
    "fill-1200x1500",
    "fill-1400x1750",
    "fill-1600x2000",
    "fill-1800x2250",
    "fill-2000x2500",
    "fill-2200x2750",
    "fill-2400x3000",
    # 2:3 aspect ratio (tall portrait)
    "fill-100x150",
    "fill-200x300",
    "fill-400x600",
    "fill-600x900",
    "fill-800x1200",
    "fill-1000x1500",
    "fill-1200x1800",
    "fill-1400x2100",
    "fill-1600x2400",
    "fill-1800x2700",
    "fill-2000x3000",
    "fill-2200x3300",
    "fill-2400x3600",
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
        The algorithm is:

        * For every step from 2400px wide down to 200px wide, generate a rendition
          with that width, plus a rendition that's 100px wide
        * For each supported aspect ratio (2:1, 1:1, 5:4, 22:9, 4:5, 2:3), generate
          cropped renditions at widths from 100px to 2400px (100, 200, then 400-2400 in 200px steps)

        And then, in template markup, we'll ensure that developers ONLY use renditions
        that match these pre-generated specs (e.g. width-2400, fill-1200x600).

        Note that Wagtail does NOT upsize an image, but it will still create an
        image as large as it can. So if the image uploaded is 1600px wide, the
        renditions for 2400px, 2000px.... 1600px will all be 1600px wide. Yes,
        this is wasteful, but it's the price we pay for having to pre-generate
        renditions that match a certain set of possible sizes we'll be expecting
        in template markup.
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
