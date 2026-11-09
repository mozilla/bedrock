# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.fixtures.base_fixtures import get_test_index_page
from bedrock.mozorg.models import ArticlePage

DEFAULT_INTRO = {
    "type": "intro_block",
    "value": {
        "settings": {"background_color": "", "heading_size": ""},
        "heading": "Article test page",
        "body": "<p>This intro is shared by test pages that exercise other blocks.</p>",
    },
    "id": "article-default-intro",
}


def get_article_test_page(
    slug: str,
    title: str,
    intro: dict | None = None,
    content: list | None = None,
) -> ArticlePage:
    """Get or create a published ArticlePage under the block tests index page.

    Args:
        slug: Slug for the test page
        title: Title for the test page
        intro: Intro block data; defaults to DEFAULT_INTRO
        content: List of content block data

    Returns:
        ArticlePage instance
    """
    test_page = ArticlePage.objects.filter(slug=slug).first()
    if test_page:
        return test_page

    test_page = ArticlePage(
        title=title,
        slug=slug,
        intro=[intro or DEFAULT_INTRO],
        content=content or [],
    )

    get_test_index_page().add_child(instance=test_page)
    test_page.save_revision().publish()

    return test_page
