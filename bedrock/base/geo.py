# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

try:
    import maxminddb
except ImportError:
    maxminddb = None


if maxminddb is not None:
    try:
        geo = maxminddb.open_database(settings.MAXMIND_DB_PATH)
    except (IOError, maxminddb.InvalidDatabaseError):
        geo = None
else:
    geo = None


def get_country_from_ip(ip_addr):
    """Return country info for the given IP Address."""
    if geo is not None:
        try:
            data = geo.get(ip_addr)
        except ValueError:
            data = None

        if data:
            country = data.get('country', data.get('registered_country'))
            if country:
                return country['iso_code'].upper()

    return settings.MAXMIND_DEFAULT_COUNTRY.upper()


def get_country_from_request(request):
    """Return country info for the given request data."""
    client_ip = request.META.get('HTTP_X_CLUSTER_CLIENT_IP',
                                 request.META.get('REMOTE_ADDR'))
    return get_country_from_ip(client_ip)
