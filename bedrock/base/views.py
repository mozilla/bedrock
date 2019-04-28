import json
import logging
import os.path
from datetime import datetime
from os import getenv
from time import time

import timeago
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_safe
from lib import l10n_utils
from raven.contrib.django.models import client

from bedrock.utils import git


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
        return JsonResponse({
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

    return JsonResponse({
        'country_code': country_code,
    })


# file names and max seconds since last run
HEALTH_FILES = (
    ('download_database', 600),
    ('update_locales', 600),
)
DB_INFO_FILE = getenv('AWS_DB_JSON_DATA_FILE', 'bedrock_db_info.json')
GIT_SHA = getenv('GIT_SHA')
BUCKET_NAME = getenv('AWS_DB_S3_BUCKET', 'bedrock-db-dev')
REGION_NAME = os.getenv('AWS_DB_REGION', 'us-west-2')
S3_BASE_URL = 'https://s3-{}.amazonaws.com/{}'.format(
    REGION_NAME,
    BUCKET_NAME,
)


def get_l10n_repo_info():
    repo = git.GitRepo(settings.LOCALES_PATH, settings.LOCALES_REPO)
    return {
        'latest_ref': repo.current_hash,
        'last_updated': repo.last_updated,
        'repo_url': repo.clean_remote_url,
    }


def get_db_file_url(filename):
    return '/'.join([S3_BASE_URL, filename])


def get_extra_server_info():
    server_name = [getattr(settings, x) for x in ['HOSTNAME', 'CLUSTER_NAME']]
    server_name = '.'.join(x for x in server_name if x)
    server_info = {
        'name': server_name,
        'git_sha': GIT_SHA,
    }
    try:
        with open(DB_INFO_FILE, 'r') as fp:
            db_info = json.load(fp)
    except (IOError, ValueError):
        pass
    else:
        db_info['last_update'] = timeago.format(datetime.fromtimestamp(db_info['updated']))
        db_info['file_url'] = get_db_file_url(db_info['file_name'])
        for key, value in list(db_info.items()):
            server_info['db_%s' % key] = value

    return server_info


@require_safe
@never_cache
def cron_health_check(request):
    results = []
    check_pass = True
    for fname, max_time in HEALTH_FILES:
        fpath = '/tmp/last-run-%s' % fname
        try:
            last_check = os.path.getmtime(fpath)
        except OSError:
            check_pass = False
            results.append((fname, max_time, 'None', False))
            continue

        time_since = int(time() - last_check)
        if time_since > max_time:
            task_pass = False
            check_pass = False
        else:
            task_pass = True

        results.append((fname, max_time, time_since, task_pass))

    git_repos = git.GitRepoState.objects.exclude(repo_name='').order_by('repo_name')
    return render(request, 'cron-health-check.html', {
        'results': results,
        'server_info': get_extra_server_info(),
        'success': check_pass,
        'git_repos': git_repos,
        'l10n_repo': get_l10n_repo_info(),
    }, status=200 if check_pass else 500)


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
