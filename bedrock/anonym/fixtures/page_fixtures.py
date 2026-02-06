# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Page fixture creators for Anonym test data.

Each function creates or updates a test page with appropriate content blocks.
"""

from bedrock.anonym.fixtures.base_fixtures import (
    get_placeholder_image,
    get_test_anonym_index_page,
    get_test_person,
)
from bedrock.anonym.fixtures.block_fixtures import (
    get_call_to_action_variants,
    get_form_field_variants,
    get_navigation_link_variants,
    get_section_block_variants,
    get_stat_item_variants,
    get_toggleable_items_variants,
)
from bedrock.anonym.models import (
    AnonymCaseStudyItemPage,
    AnonymCaseStudyPage,
    AnonymContactPage,
    AnonymContentSubPage,
    AnonymIndexPage,
    AnonymNewsItemPage,
    AnonymNewsPage,
)


def get_anonym_index_test_page() -> AnonymIndexPage:
    """Get or create a test AnonymIndexPage with content.

    Returns:
        AnonymIndexPage instance with navigation and content blocks
    """
    placeholder_image = get_placeholder_image()
    person = get_test_person()

    index_page = get_test_anonym_index_page()

    # Update with content
    section_variants = get_section_block_variants(placeholder_image.id, person.id)
    cta_variants = get_call_to_action_variants()

    index_page.navigation = get_navigation_link_variants()
    index_page.content = section_variants[:2] + cta_variants[:1]
    index_page.save_revision().publish()

    return index_page


def get_anonym_content_sub_test_page() -> AnonymContentSubPage:
    """Get or create a test AnonymContentSubPage with content.

    Returns:
        AnonymContentSubPage instance with toggleable content
    """
    placeholder_image = get_placeholder_image()
    person = get_test_person()
    index_page = get_test_anonym_index_page()

    test_page = AnonymContentSubPage.objects.filter(slug="test-content-sub-page").first()
    if not test_page:
        test_page = AnonymContentSubPage(
            slug="test-content-sub-page",
            title="Test Content Sub Page",
        )
        index_page.add_child(instance=test_page)

    section_variants = get_section_block_variants(placeholder_image.id, person.id)
    toggleable_variants = get_toggleable_items_variants(placeholder_image.id, person.id)
    cta_variants = get_call_to_action_variants()

    test_page.content = section_variants[:1] + toggleable_variants[:1] + cta_variants[:1]
    test_page.save_revision().publish()

    return test_page


def get_anonym_news_test_page() -> AnonymNewsPage:
    """Get or create a test AnonymNewsPage.

    Returns:
        AnonymNewsPage instance
    """
    index_page = get_test_anonym_index_page()

    test_page = AnonymNewsPage.objects.filter(slug="test-news-page").first()
    if not test_page:
        test_page = AnonymNewsPage(
            slug="test-news-page",
            title="Test News Page",
        )
        index_page.add_child(instance=test_page)
        test_page.save_revision().publish()

    return test_page


def get_anonym_news_item_test_page(
    news_page: AnonymNewsPage = None,
    slug: str = "test-news-item-page",
    title: str = "Test News Item Page",
    with_external_link: bool = False,
) -> AnonymNewsItemPage:
    """Get or create a test AnonymNewsItemPage with content.

    Args:
        news_page: Parent AnonymNewsPage (creates one if not provided)
        slug: Page slug
        title: Page title
        with_external_link: If True, sets an external link (excludes from sitemap)

    Returns:
        AnonymNewsItemPage instance with content
    """
    placeholder_image = get_placeholder_image()
    person = get_test_person()

    if not news_page:
        news_page = get_anonym_news_test_page()

    test_page = AnonymNewsItemPage.objects.filter(slug=slug).first()
    if not test_page:
        test_page = AnonymNewsItemPage(
            slug=slug,
            title=title,
        )
        news_page.add_child(instance=test_page)

    section_variants = get_section_block_variants(placeholder_image.id, person.id)
    cta_variants = get_call_to_action_variants()
    stat_variants = get_stat_item_variants()

    test_page.description = "This is a test news item with detailed content."
    test_page.category = "Press"
    test_page.logo = placeholder_image
    test_page.image = placeholder_image
    test_page.link = "https://example.com/external-news" if with_external_link else ""
    test_page.stats = stat_variants[:2]
    test_page.content = section_variants[:1] + cta_variants[:1]
    test_page.save_revision().publish()

    return test_page


def get_anonym_case_study_test_page() -> AnonymCaseStudyPage:
    """Get or create a test AnonymCaseStudyPage.

    Returns:
        AnonymCaseStudyPage instance
    """
    index_page = get_test_anonym_index_page()

    test_page = AnonymCaseStudyPage.objects.filter(slug="test-case-study-page").first()
    if not test_page:
        test_page = AnonymCaseStudyPage(
            slug="test-case-study-page",
            title="Test Case Study Page",
        )
        index_page.add_child(instance=test_page)
        test_page.save_revision().publish()

    return test_page


def get_anonym_case_study_item_test_page(
    case_study_page: AnonymCaseStudyPage = None,
    slug: str = "test-case-study-item-page",
    title: str = "Test Case Study Item Page",
) -> AnonymCaseStudyItemPage:
    """Get or create a test AnonymCaseStudyItemPage with content.

    Args:
        case_study_page: Parent AnonymCaseStudyPage (creates one if not provided)
        slug: Page slug
        title: Page title

    Returns:
        AnonymCaseStudyItemPage instance with content
    """
    placeholder_image = get_placeholder_image()
    person = get_test_person()

    if not case_study_page:
        case_study_page = get_anonym_case_study_test_page()

    test_page = AnonymCaseStudyItemPage.objects.filter(slug=slug).first()
    if not test_page:
        test_page = AnonymCaseStudyItemPage(
            slug=slug,
            title=title,
        )
        case_study_page.add_child(instance=test_page)

    section_variants = get_section_block_variants(placeholder_image.id, person.id)
    cta_variants = get_call_to_action_variants()

    test_page.logo = placeholder_image
    test_page.client = "Test Client Company"
    test_page.description = "A comprehensive case study demonstrating results."
    test_page.content = section_variants[:2] + cta_variants[:1]
    test_page.save_revision().publish()

    return test_page


def get_anonym_contact_test_page() -> AnonymContactPage:
    """Get or create a test AnonymContactPage with form fields.

    Returns:
        AnonymContactPage instance with form fields
    """
    index_page = get_test_anonym_index_page()

    test_page = AnonymContactPage.objects.filter(slug="test-contact-page").first()
    if not test_page:
        test_page = AnonymContactPage(
            slug="test-contact-page",
            title="Test Contact Page",
        )
        index_page.add_child(instance=test_page)

    form_field_variants = get_form_field_variants()

    test_page.subheading = "Get in touch with our team"
    test_page.form_fields = form_field_variants
    test_page.save_revision().publish()

    return test_page


def create_all_test_pages() -> dict:
    """Create all test pages for Anonym fixtures.

    Returns:
        Dictionary with all created test pages
    """
    # Create base fixtures
    placeholder_image = get_placeholder_image()
    person = get_test_person()

    # Create pages in order (respecting parent relationships)
    index_page = get_anonym_index_test_page()
    content_sub_page = get_anonym_content_sub_test_page()

    # News pages
    news_page = get_anonym_news_test_page()
    news_item_page_1 = get_anonym_news_item_test_page(
        news_page=news_page,
        slug="test-news-item-1",
        title="Test News Item 1",
    )
    news_item_page_2 = get_anonym_news_item_test_page(
        news_page=news_page,
        slug="test-news-item-2",
        title="Test News Item 2 (External)",
        with_external_link=True,
    )

    # Case study pages
    case_study_page = get_anonym_case_study_test_page()
    case_study_item_page_1 = get_anonym_case_study_item_test_page(
        case_study_page=case_study_page,
        slug="test-case-study-item-1",
        title="Test Case Study Item 1",
    )
    case_study_item_page_2 = get_anonym_case_study_item_test_page(
        case_study_page=case_study_page,
        slug="test-case-study-item-2",
        title="Test Case Study Item 2",
    )

    # Contact page
    contact_page = get_anonym_contact_test_page()

    return {
        "placeholder_image": placeholder_image,
        "person": person,
        "index_page": index_page,
        "content_sub_page": content_sub_page,
        "news_page": news_page,
        "news_item_pages": [news_item_page_1, news_item_page_2],
        "case_study_page": case_study_page,
        "case_study_item_pages": [case_study_item_page_1, case_study_item_page_2],
        "contact_page": contact_page,
    }
