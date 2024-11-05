# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


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
