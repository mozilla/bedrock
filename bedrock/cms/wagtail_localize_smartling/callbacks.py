# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This file contains callback functions to be called by
# github.com/mozilla/wagtail-localize-smartling/ and
# hooked in via settings.
#
# The README.md of that repo covers what inputs are
# provided and what outputs are needed

from typing import TYPE_CHECKING

from django.test import RequestFactory

from wagtail.models import Page
from wagtail_localize_smartling.exceptions import IncapableVisualContextCallback

if TYPE_CHECKING:
    from wagtail_localize_smartling.models import Job
from sentry_sdk import capture_exception, capture_message
from wagtaildraftsharing.models import WagtaildraftsharingLink
from wagtaildraftsharing.views import SharingLinkView


def _get_html_for_sharing_link(sharing_link: WagtaildraftsharingLink) -> str:
    request = RequestFactory().get(sharing_link.url)
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


def _get_full_url_for_sharing_link(sharing_link: WagtaildraftsharingLink, page: "Page") -> str:
    return f"{page.get_site().root_url}{sharing_link.url}"


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

    url = _get_full_url_for_sharing_link(sharing_link=sharing_link, page=content_obj)
    html = _get_html_for_sharing_link(sharing_link=sharing_link)
    return (url, html)
