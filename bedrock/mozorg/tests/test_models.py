# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from wagtail.rich_text import RichText

from bedrock.cms.tests.conftest import minimal_site  # noqa
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


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_advertising_index_page(minimal_site, rf, serving_method):  # noqa
    root_page = minimal_site.root_page

    # Create a ContactBannerSnippet
    contact_banner = factories.ContactBannerSnippetFactory(
        heading="Contact Our Advertising Team",
        button_text="Contact Sales",
        button_link="https://example.com/contact-sales",
    )

    # Create the AdvertisingIndexPage with content blocks and contact banner
    advertising_page = factories.AdvertisingIndexPageFactory(
        parent=root_page,
        contact_banner=contact_banner,
        notifications__0__notification_block__notification_text=RichText("<p>Test notification text</p>"),
        notifications__0__notification_block__links__0__link_with_icon=factories.LinkWithIconFactory(
            icon="linkedin",
            link=factories.LinkBlockFactory(
                link_to="custom_url",
                custom_url="https://example.com/notification",
            ),
        ),
        content__0__advertising_hero_block=factories.AdvertisingHeroBlockFactory(
            heading_text="Test Hero Heading",
            primary_cta_text="Primary CTA",
            primary_cta_link=factories.LinkBlockFactory(
                link_to="custom_url",
                custom_url="https://example.com/primary",
            ),
            supporting_text="Test supporting text",
            secondary_cta_text="Secondary CTA",
            secondary_cta_link=factories.LinkBlockFactory(
                link_to="custom_url",
                custom_url="https://example.com/secondary",
            ),
        ),
        content__1__section_header_block=factories.SectionHeaderBlockFactory(
            heading_text="Test Section Header",
            subheading_text="Test subheading",
        ),
    )

    advertising_page.save()

    _relative_url = advertising_page.relative_url(minimal_site)
    assert _relative_url == "/en-US/advertising/"
    request = rf.get(_relative_url)

    resp = getattr(advertising_page, serving_method)(request)
    page_content = resp.text

    # Assert content from the hero block
    assert "Test Hero Heading" in page_content
    assert "Primary CTA" in page_content
    assert "Test supporting text" in page_content
    assert "Secondary CTA" in page_content

    # Assert content from the section header block
    assert "Test Section Header" in page_content
    assert "Test subheading" in page_content

    # Assert content from the contact banner snippet
    assert "Contact Our Advertising Team" in page_content
    assert "Contact Sales" in page_content
    assert "https://example.com/contact-sales" in page_content

    # Assert notification text
    assert "Test notification text" in page_content
