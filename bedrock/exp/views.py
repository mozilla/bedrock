# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.views.generic.base import TemplateView
from lib import l10n_utils


class WhatsnewView(l10n_utils.LangFilesMixin, TemplateView):
    def get_template_names(self):
        return ['exp/firefox/whatsnew/whatsnew-fx70.html']
