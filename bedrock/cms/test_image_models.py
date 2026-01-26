# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

import pytest

from bedrock.cms.models.images import AUTOMATIC_RENDITION_FILTER_SPECS, BedrockImage, _make_renditions

pytestmark = [pytest.mark.django_db]


class BedrockImageTestCase(TestCase):
    @override_settings(TASK_QUEUE_AVAILABLE=False)
    def test_pre_generate_expected_renditions__no_queue_available(self):
        image = BedrockImage(width=1, height=1)

        with patch("bedrock.cms.models.images._make_renditions") as _make_renditions_mock:
            image._pre_generate_expected_renditions()
            _make_renditions_mock.assert_called_once_with(image_id=image.id, filter_specs=AUTOMATIC_RENDITION_FILTER_SPECS)

    @override_settings(TASK_QUEUE_AVAILABLE=True)
    def test_pre_generate_expected_renditions__queue_available(self):
        image = BedrockImage(width=1, height=1)

        with patch("bedrock.base.tasks.django_rq") as mock_django_rq:
            mock_queue = Mock(name="mocked_queue")
            mock_django_rq.get_queue.return_value = mock_queue

            image._pre_generate_expected_renditions()

            mock_django_rq.get_queue.assert_called_once_with("image_renditions")
            mock_queue.enqueue.assert_called_once_with(
                _make_renditions,
                image_id=image.id,
                filter_specs=AUTOMATIC_RENDITION_FILTER_SPECS,
            )

    def test_pre_generate_expected_renditions_uses_defer_task(self):
        image = BedrockImage(width=1, height=1)

        with patch("bedrock.cms.models.images.defer_task") as mock_defer_task:
            image._pre_generate_expected_renditions()
            mock_defer_task.assert_called_once_with(
                _make_renditions,
                queue_name="image_renditions",
                func_kwargs={
                    "image_id": image.id,
                    "filter_specs": AUTOMATIC_RENDITION_FILTER_SPECS,
                },
            )

    def test_pre_generate_expected_renditions_called_on_save(self):
        image = BedrockImage(width=1, height=1)
        with patch.object(image, "_pre_generate_expected_renditions") as pre_generate_mock:
            image.save()
            pre_generate_mock.assert_called_once_with()

    def test_bedrock_image_uses_sanitizing_field(self):
        """Verify that BedrockImage forms use SanitizingWagtailImageField."""
        from wagtail.images.forms import get_image_form

        from bedrock.cms.fields import SanitizingWagtailImageField

        ImageForm = get_image_form(BedrockImage)
        form = ImageForm()

        # Check that the 'file' field is our custom sanitizing field
        self.assertIsInstance(
            form.fields["file"],
            SanitizingWagtailImageField,
        )
