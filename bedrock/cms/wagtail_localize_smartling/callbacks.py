# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This file contains callback functions to be called by
# github.com/mozilla/wagtail-localize-smartling/ and
# hooked in via settings.
#
# The README.md of that repo covers what inputs are
# provided and what outputs are needed
import logging
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from django.conf import settings
from django.test import RequestFactory

from wagtail.models import Page, Site
from wagtail_localize_smartling.exceptions import IncapableVisualContextCallback

if TYPE_CHECKING:
    from wagtail_localize_smartling.models import Job
from sentry_sdk import capture_exception, capture_message
from wagtaildraftsharing.models import WagtaildraftsharingLink
from wagtaildraftsharing.views import SharingLinkView

logger = logging.getLogger(__name__)


def _get_html_for_sharing_link(sharing_link: WagtaildraftsharingLink) -> str:
    # Use the CMS hostname (guaranteed to be in ALLOWED_HOSTS) so that
    # Wagtail's make_preview_request doesn't fall back to 'testserver' /
    # 'localhost', which would cause DisallowedHost inside the middleware
    # chain and return a 400 error page instead of the real page HTML.
    # Also extract just the path from sharing_link.url in case it's absolute.
    cms_hostname = urlparse(settings.WAGTAILADMIN_BASE_URL).hostname
    path = urlparse(sharing_link.url).path
    request = RequestFactory(SERVER_NAME=cms_hostname).get(path)
    view_func = SharingLinkView.as_view()
    try:
        resp = view_func(
            request=request,
            key=sharing_link.key,
        )
        return resp.text
    except Exception as ex:
        # Ensure Sentry gets any problem with turning the sharing link into HTML
        capture_exception(ex)
        raise IncapableVisualContextCallback("Was not able to get a HTML export from the sharing link")


def _get_full_url_for_sharing_link(sharing_link: WagtaildraftsharingLink) -> str:
    url = f"{settings.WAGTAILADMIN_BASE_URL}{sharing_link.url}"
    logger.debug("Page URL being sent to Smartling: %s", url)
    return url


def visual_context(smartling_job: "Job") -> tuple[str, str]:
    # Needs to return two strings:
    # 1. A URL where the content object (usually a Page; possibly a draft one)
    #    can be viewed _without authentication_
    # 2. The HTML of the state of the page at this point in time

    content_obj = smartling_job.translation_source.get_source_instance()

    if not isinstance(content_obj, Page):
        # We can currently only supply visual context for Pages, but not for
        # other things like Snippets, so return early and show there's nothing
        # to be processed
        raise IncapableVisualContextCallback("Object was not visually previewable (i.e. not a Page)")

    revision = content_obj.latest_revision
    if revision is None:
        # The only time we'll have a situation like this is when someone is using
        # a DB export from dev/stage/prod, which has all of its revision history
        # excluded from the export.
        capture_message(f"Unable to get a latest_revision for {content_obj} so unable to send visual context.")
        raise IncapableVisualContextCallback(
            "Object was not visually previewable because it didn't have a saved revision. Are you a developer with a local export?"
        )

    # Always use `create_for_revision` to ensure max lifespan of the link
    sharing_link = WagtaildraftsharingLink.objects.create_for_revision(
        revision=revision,
        user=smartling_job.user,
        max_ttl=-1,  # -1 signifies "No expiry". If we pass None we get the default TTL
    )

    url = _get_full_url_for_sharing_link(sharing_link=sharing_link)
    html = _get_html_for_sharing_link(sharing_link=sharing_link)

    # Strip the CMS hostname from URLs in the HTML so they become relative,
    # then inject a <base> tag so Smartling resolves them against the public
    # domain rather than the IAP-protected CMS host.
    default_site = Site.objects.filter(is_default_site=True).first()
    if default_site:
        html = html.replace(default_site.root_url, "")
    base_tag = f'<base href="{settings.CANONICAL_URL}/">'
    html = html.replace("<head>", f"<head>{base_tag}", 1)

    return (url, html)
