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
            pass

    return GEO


def get_country_from_ip(ip_addr):
    """Return country info for the given IP Address."""
    geo = _get_geo_client()
    if geo is None and settings.DEV:
        return settings.MAXMIND_DEFAULT_COUNTRY.upper()

    if geo is not None:
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
    ip_addr = request.META.get('HTTP_X_CLUSTER_CLIENT_IP',
                               request.META.get('REMOTE_ADDR'))
    return get_country_from_ip(ip_addr)


def get_country_from_request(request):
    """Return country info for the given request data."""
    country = get_country_from_maxmind(request)
    if country is None:
        country = get_country_from_request_header(request)

    return country
