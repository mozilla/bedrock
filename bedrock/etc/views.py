# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re

from django.shortcuts import redirect
from django.views.generic.base import TemplateView


class ThankyouView(TemplateView):
    template_name = 'etc/firefox/retention/thank-you-referral.html'
    support_url = ('https://support.mozilla.org/products/firefox'
                   '?utm_medium=referral&utm_source=heartbeat'
                   '&utm_campaign=desktop-referral-loop-v1')
    score_re = re.compile(r'^\d$')

    def get_score(self):
        score = self.request.GET.get('score', '5')
        if self.score_re.match(score):
            return int(score)

        return 5

    def get(self, request, *args, **kwargs):
        score = self.get_score()
        if score < 4:
            return redirect(self.support_url)

        return super(ThankyouView, self).get(request, *args, **kwargs)
