# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.views.decorators.http import require_safe

from bedrock.contentful.constants import CONTENT_TYPE_PAGE_PRODUCT_STORY
from bedrock.contentful.models import ContentfulEntry
from lib import l10n_utils


@require_safe
def pbj_story_page(request, slug):
    """Contentful PBJ Story Page"""

    template_name = "stories/contentful-story.html"

    ctx = {}
    story = ContentfulEntry.objects.get_entry_by_slug(
        slug=slug, locale="en-US", content_type=CONTENT_TYPE_PAGE_PRODUCT_STORY, localisation_complete=False  # EN only content
    )
    ctx.update(story.data)

    return l10n_utils.render(request, template_name, ctx)


@require_safe
def pbj_landing_page(request):
    """Contentful PBJ Landing Page"""
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

    return l10n_utils.render(request, template_name, ctx)
