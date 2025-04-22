# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import contextlib

from django.urls import reverse as django_reverse
from django.utils import translation


def reverse(
    viewname,
    urlconf=None,
    args=None,
    kwargs=None,
    current_app=None,
    locale=None,
    query=None,
    fragment=None,
):
    """
    Thin wrapper around Django's reverse that allows you to force the locale to something
    other than the currently activated locale. Does NOT do prefixing - we use i18n_patterns
    for that
    """
    with translation.override(locale) if locale else contextlib.nullcontext():
        return django_reverse(
            viewname,
            urlconf=urlconf,
            args=args,
            kwargs=kwargs,
            current_app=current_app,
            query=query,
            fragment=fragment,
        )
