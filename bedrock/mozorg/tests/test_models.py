# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.exceptions import ValidationError

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


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_advertising_index_page(minimal_site, rf, serving_method):  # noqa
    root_page = minimal_site.root_page

    # Create a ContactBannerSnippet
    contact_banner = factories.ContactBannerSnippetFactory(
        heading="Contact Our Advertising Team",
        button_text="Contact Sales",
        button_link="https://example.com/contact-sales",
    )

    # Create a NitificationSnippet
    notification_snippet = factories.NotificationSnippetFactory(
        notification_text="Follow Mozilla Ads to get the latest secure advertising trends.",
        linkedin_link="https://www.linkedin.com/showcase/mozilla-ads/",
        bluesky_link="https://bsky.app/profile/mozilla_ads",
        instagram_link="https://www.instagram.com/mozilla_ads/",
        youtube_link="https://www.youtube.com/@mozilla_ads",
    )

    # Create the AdvertisingIndexPage with content blocks and contact banner
    advertising_page = factories.AdvertisingIndexPageFactory(
        parent=root_page,
        contact_banner=contact_banner,
        notification=notification_snippet,
        hero__0__advertising_hero_block=factories.AdvertisingHeroBlockFactory(
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
        sections__0__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id=""),
            header=factories.SectionHeaderBlockFactory(
                heading_text="Test Section Header",
                subheading_text="Test subheading",
            ),
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

    # Assert notification snippet text
    assert "Follow Mozilla Ads to get the latest secure advertising trends." in page_content


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_two_column_subpage(minimal_site, rf, serving_method):  # noqa
    root_page = minimal_site.root_page

    # Create an AdvertisingIndexPage as the parent
    advertising_page = factories.AdvertisingIndexPageFactory(
        parent=root_page,
    )
    advertising_page.save()

    # Build the second_column StreamBlock data for the AdvertisingTwoColumnSubpage
    list_item_heading_text = "Test List Item Heading"
    list_item_supporting_text = "Test list item supporting text"
    second_column_data = [
        (
            "list",
            {
                "list_items": [
                    {
                        "heading_text": list_item_heading_text,
                        "supporting_text": RichText(f"<p>{list_item_supporting_text}</p>"),
                    }
                ]
            },
        )
    ]

    # Create the AdvertisingTwoColumnSubpage with properly formatted StreamField data
    two_column_page = factories.AdvertisingTwoColumnSubpageFactory(
        parent=advertising_page,
        content=[
            (
                "two_column_block",
                {
                    "heading_text": "Test Heading",
                    "subheading": "Test Subheading",
                    "second_column": second_column_data,
                },
            )
        ],
    )

    two_column_page.save()

    _relative_url = two_column_page.relative_url(minimal_site)
    assert _relative_url == "/en-US/advertising/two-column-subpage/"
    request = rf.get(_relative_url)

    resp = getattr(two_column_page, serving_method)(request)
    page_content = resp.text

    # Assert page heading and subheading
    assert "Test Heading" in page_content
    assert "Test Subheading" in page_content

    # Assert content from the list item block
    assert list_item_heading_text in page_content
    assert list_item_supporting_text in page_content


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_advertising_index_page_sub_navigation(minimal_site, rf, serving_method):  # noqa
    root_page = minimal_site.root_page

    # Create a simple page to link to
    linked_page = factories.AdvertisingTwoColumnSubpageFactory(
        parent=root_page,
        title="Test Linked Page",
        slug="linked-page",
    )
    linked_page.save()

    # Create the AdvertisingIndexPage with sub-navigation and content with section IDs
    advertising_page = factories.AdvertisingIndexPageFactory(
        parent=root_page,
        # Add section block with anchor ID for anchor link testing
        sections__0__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id="test-section"),
            header=factories.SectionHeaderBlockFactory(
                heading_text="Test Section",
            ),
        ),
        # Custom URL link
        sub_navigation__0__link=factories.NavigationLinkBlockFactory(
            link_text="Custom URL Link",
            link=factories.LinkBlockFactory(
                link_to="custom_url",
                custom_url="https://example.com/custom",
            ),
        ),
        # Internal page link
        sub_navigation__1__link=factories.NavigationLinkBlockFactory(
            link_text="Internal Page Link",
            link=factories.LinkBlockFactory(
                link_to="page",
                page=linked_page,
                custom_url="",
                anchor="",
            ),
        ),
        # Anchor link
        sub_navigation__2__link=factories.NavigationLinkBlockFactory(
            link_text="Anchor Link",
            link=factories.LinkBlockFactory(
                link_to="anchor",
                anchor="test-section",
                custom_url="",
            ),
        ),
    )

    advertising_page.save()

    _relative_url = advertising_page.relative_url(minimal_site)
    assert _relative_url == "/en-US/advertising/"
    request = rf.get(_relative_url)

    resp = getattr(advertising_page, serving_method)(request)
    page_content = resp.text

    # Assert navigation link texts are present
    assert "Custom URL Link" in page_content
    assert "Internal Page Link" in page_content
    assert "Anchor Link" in page_content

    # Assert URLs are correctly resolved
    assert 'href="https://example.com/custom"' in page_content
    assert 'href="/en-US/linked-page/"' in page_content
    assert f'href="{advertising_page.url}#test-section"' in page_content


def test_advertising_index_page_duplicate_anchor_ids_in_settings(minimal_site):  # noqa
    """Test that duplicate anchor IDs in section settings raise ValidationError"""
    root_page = minimal_site.root_page

    # Build page without saving (use .build instead of create)
    advertising_page = factories.AdvertisingIndexPageFactory.build(
        parent=root_page,
        sections__0__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id="duplicate-id"),
            header=factories.SectionHeaderBlockFactory(heading_text="Section 1"),
        ),
        sections__1__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id="duplicate-id"),
            header=factories.SectionHeaderBlockFactory(heading_text="Section 2"),
        ),
    )

    # Should raise ValidationError on clean
    with pytest.raises(ValidationError) as exc_info:
        advertising_page.clean()

    assert "Duplicate anchor ID(s) found" in str(exc_info.value)
    assert "duplicate-id" in str(exc_info.value)


def test_advertising_index_page_duplicate_anchor_ids_across_hero_and_sections(
    minimal_site,  # noqa: F811
):
    """Test that duplicate anchor IDs between hero and sections raise ValidationError"""
    root_page = minimal_site.root_page

    # Build page without saving
    advertising_page = factories.AdvertisingIndexPageFactory.build(
        parent=root_page,
        hero__0__advertising_hero_block=factories.AdvertisingHeroBlockFactory(
            anchor_id="my-anchor",
            heading_text="Hero Section",
        ),
        sections__0__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id="my-anchor"),
            header=factories.SectionHeaderBlockFactory(heading_text="Section 1"),
        ),
    )

    # Should raise ValidationError on clean
    with pytest.raises(ValidationError) as exc_info:
        advertising_page.clean()

    assert "Duplicate anchor ID(s) found" in str(exc_info.value)
    assert "my-anchor" in str(exc_info.value)


def test_advertising_index_page_duplicate_anchor_ids_in_section_header(minimal_site):  # noqa
    """Test that duplicate anchor IDs in section headers raise ValidationError"""
    root_page = minimal_site.root_page

    # Build page without saving
    advertising_page = factories.AdvertisingIndexPageFactory.build(
        parent=root_page,
        sections__0__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id=""),
            header=factories.SectionHeaderBlockFactory(
                heading_text="Section 1",
                anchor_id="header-duplicate",
            ),
        ),
        sections__1__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id=""),
            header=factories.SectionHeaderBlockFactory(
                heading_text="Section 2",
                anchor_id="header-duplicate",
            ),
        ),
    )

    # Should raise ValidationError on clean
    with pytest.raises(ValidationError) as exc_info:
        advertising_page.clean()

    assert "Duplicate anchor ID(s) found" in str(exc_info.value)
    assert "header-duplicate" in str(exc_info.value)


def test_advertising_index_page_invalid_navigation_anchor_reference(minimal_site):  # noqa
    """Test that navigation links referencing non-existent anchors raise ValidationError"""
    root_page = minimal_site.root_page

    # Build page without saving
    advertising_page = factories.AdvertisingIndexPageFactory.build(
        parent=root_page,
        sections__0__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id="valid-section"),
            header=factories.SectionHeaderBlockFactory(heading_text="Valid Section"),
        ),
        sub_navigation__0__link=factories.NavigationLinkBlockFactory(
            link_text="Invalid Anchor Link",
            link=factories.LinkBlockFactory(
                link_to="anchor",
                anchor="non-existent-section",
                custom_url="",
            ),
        ),
    )

    # Should raise ValidationError on clean
    with pytest.raises(ValidationError) as exc_info:
        advertising_page.clean()

    assert "Navigation links reference unknown section(s)" in str(exc_info.value)
    assert "non-existent-section" in str(exc_info.value)


def test_advertising_index_page_valid_navigation_anchor_reference(minimal_site):  # noqa
    """Test that navigation links referencing valid anchors pass validation"""
    root_page = minimal_site.root_page

    # Create page with navigation link to valid anchor in section settings
    advertising_page = factories.AdvertisingIndexPageFactory(
        parent=root_page,
        sections__0__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id="valid-section"),
            header=factories.SectionHeaderBlockFactory(heading_text="Valid Section"),
        ),
        sub_navigation__0__link=factories.NavigationLinkBlockFactory(
            link_text="Valid Anchor Link",
            link=factories.LinkBlockFactory(
                link_to="anchor",
                anchor="valid-section",
                custom_url="",
            ),
        ),
    )

    # Should save successfully (clean is called automatically)
    assert advertising_page.id is not None
    # Should not raise ValidationError
    advertising_page.clean()  # No exception expected


def test_advertising_index_page_valid_navigation_anchor_reference_in_header(
    minimal_site,  # noqa: F811
):
    """Test that navigation links can reference anchors in section headers"""
    root_page = minimal_site.root_page

    # Create page with navigation link to valid anchor in section header
    advertising_page = factories.AdvertisingIndexPageFactory(
        parent=root_page,
        sections__0__section=factories.SectionBlockFactory(
            settings=factories.SectionSettingsFactory(anchor_id=""),
            header=factories.SectionHeaderBlockFactory(
                heading_text="Header Section",
                anchor_id="header-anchor",
            ),
        ),
        sub_navigation__0__link=factories.NavigationLinkBlockFactory(
            link_text="Header Anchor Link",
            link=factories.LinkBlockFactory(
                link_to="anchor",
                anchor="header-anchor",
                custom_url="",
            ),
        ),
    )

    # Should save successfully (clean is called automatically)
    assert advertising_page.id is not None
    # Should not raise ValidationError
    advertising_page.clean()  # No exception expected
