# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.admin.forms.pages import CopyForm


class BedrockCopyForm(CopyForm):
    """Wagtail's page copy form plus a "Keep analytics IDs" opt-out.

    By default a copied page gets freshly generated analytics IDs (see the
    ``after_copy_page`` hook). Ticking this box preserves the source page's IDs
    instead. The checkbox is rendered by the overridden
    ``wagtailadmin/pages/copy.html`` template and read from ``request.POST`` by
    the hook.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["keep_analytics_ids"] = forms.BooleanField(
            required=False,
            initial=False,
            label=_("Keep analytics IDs"),
            help_text=_("Preserve the original page's analytics tracking IDs instead of generating new ones for the copy."),
        )
