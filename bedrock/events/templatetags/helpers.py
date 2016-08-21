# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django_jinja import library

from .. import utils


@library.global_function
def events_count():
    return utils.future_event_count()


@library.global_function
def next_event():
    return utils.next_event()


@library.global_function
def next_few_events(count):
    return utils.next_few_events(count)


@library.global_function
def current_and_future_events():
    return utils.current_and_future_events()


@library.global_function
def future_events():
    return utils.future_events()
