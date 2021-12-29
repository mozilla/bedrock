# -*- coding: utf-8 -*-
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
)
from bedrock.contentful.management.commands.update_contentful import (
    MAX_MESSAGES_PER_QUEUE_POLL,
    Command as UpdateContentfulCommand,
)
from bedrock.contentful.models import ContentfulEntry


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
    # Create is the only message that will not trigger a contenful poll in Dev
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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "total_to_create, contentful_ids_synced, expected_deletion_count",
    (
        (3, ["entry_1", "entry_2", "entry_3"], 0),
        (3, ["entry_1", "entry_2"], 1),
        (5, ["entry_2", "entry_3", "entry_4"], 2),
        (3, [], 3),
    ),
    ids=[
        "All ids attempted, so none deleted",
        "First two ids attempted, so one deleted",
        "Middle three of five ids attempted,, so two deleted",
        "No ids attempted, so all deleted",
    ],
)
def test_update_contentful__detect_and_delete_absent_entries(
    total_to_create,
    contentful_ids_synced,
    expected_deletion_count,
    command_instance,
):
    for idx in range(total_to_create):
        ContentfulEntry.objects.create(contentful_id=f"entry_{idx+1}")

    retval = command_instance._detect_and_delete_absent_entries(contentful_ids_synced)
    assert retval == expected_deletion_count
