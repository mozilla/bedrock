# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import Mock, patch

from django.core.management.base import BaseCommand

from bedrock.utils.management.decorators import alert_sentry_on_exception


@alert_sentry_on_exception
class _TestCommandWithException(BaseCommand):
    def handle(self, *args, **options):
        raise Exception("This is a test")


class _TestCommandWithoutException(BaseCommand):
    def foo(self):
        # just for mocking in tests
        pass

    def handle(self, *args, **options):
        self.foo()


@patch("bedrock.utils.management.decorators.capture_exception")
def test_sentry_alerting_base_command__exception_raised(mock_capture_exception):
    assert not mock_capture_exception.called

    try:
        _TestCommandWithException().handle()
        assert False, "Expected an exception to have been raised"
    except Exception as ex:
        # The same exception raised should have been passed to Sentry
        mock_capture_exception.assert_called_once_with(ex)


@patch("bedrock.utils.management.decorators.capture_exception")
def test_sentry_alerting_base_command__no_exception_raised(mock_capture_exception):
    assert not mock_capture_exception.called

    command = _TestCommandWithoutException()
    command.foo = Mock()
    command.handle()

    assert not mock_capture_exception.called
    assert command.foo.call_count == 1
