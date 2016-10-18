"""
Replacement library (function really) for Waffle that uses environment variables.
"""
from django.conf import settings

from decouple import config


def switch(name):
    """A template helper that replaces waffle

    * All calls default to True when DEV setting is True.
    * If the env var is explicitly false it will be false even when DEV = True.
    * Otherwise the call is False by default and True is a specific env var exists and is truthy.

    For example:

        {% if switch('dude-and-walter') %}

    would check for an environment variable called `SWITCH_DUDE_AND_WALTER`. The string from the
    `switch()` call is converted to uppercase and dashes replaced with underscores.
    """
    env_name = 'SWITCH_' + name.upper().replace('-', '_')
    return config(env_name, default=settings.DEV, cast=bool)
