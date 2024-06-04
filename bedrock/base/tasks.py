# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"Helpers to abstract background task processing via django_rq"

import logging

from django.conf import settings

import django_rq

logger = logging.getLogger(__name__)


def defer_task(func, *, queue_name="default", func_args=None, func_kwargs=None):
    # Note that the * means queue_name, func_args and func_kwargs MUST be passed
    # as keywords

    # Avoid mutable default problem
    func_args = func_args or []
    func_kwargs = func_kwargs or {}

    if settings.TASK_QUEUE_AVAILABLE:
        logger.info(f"Sending {func} to the task queue '{queue_name}'")
        queue = django_rq.get_queue(queue_name)
        queue.enqueue(func, *func_args, **func_kwargs)
    else:
        logger.info(f"Task queue '{queue_name}' not available. Immediately executing {func}")
        func(*func_args, **func_kwargs)
