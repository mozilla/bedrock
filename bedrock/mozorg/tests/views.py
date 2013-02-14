# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.http import HttpResponse

from bedrock.mozorg.decorators import cache_control_expires


RESPONSE_CONTENT = 'The Dude abides, man.'
RESPONSE_ETAG = '"9766cf1452d8b193ef3b608848863a13"'


@cache_control_expires(48)
def view_test_48_hrs(request):
    return HttpResponse(RESPONSE_CONTENT)


@cache_control_expires(24 * 30)
def view_test_30_days(request):
    return HttpResponse(RESPONSE_CONTENT)
