# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from jinja2.ext import InternationalizationExtension

from lib.l10n_utils.templatetags.helpers import gettext
from lib.l10n_utils.utils import strip_whitespace


class I18nExtension(InternationalizationExtension):
    """
    Use this instead of `puente.ext.PuenteI18nExtension` because the override of `_`
    global was throwing errors.
    """

    def _parse_block(self, parser, allow_pluralize):
        ref, buffer = super()._parse_block(parser, allow_pluralize)
        return ref, strip_whitespace(buffer)


# Makes for a prettier import in settings.py
i18n = I18nExtension

# TODO: make an ngettext compatible function.
# The pluaralize clause of a trans block won't work untill we do.
# Need this so that installing translations will work in Jinja.
ngettext = gettext
