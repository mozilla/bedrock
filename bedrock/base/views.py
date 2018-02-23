import json
import logging

from django.conf import settings
from django.db import DatabaseError
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_safe

from bedrock.mozorg.util import HttpResponseJSON
from bedrock.wordpress.models import BlogPost
from lib import l10n_utils

from raven.contrib.django.models import client


def get_geo_from_request(request):
    """Return an uppercase 2 letter country code retrieved from request headers."""
    if settings.DEV:
        country_code = settings.DEV_GEO_COUNTRY_CODE
    else:
        country_code = request.META.get('HTTP_CF_IPCOUNTRY', 'XX')

    if country_code == 'XX' or len(country_code) != 2:
        return None

    return country_code.upper()


@require_safe
@never_cache
def geolocate(request):
    """Return the country code provided by our CDN

    https://support.cloudflare.com/hc/en-us/articles/200168236-What-does-CloudFlare-IP-Geolocation-do-

    Mimics the responses from the Mozilla Location Service:

    https://mozilla.github.io/ichnaea/api/region.html
    """
    country_code = get_geo_from_request(request)
    if country_code is None:
        return HttpResponseJSON({
            "error": {
                "errors": [{
                    "domain": "geolocation",
                    "reason": "notFound",
                    "message": "Not found",
                }],
                "code": 404,
                "message": "Not found",
            }
        }, status=404)

    return HttpResponseJSON({
        'country_code': country_code,
    })


# copied from
# https://github.com/mozilla/kuma/blob/master/kuma/health/views.py
@require_safe
def liveness(request):
    """
    A successful response from this endpoint simply proves
    that Django is up and running. It doesn't mean that its
    supporting services (like MySQL, Redis, Celery) can
    be successfully used from within this service.
    """
    return HttpResponse(status=200)


# copied from
# https://github.com/mozilla/kuma/blob/master/kuma/health/views.py
@require_safe
@cache_page(10)
def readiness(request):
    """
    A successful response from this endpoint goes a step further
    and means not only that Django is up and running, but also that
    the database can be successfully used from within this service.
    Some other supporting services (like ElasticSearch) are not checked,
    but we may find that we want/need to add them later.

    Wrapped with `cache_page` to test cache.
    """
    try:
        # Confirm that we can use the database by making a fast query
        # against the Newsletter table. It's not important that the document
        # with the requested primary key exists or not, just that the query
        # completes without error.
        BlogPost.objects.filter(pk=1).exists()
    except DatabaseError as e:
        reason_tmpl = 'service unavailable due to database issue ({!s})'
        status, reason = 503, reason_tmpl.format(e)
    else:
        status, reason = 204, None

    return HttpResponse(status=status, reason=reason)


def server_error_view(request, template_name='500.html'):
    """500 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, status=500)


@csrf_exempt
@require_POST
def csp_violation_capture(request):
    # HT @glogiotatidis https://github.com/mozmeao/lumbergh/pull/180/
    if not settings.CSP_REPORT_ENABLE:
        # mitigation option for a flood of violation reports
        return HttpResponse()

    data = client.get_data_from_request(request)
    data.update({
        'level': logging.INFO,
        'logger': 'CSP',
    })
    try:
        csp_data = json.loads(request.body)
    except ValueError:
        # Cannot decode CSP violation data, ignore
        return HttpResponseBadRequest('Invalid CSP Report')

    try:
        blocked_uri = csp_data['csp-report']['blocked-uri']
    except KeyError:
        # Incomplete CSP report
        return HttpResponseBadRequest('Incomplete CSP Report')

    client.captureMessage(message='CSP Violation: {}'.format(blocked_uri),
                          data=data)

    return HttpResponse('Captured CSP violation, thanks for reporting.')
