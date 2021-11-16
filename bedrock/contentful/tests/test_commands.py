# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import List, Tuple
from unittest import mock

from django.conf import settings
from django.test import override_settings

import pytest

from bedrock.contentful.management.commands.update_contentful import (
    MAX_MESSAGES_PER_QUEUE_POLL,
    Command as UpdateContentfulCommand,
)


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
                return_value=(True, 0, 0, 0),
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
            "create",
        ),
        (
            "ContentManagement.Entry.publish,123abcdef123abcdef,abcdefabcdefabcdef",
            "publish",
        ),
        (
            "ContentManagement.Entry.unarchive,123abcdef123abcdef,abcdefabcdefabcdef",
            "unarchive",
        ),
        (
            "ContentManagement.Entry.save,123abcdef123abcdef,abcdefabcdefabcdef",
            "save",
        ),
        (
            "ContentManagement.Entry.auto_save,123abcdef123abcdef,abcdefabcdefabcdef",
            "auto_save",
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
    DEV=True,
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.boto3")
@pytest.mark.parametrize(
    "message_actions_sequence",
    (
        # One message in the queue
        ["auto_save"],
        ["create"],
        ["publish"],
        ["save"],
        ["unarchive"],
        # Multiple messages in the queue
        ["delete", "auto_save", "delete"],
        ["delete", "unpublish", "create"],
        ["publish", "unpublish", "unpublish"],
        ["publish", "publish", "publish", "publish"],
    ),
    ids=[
        "single auto-save message",
        "single create message",
        "single publish message",
        "single save message",
        "single unarchive message",
        "multiple messages, go-signal is in middle",
        "multiple messages, go-signal is last",
        "multiple messages, go-signal is first",
        "multiple messages, all are go-signals",
    ],
)
def test_update_contentful__queue_has_viable_messages__viable_message_found(
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
    DEV=True,
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.boto3")
@pytest.mark.parametrize(
    "message_actions_sequence",
    (
        # One message in the queue
        ["delete"],
        ["unpublish"],
        ["archive"],
        # Multiple messages in the queue
        ["delete", "archive", "delete"],
    ),
    ids=[
        "single delete message",
        "single unpublish message",
        "single archive message",
        "multiple messages",
    ],
)
def test_update_contentful__queue_has_viable_messages__no_viable_message_found(
    mock_boto_3,
    message_actions_sequence,
    command_instance,
):
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
    DEV=True,
)
@mock.patch("bedrock.contentful.management.commands.update_contentful.boto3")
@pytest.mark.parametrize(
    "message_actions_sequence",
    (
        ["delete"] * 10 + ["publish"],
        ["delete"] * 9 + ["publish"],
        ["delete"] * 8 + ["publish"],
        ["delete"] * 56 + ["publish"],
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
    # Only the last message in each test case is viable
    messages_for_queue = _build_mock_messages(message_actions_sequence)
    mock_sqs, mock_queue = _establish_mock_queue(messages_for_queue)

    mock_boto_3.resource.return_value = mock_sqs

    assert command_instance._queue_has_viable_messages() is True
    mock_queue.purge.assert_called_once()


@override_settings(
    CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID="dummy",
    DEV=True,
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
        (False, False, (False, -1, -1, -1)),
        (True, False, (True, 1, 2, 0)),
        (False, True, (True, 1, 2, 0)),
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
            1,  # 'added'
            2,  # 'updated'
            0,  # 'errors'
        ),
    )

    command_instance.force = must_force

    retval = command_instance.refresh()
    assert retval == expected
