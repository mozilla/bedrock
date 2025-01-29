# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re

from django.forms import widgets
from django.utils.safestring import mark_safe

from lib.l10n_utils.fluent import ftl

LANGS_TO_STRIP = ["en-US", "es"]
PARENTHETIC_RE = re.compile(r" \([^)]+\)$")


def strip_parenthetical(lang_name):
    """
    Remove the parenthetical from the end of the language name string.
    """
    return PARENTHETIC_RE.sub("", lang_name, 1)


class PrivacyWidget(widgets.CheckboxInput):
    """Render a checkbox with privacy text. Lots of pages need this so
    it should be standardized"""

    def render(self, name, value, attrs=None, renderer=None):
        attrs["required"] = "required"
        input_txt = super().render(name, value, attrs)

        policy_txt = ftl("newsletter-form-im-okay-with-mozilla", url="https://www.mozilla.org/privacy/websites/")

        return mark_safe(f"""<label for="{attrs["id"]}" class="privacy-check-label">{input_txt}<span class="title">{policy_txt}</span></label>""")


class EmailInput(widgets.TextInput):
    input_type = "email"
