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

    print(ctx)

    return l10n_utils.render(request, template_name, ctx)


@require_safe
def pbj_landing_page(request):
    """Contentful PBJ Landing Page"""
    # ft. is latest published
    # all other articles listed in Other Stories section by publish date
    template_name = "stories/contentful-landing.html"

    # get all stories
    # todo: order by official published date (newest to oldest), not necessarily last modified
    # does it make sense to convert this to a list?
    # should there be a _get_pbj_story_preview function that formats the data?
    stories = [
        story.data["info"]
        for story in ContentfulEntry.objects.get_entries_by_type(
            locale="en-US", content_type=CONTENT_TYPE_PAGE_PRODUCT_STORY, localisation_complete=False
        )
    ]

    # todo:
    # - separate featured story from other stories
    # is there a better way to take the latest published story out of the list? does it need to be a list?
    featured_story = stories.pop(0)
    # - only send preview data (no content body)

    ctx = {"featured_story": featured_story, "stories": stories}

    # I only get one story here, but there are two (both in draft status) in contentful sandbox
    print(len(stories))
    print(stories)

    return l10n_utils.render(request, template_name, ctx)
