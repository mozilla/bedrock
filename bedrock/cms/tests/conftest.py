# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
import wagtail_factories
from wagtail.models import Site

from bedrock.cms.tests.factories import LocaleFactory, SimpleRichTextPageFactory


@pytest.fixture
def minimal_site(
    client,
    top_level_page=None,
):
    # Bootstraps a minimal site with a root page at / and one child page at /test-page/

    if top_level_page is None:
        top_level_page = SimpleRichTextPageFactory(
            slug="root_page",  # this doesn't get shown
            live=True,
        )

    try:
        site = Site.objects.get(is_default_site=True)
        site.root_page = top_level_page
        site.hostname = client._base_environ()["SERVER_NAME"]
        site.save()
    except Site.DoesNotExist:
        site = wagtail_factories.SiteFactory(
            root_page=top_level_page,
            is_default_site=True,
            hostname=client._base_environ()["SERVER_NAME"],
        )

    LocaleFactory(language_code="fr")

    SimpleRichTextPageFactory(
        slug="test-page",
        parent=top_level_page,
        title="Test Page",
    )

    return site
