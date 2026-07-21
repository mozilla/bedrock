# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from wagtail.models import Site

from bedrock.anonym.models import AnonymIndexPage, Person
from bedrock.mozorg.fixtures.base_fixtures import get_placeholder_image  # noqa: F401


def get_test_anonym_index_page() -> AnonymIndexPage:
    """Get or create a test AnonymIndexPage for fixture tests.

    Returns:
        AnonymIndexPage instance to use as parent for test pages
    """
    site = Site.objects.get(is_default_site=True)
    root_page = site.root_page

    index_page = AnonymIndexPage.objects.filter(slug="tests-anonym-index-page").first()
    if not index_page:
        index_page = AnonymIndexPage(
            slug="tests-anonym-index-page",
            title="Tests Anonym Index Page",
        )
        root_page.add_child(instance=index_page)
        index_page.save_revision().publish()

    return index_page


def get_test_person() -> Person:
    """Get or create a test Person snippet for fixture tests.

    Returns:
        Person instance for use in tests
    """
    placeholder_image = get_placeholder_image()

    person, _ = Person.objects.get_or_create(
        name="Test Person",
        defaults={
            "image": placeholder_image,
            "position": "Test Position",
            "description": "<p>Test description for this person.</p>",
            "learn_more_link": "https://example.com/person",
        },
    )
    return person
