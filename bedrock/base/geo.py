# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

from product_details import product_details


def valid_country_code(country):
    codes = product_details.get_regions("en-US").keys()
    if country and country.lower() in codes:
        return country.upper()


def get_country_from_param(request):
    is_prod = request.get_host() == "www.mozilla.org"
    country_code = valid_country_code(request.GET.get("geo"))
    return country_code if not is_prod else None


def get_country_from_header(request):
    """Return an uppercase 2 letter country code retrieved from the request header."""
    country_code = request.headers.get("Cloudfront-Viewer-Country", request.headers.get("CF-IPCountry"))
    country_code = valid_country_code(country_code)
    if not country_code and settings.DEV:
        country_code = settings.DEV_GEO_COUNTRY_CODE

    return country_code


def get_country_from_request(request):
    """Return a country code from either the request geo param or header from CDN"""
    param_code = get_country_from_param(request)
    header_code = get_country_from_header(request)
    return param_code or header_code
