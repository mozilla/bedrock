# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
from datetime import datetime
from random import randrange

from django import forms
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe

from lib.l10n_utils.fluent import ftl, ftl_lazy

FORMATS = (("H", ftl_lazy("newsletter-form-html")), ("T", ftl_lazy("newsletter-form-text")))
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

        policy_txt = ftl("newsletter-form-im-okay-with-mozilla", url=reverse("privacy.notices.websites"))

        return mark_safe(f"""<label for="{attrs['id']}" class="privacy-check-label">{input_txt}<span class="title">{policy_txt}</span></label>""")


class HoneyPotWidget(widgets.TextInput):
    """Render a text field to (hopefully) trick bots. Will be used on many pages."""

    def render(self, name, value, attrs=None, renderer=None):
        honeypot_txt = ftl("newsletter-form-leave-this-field-empty")
        # semi-randomized in case we have more than one per page.
        # this is maybe/probably overthought
        honeypot_id = "office-fax-" + str(randrange(1001)) + "-" + str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
        return mark_safe(
            '<div class="super-priority-field">'
            '<label for="%s">%s</label>'
            '<input type="text" name="office_fax" id="%s">'
            "</div>" % (honeypot_id, honeypot_txt, honeypot_id)
        )


class URLInput(widgets.TextInput):
    input_type = "url"


class EmailInput(widgets.TextInput):
    input_type = "email"


class DateInput(widgets.DateInput):
    input_type = "date"


class TimeInput(widgets.TimeInput):
    input_type = "time"


class TelInput(widgets.TextInput):
    input_type = "tel"


class NumberInput(widgets.TextInput):
    input_type = "number"


class MeicoEmailForm(forms.Form):
    """
    A form class used to validate the data coming from the MEICO site.
    """

    name = forms.CharField(required=False, max_length=100)
    email = forms.EmailField()
    interests = forms.CharField(required=False, max_length=100)
    description = forms.CharField(required=False, max_length=750)
