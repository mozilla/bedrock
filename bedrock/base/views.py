import os.path
import json
import logging
from time import time

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_safe

from bedrock.mozorg.util import HttpResponseJSON
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


@require_safe
@never_cache
def health_check(request):
    return HttpResponse('OK')


# file names and max seconds since last run
HEALTH_FILES = (
    ('ical_feeds', 65 * 60),
    ('update_blog_feeds', 65 * 60),
    ('update_externalfiles', 35 * 60),
    ('update_locales', 15 * 60),
    ('update_product_details', 20 * 60),
    ('update_release_notes', 15 * 60),
    ('update_security_advisories', 35 * 60),
    ('update_tweets', 7 * 60 * 60),
)


@require_safe
@never_cache
def cron_health_check(request):
    results = []
    check_fail = False
    for fname, max_time in HEALTH_FILES:
        fpath = '/tmp/last-run-%s' % fname
        try:
            last_check = os.path.getmtime(fpath)
        except OSError:
            check_fail = True
            results.append((fname, max_time, 'None', False))
            continue

        time_since = int(time() - last_check)
        if time_since > max_time:
            task_pass = False
            check_fail = True
        else:
            task_pass = True

        results.append((fname, max_time, time_since, task_pass))

    return render(request, 'cron-health-check.html', {'results': results},
                  status=500 if check_fail else 200)


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
