# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.views.decorators.http import require_safe

from sentry_sdk import capture_exception

# todo: add tests for switch functionality
from bedrock.base.waffle import switch
from bedrock.contentful.constants import CONTENT_TYPE_PAGE_PRODUCT_STORY
from bedrock.contentful.models import ContentfulEntry
from lib import l10n_utils


@require_safe
def story_page(request, slug):
    """If switch is ON, use Contentful PBJ Story Page"""

    ctx = {}

    if switch("contentful-product-story"):
        try:
            template_name = "stories/contentful-story.html"
            story = ContentfulEntry.objects.get_entry_by_slug(
                slug=slug, locale="en-US", content_type=CONTENT_TYPE_PAGE_PRODUCT_STORY, localisation_complete=False  # EN only content
            )
            ctx.update(story.data)
        except Exception as ex:
            capture_exception(ex)
    else:
        # set hardcoded story article pages
        template_name = f"stories/articles/{slug}.html"

    return l10n_utils.render(request, template_name, ctx)


@require_safe
def landing_page(request):
    """If switch is ON, use Contentful PBJ Landing Page"""

    ctx = {}

    if switch("contentful-product-story"):
        try:
            template_name = "stories/contentful-landing.html"
            # get all stories (TODO: order by info.published field, newest story should be first in list)
            stories = [
                story.data["info"]
                for story in ContentfulEntry.objects.get_entries_by_type(
                    locale="en-US", content_type=CONTENT_TYPE_PAGE_PRODUCT_STORY, localisation_complete=False
                )
            ]
            # Remove first story from list for spotlight as featured story
            featured_story = stories.pop(0)
            ctx = {"featured_story": featured_story, "stories": stories}
        except Exception as ex:
            print("error!")
            capture_exception(ex)
    else:
        # set hardcoded landing page
        template_name = "stories/landing.html"

    return l10n_utils.render(request, template_name, ctx)
