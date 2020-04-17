# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.views.generic.base import TemplateView
from lib import l10n_utils


class WhatsnewView(l10n_utils.LangFilesMixin, TemplateView):
    def get_template_names(self):
        return ['exp/firefox/whatsnew/whatsnew-fx71.html']


def new(request):

    # note: v and xv params only allow a-z, A-Z, 0-9, -, and _ characters
    experience = request.GET.get('xv', None)
    variant = request.GET.get('v', None)

    # ensure experience matches pre-defined value
    if experience not in ['']:  # place expected ?xv= values in this list
        experience = None

    # ensure variant matches pre-defined value
    if variant not in ['a', 'b', 'c']:  # place expected ?v= values in this list
        variant = None

    # no harm done by passing 'v' to template, even when no experiment is running
    # (also makes tests easier to maintain by always sending a context)
    return l10n_utils.render(
        request, 'exp/firefox/new/download.html', {'experience': experience, 'v': variant, 'active_locales': ['en-US', 'en-GB', 'en-CA', 'de']}
    )
