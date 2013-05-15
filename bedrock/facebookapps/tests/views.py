# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.http import HttpResponse

from bedrock.facebookapps import decorators
from bedrock.facebookapps.tests import DUMMY_CONTENT


@decorators.facebook_locale
def dummy_locale_view(request):
    return HttpResponse(DUMMY_CONTENT)


@decorators.extract_app_data
def dummy_app_data_view(request):
    return HttpResponse(DUMMY_CONTENT)
