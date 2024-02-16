# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Tuple
from unittest import mock

from django.conf import settings
from django.test import override_settings

import pytest

from bedrock.contentful.constants import (
    ACTION_ARCHIVE,
    ACTION_AUTO_SAVE,
    ACTION_CREATE,
    ACTION_DELETE,
    ACTION_PUBLISH,
    ACTION_SAVE,
    ACTION_UNARCHIVE,
    ACTION_UNPUBLISH,
    CONTENT_TYPE_CONNECT_HOMEPAGE,
    CONTENT_TYPE_PAGE_RESOURCE_CENTER,
)
from bedrock.contentful.management.commands.update_contentful import (
    MAX_MESSAGES_PER_QUEUE_POLL,
    Command as UpdateContentfulCommand,
)
from bedrock.contentful.models import ContentfulEntry
from bedrock.contentful.tests.data import resource_center_page_data


@pytest.fixture
def command_instance():
    command = UpdateContentfulCommand()
    command.quiet = False
    command.log = mock.Mock(name="log")
    return command


@pytest.mark.parametrize(
    "space_id, space_key, run_expected",
    (
        ("", "a_key", False),
        ("an_id", "", False),
        ("an_id", "a_key", True),
    ),
)
def test_handle__no_contentful_configuration_results_in_pass_but_no_exception(
    space_id,
    space_key,
    run_expected,
    command_instance,
):
    # If Contentful is not set up, we should just return gracefully, not blow up
    with mock.patch("builtins.print") as mock_print:
        with override_settings(
            CONTENTFUL_SPACE_ID=space_id,
            CONTENTFUL_SPACE_KEY=space_key,
        ):
            command_instance.refresh = mock.Mock(
                name="mock_refresh",
                return_value=(True, 0, 0, 0, 0),
            )
            command_instance.handle(quiet=True, force=False)

            if run_expected:
                command_instance.refresh.assert_called_once()
            else:
                command_instance.refresh.assert_not_called()
                mock_print.assert_called_once_with("Contentful credentials not configured")


@override_settings(CONTENTFUL_SPACE_ID="space_id", CONTENTFUL_SPACE_KEY="space_key")
def test_handle__message_logging__forced__and__successful(command_instance):
    command_instance.refresh = mock.Mock(
        name="mock_refresh",
        return_value=(True, 1, 2, 3, 4),
    )
    command_instance.handle(quiet=False, force=True)
    assert command_instance.log.call_count == 2
    command_instance.log.call_args_list[0][0] == ("Running forced update from Contentful data",)
    assert command_instance.log.call_args_list[1][0] == ("Done. Added: 1. Updated: 2. Deleted: 3. Errors: 4",)


@override_settings(CONTENTFUL_SPACE_ID="space_id", CONTENTFUL_SPACE_KEY="space_key")
def test_handle__message_logging__not_forced__and__nothing_changed(command_instance):
    command_instance.refresh = mock.Mock(
        name="mock_refresh",
        return_value=(False, 0, 0, 0, 0),
    )
    command_instance.handle(quiet=False, force=True)
    assert command_instance.log.call_count == 2
    command_instance.log.call_args_list[0][0] == ("Checking for updated Contentful data",)
    assert command_instance.log.call_args_list[1][0] == ("Nothing to pull from Contentful",)


@pytest.mark.parametrize(
    "param,expected",
    (
        (
            "ContentManagement.Entry.create,123abcdef123abcdef,abcdefabcdefabcdef",
            ACTION_CREATE,
        ),
        (
            "ContentManagement.Entry.publish,123abcdef123abcdef,abcdefabcdefabcdef",
            ACTION_PUBLISH,
        ),
        (
            "ContentManagement.Entry.unpublish,123abcdef123abcdef,abcdefabcdefabcdef",
            ACTION_UNPUBLISH,
        ),
        (
            "ContentManagement.Entry.archive,123abcdef123abcdef,abcdefabcdefabcdef",
            ACTION_ARCHIVE,
        ),
        (
            "ContentManagement.Entry.unarchive,123abcdef123abcdef,abcdefabcdefabcdef",
            ACTION_UNARCHIVE,
        ),
        (
            "ContentManagement.Entry.save,123abcdef123abcdef,abcdefabcdefabcdef",
            ACTION_SAVE,
        ),
        (
            "ContentManagement.Entry.auto_save,123abcdef123abcdef,abcdefabcdefabcdef",
            ACTION_AUTO_SAVE,
        ),
        (
            "ContentManagement.Entry.delete,123abcdef123abcdef,abcdefabcdefabcdef",
            ACTION_DELETE,
        ),
        (
            "ContentManagement.Entry,123abcdef123abcdef,abcdefabcdefabcdef",
            None,
        ),
        (
            "ContentManagement,123abcdef123abcdef,abcdefabcdefabcdef",
            None,
        ),
        (
            "abcdefabcdefabcdef",
            None,
        ),
        (
            "",
            None,
        ),
        (
            None,
            None,
        ),
    ),
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.capture_exception")
def test_update_contentful__get_message_action(
    mock_capture_exception,
    param,
    expected,
    command_instance,
):
    assert command_instance._get_message_action(param) == expected

    if expected is None:
        assert mock_capture_exception.call_count == 1


def test_update_contentful__purge_queue(command_instance):
    mock_queue = mock.Mock(name="mock-queue")
    command_instance._purge_queue(mock_queue)
    assert mock_queue.purge.call_count == 1


def _build_mock_messages(actions: List) -> List[List]:
    messages = []
    for i, action in enumerate(actions):
        msg = mock.Mock(name=f"msg-{i}-{action}")
        msg.body = f"ContentManagement.Entry.{action},123abc,123abc"
        messages.append(msg)

    # Split the messages into sublists, if need be
    batched_messages = []
    for idx in range(0, len(messages), MAX_MESSAGES_PER_QUEUE_POLL):
        offset = idx + MAX_MESSAGES_PER_QUEUE_POLL
        batched_messages.append(messages[idx:offset])
    return batched_messages


def _establish_mock_queue(batched_messages: List[List]) -> Tuple[mock.Mock, mock.Mock]:
    mock_queue = mock.Mock(name="mock_queue")

    def _receive_messages(*args, **kwargs):
        # Doing it this way to avoid side_effect raising StopIteration when the batch is exhausted
        if batched_messages:
            return batched_messages.pop(0)
        return []

    mock_queue.receive_messages = _receive_messages

    mock_sqs = mock.Mock(name="mock_sqs")
    mock_sqs.Queue.return_value = mock_queue
    return (mock_sqs, mock_queue)


@override_settings(
    CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID="dummy",
    APP_NAME="bedrock-dev",
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.boto3")
@pytest.mark.parametrize(
    "message_actions_sequence",
    (
        # In Dev mode, all Contentful actions apart from `create` are ones which
        # should trigger polling the queue
        [ACTION_AUTO_SAVE],
        [ACTION_SAVE],
        [ACTION_ARCHIVE],
        [ACTION_UNARCHIVE],
        [ACTION_PUBLISH],
        [ACTION_UNPUBLISH],
        [ACTION_DELETE],
        [ACTION_DELETE, ACTION_AUTO_SAVE, ACTION_PUBLISH],
        ["dummy_for_test", ACTION_AUTO_SAVE, "dummy_for_test"],
        ["dummy_for_test", "dummy_for_test", ACTION_PUBLISH],
        [ACTION_PUBLISH, "dummy_for_test", "dummy_for_test"],
    ),
    ids=[
        "single auto-save message",
        "single save message",
        "single archive message",
        "single unarchive message",
        "single publish message",
        "single unpublish message",
        "single delete message",
        "multiple messages, all are triggers",
        "multiple messages with fake extra non-trigger states, go-signal is in middle",
        "multiple messages with fake extra non-trigger states, go-signal is last",
        "multiple messages with fake extra non-trigger states, go-signal is first",
    ],
)
def test_update_contentful__queue_has_viable_messages__viable_message_found__dev_mode(
    mock_boto_3,
    message_actions_sequence,
    command_instance,
):
    messages_for_queue = _build_mock_messages(message_actions_sequence)
    mock_sqs, mock_queue = _establish_mock_queue(messages_for_queue)

    mock_boto_3.resource.return_value = mock_sqs

    assert command_instance._queue_has_viable_messages() is True
    mock_queue.purge.assert_called_once()


@override_settings(
    CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID="dummy",
    APP_NAME="bedrock-prod",
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.boto3")
@pytest.mark.parametrize(
    "message_actions_sequence",
    (
        # One message in the queue
        [ACTION_PUBLISH],
        [ACTION_UNPUBLISH],
        [ACTION_ARCHIVE],
        [ACTION_UNARCHIVE],
        [ACTION_DELETE],
        # Multiple messages in the queue
        [ACTION_AUTO_SAVE, ACTION_DELETE, ACTION_AUTO_SAVE],
        [ACTION_SAVE, ACTION_AUTO_SAVE, ACTION_PUBLISH],
        [ACTION_ARCHIVE, ACTION_AUTO_SAVE, ACTION_AUTO_SAVE],
        [ACTION_ARCHIVE, ACTION_PUBLISH, ACTION_DELETE, ACTION_UNPUBLISH, ACTION_UNARCHIVE],
    ),
    ids=[
        "single publish message",
        "single unpublish message",
        "single archive message",
        "single unarchive message",
        "single delete message",
        "multiple messages, go-signal is in middle",
        "multiple messages, go-signal is last",
        "multiple messages, go-signal is first",
        "multiple messages, all are go-signals",
    ],
)
def test_update_contentful__queue_has_viable_messages__viable_message_found__prod_mode(
    mock_boto_3,
    message_actions_sequence,
    command_instance,
):
    messages_for_queue = _build_mock_messages(message_actions_sequence)
    mock_sqs, mock_queue = _establish_mock_queue(messages_for_queue)

    mock_boto_3.resource.return_value = mock_sqs

    assert command_instance._queue_has_viable_messages() is True
    mock_queue.purge.assert_called_once()


@override_settings(
    CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID="dummy",
    APP_NAME="bedrock-dev",
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.boto3")
@pytest.mark.parametrize(
    "message_actions_sequence",
    (
        # One message in the queue
        [ACTION_CREATE],
        # Multiple messages in the queue
        [ACTION_CREATE, ACTION_CREATE, ACTION_CREATE],
    ),
    ids=[
        "single create message",
        "multiple create messages",
    ],
)
def test_update_contentful__queue_has_viable_messages__no_viable_message_found__dev_mode(
    mock_boto_3,
    message_actions_sequence,
    command_instance,
):
    # Create is the only message that will not trigger a Contentful poll in Dev
    assert settings.APP_NAME == "bedrock-dev"
    messages_for_queue = _build_mock_messages(message_actions_sequence)
    mock_sqs, mock_queue = _establish_mock_queue(messages_for_queue)

    mock_boto_3.resource.return_value = mock_sqs

    assert command_instance._queue_has_viable_messages() is False
    mock_queue.purge.assert_not_called()


@override_settings(
    CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID="dummy",
    APP_NAME="bedrock-prod",
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.boto3")
@pytest.mark.parametrize(
    "message_actions_sequence",
    (
        # One message in the queue
        [ACTION_SAVE],
        [ACTION_AUTO_SAVE],
        [ACTION_CREATE],
        # Multiple messages in the queue
        [ACTION_AUTO_SAVE, ACTION_SAVE, ACTION_CREATE],
    ),
    ids=[
        "single save message",
        "single auto-save message",
        "single create message",
        "multiple messages",
    ],
)
def test_update_contentful__queue_has_viable_messages__no_viable_message_found__prod_mode(
    mock_boto_3,
    message_actions_sequence,
    command_instance,
):
    # In prod mode we don't want creation or draft editing to trigger a
    # re-poll of the API because it's unnecessary.
    assert settings.APP_NAME == "bedrock-prod"
    messages_for_queue = _build_mock_messages(message_actions_sequence)
    mock_sqs, mock_queue = _establish_mock_queue(messages_for_queue)

    mock_boto_3.resource.return_value = mock_sqs

    assert command_instance._queue_has_viable_messages() is False
    mock_queue.purge.assert_not_called()


@pytest.mark.parametrize("unconfigured_value", ("", None))
def test_queue_has_viable_messages__no_sqs_configured(
    unconfigured_value,
    command_instance,
):
    # If SQS is not set up, we should just poll as if --force was used
    with override_settings(
        CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID=unconfigured_value,
    ):
        assert settings.CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID == unconfigured_value
        assert command_instance._queue_has_viable_messages() is True


@override_settings(
    CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID="dummy",
    APP_NAME="bedrock-dev",
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.boto3")
@pytest.mark.parametrize(
    "message_actions_sequence",
    (
        [ACTION_CREATE] * 10 + [ACTION_PUBLISH],
        [ACTION_CREATE] * 9 + [ACTION_PUBLISH],
        [ACTION_CREATE] * 8 + [ACTION_PUBLISH],
        [ACTION_CREATE] * 56 + [ACTION_PUBLISH],
    ),
    ids=[
        "Eleven messages",
        "Ten messages",
        "Nine messages",
        "57 messages",
    ],
)
def test_update_contentful__iteration_through_message_batch_thresholds(
    mock_boto_3,
    message_actions_sequence,
    command_instance,
):
    # ie, show we handle less and more than 10 messages in the queue.
    # Only the last message in each test case is viable, because
    # ACTION_CREATE should NOT trigger anything in Dev, Stage or Prod
    messages_for_queue = _build_mock_messages(message_actions_sequence)
    mock_sqs, mock_queue = _establish_mock_queue(messages_for_queue)

    mock_boto_3.resource.return_value = mock_sqs

    assert command_instance._queue_has_viable_messages() is True
    mock_queue.purge.assert_called_once()


@override_settings(
    CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID="dummy",
    APP_NAME="bedrock-dev",
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.boto3")
def test_update_contentful__queue_has_viable_messages__no_messages(
    mock_boto_3,
    command_instance,
):
    messages_for_queue = _build_mock_messages([])
    mock_sqs, mock_queue = _establish_mock_queue(messages_for_queue)

    mock_boto_3.resource.return_value = mock_sqs

    assert command_instance._queue_has_viable_messages() is False
    mock_queue.purge.assert_not_called()


@pytest.mark.parametrize(
    "must_force,has_viable_messages,expected",
    (
        (False, False, (False, -1, -1, -1, -1)),
        (True, False, (True, 3, 2, 1, 0)),
        (False, True, (True, 3, 2, 1, 0)),
    ),
    ids=(
        "Not forced, no viable messages in queue",
        "Forced, no viable messages in queue",
        "Not forced, queue has viable messages",
    ),
)
def test_update_contentful__refresh(
    must_force,
    has_viable_messages,
    expected,
    command_instance,
):
    command_instance._queue_has_viable_messages = mock.Mock(
        name="_queue_has_viable_messages",
        return_value=has_viable_messages,
    )

    command_instance._refresh_from_contentful = mock.Mock(
        name="_refresh_from_contentful",
        return_value=(
            3,  # 'added'
            2,  # 'updated'
            1,  # 'deleted'
            0,  # 'errors'
        ),
    )

    command_instance.force = must_force

    retval = command_instance.refresh()
    assert retval == expected


def _build_mock_entries(mock_entry_data: List[dict]) -> List[mock.Mock]:
    output = []
    for datum_dict in mock_entry_data:
        mock_entry = mock.Mock()
        for attr, val in datum_dict.items():
            setattr(mock_entry, attr, val)

        output.append(mock_entry)
    return output


@override_settings(CONTENTFUL_CONTENT_TYPES_TO_SYNC=["type_one", "type_two"])
@mock.patch("bedrock.contentful.management.commands.update_contentful.ContentfulPage")
def test_update_contentful__get_content_to_sync(
    mock_contentful_page,
    command_instance,
):
    mock_en_us_locale = mock.Mock()
    mock_en_us_locale.code = "en-US"
    mock_de_locale = mock.Mock()
    mock_de_locale.code = "de"

    available_locales = [
        mock_en_us_locale,
        mock_de_locale,
    ]

    _first_batch = _build_mock_entries(
        [
            {"sys": {"id": "one"}},
            {"sys": {"id": "two"}},
            {"sys": {"id": "three"}},
            {"sys": {"id": "four"}},
        ],
    )

    _second_batch = _build_mock_entries(
        [
            {"sys": {"id": "1"}},
            {"sys": {"id": "2"}},
            {"sys": {"id": "3"}},
            {"sys": {"id": "4"}},
        ],
    )

    _third_batch = _build_mock_entries(
        # These will not be used/requested
        [
            {"sys": {"id": "X"}},
            {"sys": {"id": "Y"}},
            {"sys": {"id": "Z"}},
        ],
    )

    mock_retval_1 = mock.Mock()
    mock_retval_1.items = _first_batch
    mock_retval_2 = mock.Mock()
    mock_retval_2.items = _second_batch
    mock_retval_3 = mock.Mock()
    mock_retval_3.items = _first_batch
    mock_retval_4 = mock.Mock()
    mock_retval_4.items = _second_batch
    mock_retval_5 = mock.Mock()
    mock_retval_5.items = _third_batch

    mock_contentful_page.client.entries.side_effect = [
        mock_retval_1,
        mock_retval_2,
        mock_retval_3,
        mock_retval_4,
        mock_retval_5,  # will not be called for
    ]

    output = command_instance._get_content_to_sync(available_locales)

    assert output == [
        ("type_one", "one", "en-US"),
        ("type_one", "two", "en-US"),
        ("type_one", "three", "en-US"),
        ("type_one", "four", "en-US"),
        ("type_two", "1", "en-US"),
        ("type_two", "2", "en-US"),
        ("type_two", "3", "en-US"),
        ("type_two", "4", "en-US"),
        ("type_one", "one", "de"),
        ("type_one", "two", "de"),
        ("type_one", "three", "de"),
        ("type_one", "four", "de"),
        ("type_two", "1", "de"),
        ("type_two", "2", "de"),
        ("type_two", "3", "de"),
        ("type_two", "4", "de"),
        # and deliberately nothing from the third batch
    ]

    assert mock_contentful_page.client.entries.call_count == 4

    assert mock_contentful_page.client.entries.call_args_list[0][0] == (
        {
            "content_type": "type_one",
            "include": 0,
            "locale": "en-US",
        },
    )
    assert mock_contentful_page.client.entries.call_args_list[1][0] == (
        {
            "content_type": "type_two",
            "include": 0,
            "locale": "en-US",
        },
    )
    assert mock_contentful_page.client.entries.call_args_list[2][0] == (
        {
            "content_type": "type_one",
            "include": 0,
            "locale": "de",
        },
    )
    assert mock_contentful_page.client.entries.call_args_list[3][0] == (
        {
            "content_type": "type_two",
            "include": 0,
            "locale": "de",
        },
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "total_to_create_per_locale, locales_to_use, entries_processed_in_sync, expected_deletion_count",
    (
        (
            3,
            ["en-US"],
            [
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "en-US"),
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "en-US"),
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "en-US"),
            ],
            0,
        ),
        (
            3,
            ["en-US"],
            [
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "en-US"),
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "en-US"),
            ],
            1,
        ),
        (
            5,
            ["en-US"],
            [
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "en-US"),
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "en-US"),
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_4", "en-US"),
            ],
            2,
        ),
        (
            3,
            ["en-US"],
            [],
            3,
        ),
        (
            3,
            ["en-US", "de", "fr", "it"],
            [
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "en-US"),
                # (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "de"),  # simulating deletion/absence from sync
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "fr"),
                # (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "it"),
                # (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "en-US"),
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "de"),
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "fr"),
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "it"),
                (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "en-US"),
                # (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "de"),
                # (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "fr"),
                # (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "it"),
            ],
            6,
        ),
    ),
    ids=[
        "All ids attempted, so none deleted",
        "First two ids attempted, so one deleted",
        "Middle three of five ids attempted,, so two deleted",
        "No ids attempted, so all deleted",
        "Pages remain but some locales zapped, reducing entries",
    ],
)
def test_update_contentful__detect_and_delete_absent_entries(
    total_to_create_per_locale,
    locales_to_use,
    entries_processed_in_sync,
    expected_deletion_count,
    command_instance,
):
    for locale in locales_to_use:
        for idx in range(total_to_create_per_locale):
            ContentfulEntry.objects.create(
                content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
                contentful_id=f"entry_{idx+1}",
                locale=locale,
            )

    retval = command_instance._detect_and_delete_absent_entries(entries_processed_in_sync)
    assert retval == expected_deletion_count


@pytest.mark.django_db
def test_update_contentful__detect_and_delete_absent_entries__homepage_involved(command_instance):
    # Make two homepages, with en-US locales (because that's how it rolls for now)
    ContentfulEntry.objects.create(
        content_type=CONTENT_TYPE_CONNECT_HOMEPAGE,
        contentful_id="home_1",
        locale="en-US",
    )
    ContentfulEntry.objects.create(
        content_type=CONTENT_TYPE_CONNECT_HOMEPAGE,
        contentful_id="home_2",
        locale="en-US",
    )

    # Make some other pages
    for locale in ["en-US", "fr", "it"]:
        for idx in range(3):
            ContentfulEntry.objects.create(
                content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
                contentful_id=f"entry_{idx+1}",
                locale=locale,
            )

    # Let's pretend the second homepage and some others have been deleted
    entries_processed_in_sync = [
        (CONTENT_TYPE_CONNECT_HOMEPAGE, "home_1", "en-US"),
        # (CONTENT_TYPE_CONNECT_HOMEPAGE, "home_2", "en-US"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "en-US"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "fr"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "it"),
        # (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "en-US"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "fr"),
        # (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "it"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "en-US"),
        # (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "fr"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "it"),
    ]
    retval = command_instance._detect_and_delete_absent_entries(entries_processed_in_sync)
    assert retval == 4

    for ctype, contentful_id, locale in [
        (CONTENT_TYPE_CONNECT_HOMEPAGE, "home_1", "en-US"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "en-US"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "fr"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_1", "it"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "fr"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "en-US"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "it"),
    ]:
        assert ContentfulEntry.objects.get(
            content_type=ctype,
            contentful_id=contentful_id,
            locale=locale,
        )

    for ctype, contentful_id, locale in [
        (CONTENT_TYPE_CONNECT_HOMEPAGE, "home_2", "en-US"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "en-US"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_2", "it"),
        (CONTENT_TYPE_PAGE_RESOURCE_CENTER, "entry_3", "fr"),
    ]:
        assert not ContentfulEntry.objects.filter(
            content_type=ctype,
            contentful_id=contentful_id,
            locale=locale,
        ).exists()


def test_log():
    command_instance = UpdateContentfulCommand()
    command_instance.quiet = False
    with mock.patch("builtins.print") as mock_print:
        command_instance.log("This SHALL be printed")
    mock_print.assert_called_once_with("This SHALL be printed")

    mock_print.reset_mock()

    command_instance.quiet = True
    with mock.patch("builtins.print") as mock_print:
        command_instance.log("This shall not be printed")
    assert not mock_print.called


_dummy_completeness_spec = {
    "test-content-type": [
        # just three of anything, as it's not acted upon in this test
        {
            "type": list,
            "key": "fake1",
        },
        {
            "type": dict,
            "key": "fake2",
        },
        {
            "type": list,
            "key": "fake3",
        },
    ]
}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "mock_localised_values, expected_completion_flag",
    (
        (["one", "two", "three"], True),
        (["", "", ""], False),
        (["one", None, ""], False),
    ),
)
def test_update_contentful__check_localisation_complete(
    mock_localised_values,
    expected_completion_flag,
    command_instance,
):
    entry = ContentfulEntry.objects.create(
        content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
        contentful_id="test_1",
        locale="en-US",
    )
    assert entry.localisation_complete is False

    command_instance._get_value_from_data = mock.Mock(side_effect=mock_localised_values)
    command_instance._check_localisation_complete()

    entry.refresh_from_db()
    assert entry.localisation_complete == expected_completion_flag


@pytest.mark.parametrize(
    "spec, expected_string",
    (
        (".entries[].body", "Virtual private networks (VPNs) and secure web proxies are solutions "),
        (
            ".info.seo.description",
            "VPNs and proxies are solutions for online privacy and security. Here’s how these protect you and how to choose the best option.",
        ),
        (
            ".info.seo.image",
            "https://images.ctfassets.net/w5er3c7zdgmd/7o6QXGC6BXMq3aB5hu4mmn/d0dc31407051937f56a0a46767e11f6f/vpn-16x9-phoneglobe.png",
        ),
    ),
)
def test_update_contentful__get_value_from_data(spec, expected_string, command_instance):
    assert expected_string in command_instance._get_value_from_data(
        resource_center_page_data,
        spec,
    )


@pytest.mark.parametrize(
    "jq_all_mocked_output, expected",
    (
        (["   ", "", None], ""),
        ([" Hello, World!  ", "test", None], "Hello, World! test"),
    ),
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.jq.all")
def test__get_value_from_data__no_false_positives(
    mocked_jq_all,
    jq_all_mocked_output,
    expected,
    command_instance,
):
    mocked_jq_all.return_value = jq_all_mocked_output
    assert command_instance._get_value_from_data(data=None, spec=None) == expected
