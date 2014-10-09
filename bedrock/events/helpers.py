# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jingo

from bedrock.events.models import Event


@jingo.register.function
def events_count():
    return Event.objects.future().count()


@jingo.register.function
def next_event():
    try:
        return Event.objects.future()[0]
    except IndexError:
        return None


@jingo.register.function
def next_few_events(count):
    return Event.objects.future()[:count]
