# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from lib import l10n_utils


def server_error_view(request, template_name="pocket/500.html"):
    """500 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, ftl_files=["pocket/500"], status=500)


def page_not_found_view(request, exception=None, template_name="pocket/404.html"):
    """404 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, ftl_files=["pocket/404"], status=404)
