# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jingo

from l10n_utils.helpers import gettext


# TODO: Fix tower and remove this.
class FixLangFileTranslationsMiddleware(object):
    """
    Middleware that will overwrite the gettext functions in the Jinja2 setup.
    tower.activate() called by LocaleURLMiddleware sets them to tower's own
    functions.

    Bug 808580
    """

    def process_request(self, request):
        jingo.env.install_gettext_callables(gettext, gettext)
