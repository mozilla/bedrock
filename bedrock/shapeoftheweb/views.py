# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.views.decorators.cache import cache_control

from lib import l10n_utils


@cache_control(public=True, max_age=60 * 15)
def localized_json(request, filename):
    """Render a JSON file with localized strings."""
    return l10n_utils.render(request, 'shapeoftheweb/{0}'.format(filename),
                             content_type='application/json; charset=utf8')
