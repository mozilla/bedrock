# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.http import Http404


def get_page_for_path(request, path):
    from wagtail.models import Site

    site = Site.find_for_request(request)
    try:
        page, args, kwargs = site.root_page.specific.route(request, path)
        return page
    except Http404:
        pass

    return None


def get_locales_for_cms_page(page):
    # Patch in a list of CMS-available locales for pages that are
    # translations, not just aliases

    locales_available_via_cms = [page.locale.language_code]
    try:
        _actual_translations = (
            page.get_translations()
            .live()
            .exclude(
                id__in=[x.id for x in page.aliases.all()],
            )
        )
        locales_available_via_cms += [x.locale.language_code for x in _actual_translations]
    except ValueError:
        # when there's no draft and no potential for aliases, etc, the above lookup will fail
        pass

    return locales_available_via_cms


def get_cms_locales_for_path(request):
    locales = []

    if page := get_page_for_path(request=request, path=request.path):
        locales = get_locales_for_cms_page(page)

    return locales
