# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from wagtail.rich_text import RichText

from bedrock.cms.tests.conftest import minimal_site  # noqa: F401, F811
from bedrock.mozorg.tests import factories

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_leadership_page(minimal_site, rf, serving_method):  # noqa
    root_page = minimal_site.root_page

    leadership_page = factories.LeadershipPageFactory(
        parent=root_page,
        leadership_sections__0__section__title="Test Section Title",
        leadership_sections__0__section__leadership_group__0__title="Test Leadership Group Title",
        leadership_sections__0__section__leadership_group__0__leaders__0__name="Test Name",
        leadership_sections__0__section__leadership_group__0__leaders__0__headshot=factories.LeadershipHeadshotBlockFactory(
            image_alt_text="Text Alt Text",
            photos_link="https://example.com/photos.zip",
        ),
        leadership_sections__0__section__leadership_group__0__leaders__0__job_title="Test Job Title",
        leadership_sections__0__section__leadership_group__0__leaders__0__biography=RichText("Test Biography"),
        leadership_sections__0__section__leadership_group__0__leaders__0__external_links__0__url="https://example.com",
        leadership_sections__0__section__leadership_group__0__leaders__0__external_links__0__type="Website",
        leadership_sections__0__section__leadership_group__0__leaders__0__external_links__0__text="Test Blog link",
    )

    leadership_page.save()

    _relative_url = leadership_page.relative_url(minimal_site)
    assert _relative_url == "/en-US/leadership/"  # Note: not the real site URL just for testing.
    request = rf.get(_relative_url)

    resp = getattr(leadership_page, serving_method)(request)
    page_content = resp.text
    assert "Test Section Title" in page_content
    assert "Test Leadership Group" in page_content
    assert "Test Name" in page_content
    assert 'alt="Text Alt Text"' in page_content
    assert "Test Blog link" and 'href="https://example.com"' in page_content
    assert 'href="https://example.com/photos.zip"' in page_content
    assert "Test Job Title" in page_content
    assert "Test Biography" in page_content
