# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.views.decorators.http import require_safe
from django.views.generic import TemplateView

from product_details import product_details

from lib import l10n_utils
from lib.l10n_utils import RequireSafeMixin


class Robots(RequireSafeMixin, TemplateView):
    template_name = "mozorg/robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs):
        hostname = self.request.get_host()
        return {"disallow_all": not hostname == "www.mozilla.org"}


class SecurityDotTxt(RequireSafeMixin, TemplateView):
    # https://github.com/mozilla/bedrock/issues/14173
    # served under .well-known/security.txt
    template_name = "mozorg/security.txt"
    content_type = "text/plain"


class GpcDotJson(RequireSafeMixin, TemplateView):
    # https://github.com/mozilla/bedrock/issues/14213
    # served under .well-known/gpc.json
    template_name = "mozorg/gpc.json"
    content_type = "application/json"


@require_safe
def locales(request):
    context = {"languages": product_details.languages}
    return l10n_utils.render(request, "mozorg/locales.html", context)
