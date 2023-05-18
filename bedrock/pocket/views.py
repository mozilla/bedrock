# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from bedrock.pocket.forms import NewsletterForm
from bedrock.utils.braze import client as braze_client
from lib import l10n_utils


def server_error_view(request, template_name="pocket/500.html"):
    """500 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, ftl_files=["pocket/500"], status=500)


def page_not_found_view(request, exception=None, template_name="pocket/404.html"):
    """404 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, ftl_files=["pocket/404"], status=404)


@require_POST
def newsletter_subscribe(request):
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"status": "error", "detail": "Error parsing JSON data"}, status=400)

    external_id = request.COOKIES.get(settings.BRAZE_POCKET_COOKIE_NAME) or None

    form = NewsletterForm(data)
    if form.is_valid():
        email = form.cleaned_data.pop("email")
        newsletter = form.cleaned_data.pop("newsletter")
    else:
        return JsonResponse({"status": "error", "detail": form.errors}, status=400)

    # Drop out any fields with empty strings as their values
    clean_data = {}
    for fieldname, value in form.cleaned_data.items():
        if value != "":
            clean_data[fieldname] = value
    try:
        braze_client.subscribe(email, newsletter, external_id=external_id, **clean_data)
    except Exception:
        return JsonResponse({"status": "error", "detail": "Error contacting subscription provider"}, status=500)

    return JsonResponse({"status": "success"})
