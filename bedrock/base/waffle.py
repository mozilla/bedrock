# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

from waffle import switch_is_active


def switch(name):
    """
    A wrapper around django-waffle's `switch_is_active`.

    It will take whatever name you pass to it (must be only numbers, letters, and dashes), convert
    it to uppercase, convert dashes to underscores, then call waffle's `switch_is_active`.

    * When DEV=True
        - When switch doesn't exist -> True
        - When switch exists and is True -> True
        - When switch exists and is False -> False
    * When Dev=False
        - When switch doesn't exist -> False
        - When switch exists and is True -> True
        - When switch exists and is False -> False

    For example:

        {% if switch('dude-and-walter') %}

    would check for a waffle switch called `DUDE_AND_WALTER` and return True if active, else False.

    """
    switch_name = name.upper().replace("-", "_")
    active = switch_is_active(switch_name)
    # With `settings.WAFFLE_SWITCH_DEFAULT` set to `None`, we can test if a switch is explicitly set or not.
    # Here, active is None we know the switch doesn't exist so we default to what `settings.DEV` is.
    if active is None:
        return settings.DEV
    # Otherwise we return the defined switch value.
    return active
