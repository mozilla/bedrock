# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.test import TestCase

from bedrock.cms.models.images import BedrockImage


class BedrockImageTestCase(TestCase):
    def test_pre_generate_expected_renditions(self):
        image = BedrockImage(width=1, height=1)
        filter_specs = [
            "width-2400",
            "width-2200",
            "width-2000",
            "width-1800",
            "width-1600",
            "width-1400",
            "width-1200",
            "width-1000",
            "width-800",
            "width-600",
            "width-400",
            "width-200",
            "width-100",
        ]

        with patch.object(image, "get_renditions") as get_renditions_mock:
            image._pre_generate_expected_renditions()
            get_renditions_mock.assert_called_once_with(*filter_specs)

    def test_pre_generate_expected_renditions_called_on_save(self):
        image = BedrockImage(width=1, height=1)
        with patch.object(image, "_pre_generate_expected_renditions") as pre_generate_mock:
            image.save()
            pre_generate_mock.assert_called_once_with()
