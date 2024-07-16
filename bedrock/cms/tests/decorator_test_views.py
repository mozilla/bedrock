# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.http import HttpResponse

from bedrock.cms.decorators import prefer_cms


def undecorated_dummy_view(request):
    return HttpResponse("This is a dummy response from the undecorated view")


@prefer_cms
def decorated_dummy_view(request):
    return HttpResponse("This is a dummy response from the decorated view")


def wrapped_dummy_view(request):
    return HttpResponse("This is a dummy response from the wrapped view")
