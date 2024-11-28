# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from django.test import override_settings

import pytest
from wagtail_localize.models import Translation
from wagtail_localize_smartling.models import Job
from wagtail_localize_smartling.signals import translation_imported

from bedrock.cms.signal_handlers import notify_of_imported_translation
from bedrock.cms.tests.factories import WagtailUserFactory

pytestmark = [pytest.mark.django_db]


def test_translation_imported_is_connected_to_the_expected_handler():
    assert len(translation_imported.receivers) == 1
    assert translation_imported.receivers[0][1] == notify_of_imported_translation


@override_settings(
    DEFAULT_FROM_EMAIL="from@example.com",
    WAGTAILADMIN_BASE_URL="https://cms.example.com",
)
def test_notify_of_imported_translation__happy_path(mocker, caplog):
    caplog.set_level(logging.INFO)

    WagtailUserFactory(
        username="admin_1",
        email="admin_1@example.com",
        is_superuser=True,
    )
    WagtailUserFactory(
        username="user_1",
        email="user_1@example.com",
        is_superuser=False,
    )
    WagtailUserFactory(
        username="admin_2",
        email="admin_2@example.com",
        is_superuser=True,
    )

    mock_job = mocker.MagicMock(spec=Job)
    mock_job.name = "Test Job"
    mock_job.pk = 9876
    mock_source = mocker.Mock(name="test-source")
    mock_job.translation_source.get_source_instance.return_value = mock_source

    mock_translation = mocker.MagicMock(spec=Translation, name="mock-translation")
    mock_translation.target_locale.language_code = "fr-CA"

    mock_send_mail = mocker.patch("bedrock.cms.signal_handlers.send_mail")

    translation_imported.send(
        sender=Job,
        instance=mock_job,
        translation=mock_translation,
    )
    assert mock_send_mail.call_count == 1
    assert mock_send_mail.call_args[1]["subject"] == "New translations imported into Bedrock CMS"
    assert mock_send_mail.call_args[1]["from_email"] == "from@example.com"
    assert mock_send_mail.call_args[1]["recipient_list"] == ["admin_1@example.com", "admin_2@example.com"]

    for expected_string in [
        "ACTION REQUIRED: A new translation has been synced back from Smartling",
        "It is Job 'Test Job'",
        "https://cms.example.com/cms-admin/smartling-jobs/inspect/9876/",
    ]:
        assert expected_string in mock_send_mail.call_args[1]["message"]
    assert caplog.records[0].message == "Translation-imported notification sent to 2 admins"


def test_notify_of_imported_translation__no_admins_in_system(mocker, caplog):
    caplog.set_level(logging.INFO)

    mock_job = mocker.MagicMock(spec=Job)
    mock_job.name = "Test Job"
    mock_job.pk = 9876
    mock_source = mocker.Mock(name="test-source")
    mock_job.translation_source.get_source_instance.return_value = mock_source

    mock_translation = mocker.MagicMock(spec=Translation, name="mock-translation")
    mock_translation.target_locale.language_code = "fr-CA"

    mock_send_mail = mocker.patch("bedrock.cms.signal_handlers.send_mail")

    translation_imported.send(
        sender=Job,
        instance=mock_job,
        translation=mock_translation,
    )
    assert mock_send_mail.call_count == 0
    assert caplog.records[0].message == "Unable to send translation-imported email alerts: no admins in system"
