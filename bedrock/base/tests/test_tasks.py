# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings

from bedrock.base import tasks


class TasksHelperTests(TestCase):
    @override_settings(TASK_QUEUE_AVAILABLE=True)
    @patch("bedrock.base.tasks.django_rq.get_queue")
    def test_defer_task_with_task_queue_available(self, mock_get_queue):
        mock_queue = MagicMock()
        mock_get_queue.return_value = mock_queue

        func = MagicMock()
        func_args = [1, 2, 3]
        func_kwargs = {"a": "foo", "b": "bar"}

        tasks.defer_task(
            func,
            queue_name="custom_queue_name",
            func_args=func_args,
            func_kwargs=func_kwargs,
        )

        mock_get_queue.assert_called_once_with("custom_queue_name")
        mock_queue.enqueue.assert_called_once_with(func, *func_args, **func_kwargs)
        func.assert_not_called()

    @override_settings(TASK_QUEUE_AVAILABLE=True)
    @patch("bedrock.base.tasks.django_rq.get_queue")
    def test_defer_task_no_args(self, mock_get_queue):
        mock_queue = MagicMock()
        mock_get_queue.return_value = mock_queue

        func = MagicMock()
        func_kwargs = {"a": "foo", "b": "bar"}

        tasks.defer_task(
            func,
            queue_name="custom_queue_name",
            func_kwargs=func_kwargs,
        )

        expected_func_args = []

        mock_get_queue.assert_called_once_with("custom_queue_name")
        mock_queue.enqueue.assert_called_once_with(func, *expected_func_args, **func_kwargs)
        func.assert_not_called()

    @override_settings(TASK_QUEUE_AVAILABLE=True)
    @patch("bedrock.base.tasks.django_rq.get_queue")
    def test_defer_task_no_kwargs(self, mock_get_queue):
        mock_queue = MagicMock()
        mock_get_queue.return_value = mock_queue

        func = MagicMock()
        func_args = [1, 2, 3]

        tasks.defer_task(
            func,
            queue_name="custom_queue_name",
            func_args=func_args,
        )

        expected_func_kwargs = {}

        mock_get_queue.assert_called_once_with("custom_queue_name")
        mock_queue.enqueue.assert_called_once_with(func, *func_args, **expected_func_kwargs)
        func.assert_not_called()

    @override_settings(TASK_QUEUE_AVAILABLE=True)
    @patch("bedrock.base.tasks.django_rq.get_queue")
    def test_defer_task_with_task_queue_available__default_queue_name(self, mock_get_queue):
        mock_queue = MagicMock()
        mock_get_queue.return_value = mock_queue

        func = MagicMock()
        func_args = [1, 2, 3]
        func_kwargs = {"a": "foo", "b": "bar"}

        tasks.defer_task(
            func,
            func_args=func_args,
            func_kwargs=func_kwargs,
        )

        mock_get_queue.assert_called_once_with("default")
        mock_queue.enqueue.assert_called_once_with(func, *func_args, **func_kwargs)
        func.assert_not_called()

    @override_settings(TASK_QUEUE_AVAILABLE=False)
    @patch("bedrock.base.tasks.django_rq.get_queue")
    def test_defer_task_with_task_queue_not_available(self, mock_get_queue):
        func = MagicMock()
        func_args = [1, 2, 3]
        func_kwargs = {"a": "foo", "b": "bar"}

        tasks.defer_task(
            func,
            queue_name="custom_queue_name",
            func_args=func_args,
            func_kwargs=func_kwargs,
        )

        mock_get_queue.assert_not_called()
        func.assert_called_once_with(*func_args, **func_kwargs)
