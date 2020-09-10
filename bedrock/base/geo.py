# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

try:
    import maxminddb
except ImportError:
    maxminddb = None


GEO = None


def _get_geo_client():
    global GEO
    if GEO is None and maxminddb is not None:
        try:
            GEO = maxminddb.open_database(settings.MAXMIND_DB_PATH)
        except (maxminddb.InvalidDatabaseError, OSError, IOError):
            GEO = False

    return GEO


def get_country_from_ip(ip_addr):
    """Return country info for the given IP Address."""
    geo = _get_geo_client()
    if not geo and settings.DEV:
        return settings.MAXMIND_DEFAULT_COUNTRY.upper()

    if geo and ip_addr:
        try:
            data = geo.get(ip_addr)
        except ValueError:
            data = None

        if data:
            country = data.get('country', data.get('registered_country'))
            if country:
                return country['iso_code'].upper()

    return None


def get_country_from_request_header(request):
    """Return an uppercase 2 letter country code retrieved from request headers."""
    if settings.DEV:
        country_code = settings.DEV_GEO_COUNTRY_CODE
    else:
        country_code = request.META.get('HTTP_CF_IPCOUNTRY', 'XX')

    if country_code == 'XX' or len(country_code) != 2:
        return None

    return country_code.upper()


def get_country_from_maxmind(request):
    ip_addr = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if ',' in ip_addr:
        ip_addr = ip_addr.split(',', 1)[0]

    return get_country_from_ip(ip_addr.strip())


def get_country_from_request(request):
    """Return country info for the given request data."""
    country = get_country_from_maxmind(request)
    source = 'local'
    if country is None:
        country = get_country_from_request_header(request)
        source = 'cdn'

    return country, source
