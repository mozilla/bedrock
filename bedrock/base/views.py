import json
import os.path
import re
from datetime import datetime
from os import getenv
from time import time

import timeago
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe
from lib import l10n_utils

from bedrock.base.geo import get_country_from_request
from bedrock.utils import git


@method_decorator(never_cache, name='dispatch')
class GeoRedirectView(RedirectView):
    # dict of country codes to full URLs or URL names
    geo_urls = None
    # default URL or URL name for countries not in `geo_urls`
    default_url = None
    # default to sending the query parameters through to the redirect
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        country_code, _ = get_country_from_request(self.request)
        url = self.geo_urls.get(country_code, self.default_url)
        if re.match(r'https?://', url, re.I):
            self.url = url
        else:
            self.pattern_name = url

        return super().get_redirect_url(*args, **kwargs)


@require_safe
@never_cache
def geolocate(request):
    """Return the country code provided by our CDN

    https://support.cloudflare.com/hc/en-us/articles/200168236-What-does-CloudFlare-IP-Geolocation-do-

    Mimics the responses from the Mozilla Location Service:

    https://mozilla.github.io/ichnaea/api/region.html
    """
    country_code, source = get_country_from_request(request)
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
        'data_source': source,
    })


# file names and max seconds since last run
HEALTH_FILES = (
    ('download_database', 600),
    ('update_locales', 600),
)
DB_INFO_FILE = getenv('AWS_DB_JSON_DATA_FILE', f'{settings.DATA_PATH}/bedrock_db_info.json')
GIT_SHA = getenv('GIT_SHA')
BUCKET_NAME = getenv('AWS_DB_S3_BUCKET', 'bedrock-db-dev')
REGION_NAME = os.getenv('AWS_DB_REGION', 'us-west-2')
S3_BASE_URL = 'https://s3-{}.amazonaws.com/{}'.format(
    REGION_NAME,
    BUCKET_NAME,
)


def get_l10n_repo_info():
    repo = git.GitRepo(settings.LOCALES_PATH, settings.LOCALES_REPO)
    fluent_repo = git.GitRepo(settings.FLUENT_REPO_PATH, settings.FLUENT_REPO_URL)
    return ({
        'latest_ref': repo.current_hash,
        'last_updated': repo.last_updated,
        'repo_url': repo.clean_remote_url,
    }, {
        'latest_ref': fluent_repo.current_hash,
        'last_updated': fluent_repo.last_updated,
        'repo_url': fluent_repo.clean_remote_url,
    })


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
        for key, value in db_info.items():
            server_info['db_%s' % key] = value

    # Maxmind DB File Info
    try:
        geo_last_mod = os.path.getmtime(settings.MAXMIND_DB_PATH)
    except FileNotFoundError:
        pass
    else:
        server_info['geo_last_update'] = timeago.format(datetime.fromtimestamp(geo_last_mod))

    return server_info


@require_safe
@never_cache
def cron_health_check(request):
    results = []
    check_pass = True
    for fname, max_time in HEALTH_FILES:
        fpath = f'{settings.DATA_PATH}/last-run-{fname}'
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

    git_repos = git.GitRepoState.objects.exclude(repo_name='').order_by('repo_name', '-latest_ref_timestamp')
    unique_repos = {}
    for repo in git_repos:
        if repo.repo_name in unique_repos:
            continue
        unique_repos[repo.repo_name] = repo

    l10n_repo, fluent_repo = get_l10n_repo_info()
    return render(request, 'cron-health-check.html', {
        'results': results,
        'server_info': get_extra_server_info(),
        'success': check_pass,
        'git_repos': unique_repos.values(),
        'l10n_repo': l10n_repo,
        'fluent_repo': fluent_repo,
    }, status=200 if check_pass else 500)


def server_error_view(request, template_name='500.html'):
    """500 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, status=500)


def page_not_found_view(request, exception=None, template_name='404.html'):
    """404 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, status=404)
