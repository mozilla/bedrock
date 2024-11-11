# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest import mock

from django.http import HttpResponse

from bedrock.cms.decorators import prefer_cms

test_callable_to_get_locales = mock.Mock(return_value=["sco", "es-ES"])


def undecorated_dummy_view(request):
    return HttpResponse("This is a dummy response from the undecorated view")


@prefer_cms
def decorated_dummy_view(request):
    return HttpResponse("This is a dummy response from the decorated view")


@prefer_cms(fallback_lang_codes=["fr-CA", "es-MX", "sco"])
def decorated_dummy_view_with_locale_strings(request):
    return HttpResponse("This is a dummy response from the decorated view with locale strings passed in")


@prefer_cms(fallback_ftl_files=["test/fluentA", "test/fluentB"])
def decorated_dummy_view_with_fluent_files(request):
    return HttpResponse("This is a dummy response from the decorated view with fluent files explicitly passed in")


def wrapped_dummy_view(request, *args, **kwargs):
    return HttpResponse("This is a dummy response from the wrapped view")


@prefer_cms(fallback_callable=test_callable_to_get_locales)
def decorated_dummy_view_for_use_with_a_callable(request, *args, **kwargs):
    return HttpResponse(f"This is a dummy response from the decorated view for the callable, taking {args} and {kwargs}")
