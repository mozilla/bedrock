# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from wagtail.models import Site

from bedrock.anonym.models import AnonymIndexPage


def get_test_anonym_index_page():
    site = Site.objects.get(is_default_site=True)
    root_page = site.root_page
    anonym_index_page = AnonymIndexPage.objects.filter(slug="tests-anonym-index-page").first()
    if not anonym_index_page:
        anonym_index_page = AnonymIndexPage(
            slug="tests-anonym-index-page",
            title="Tests Anonym Index Page",
        )
        root_page.add_child(instance=anonym_index_page)
        anonym_index_page.save_revision().publish()
    return anonym_index_page


@pytest.fixture
def anonym_index_page():
    return get_test_anonym_index_page()
