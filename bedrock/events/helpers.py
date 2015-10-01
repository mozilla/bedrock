# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jingo

from . import utils


@jingo.register.function
def events_count():
    return utils.future_event_count()


@jingo.register.function
def next_event():
    return utils.next_event()


@jingo.register.function
def next_few_events(count):
    return utils.next_few_events(count)


@jingo.register.function
def current_and_future_events():
    return utils.current_and_future_events()


@jingo.register.function
def future_events():
    return utils.future_events()
