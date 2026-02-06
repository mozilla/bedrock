# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test import RequestFactory

import pytest
from bs4 import BeautifulSoup
from wagtail.models import Site

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
    Person,
)
from bedrock.cms.tests.conftest import minimal_site  # noqa: F401

pytestmark = [
    pytest.mark.django_db,
]


def get_text_from_html(html_string: str) -> str:
    """Extract plain text from an HTML string.

    Args:
        html_string: HTML content string

    Returns:
        Plain text with HTML tags stripped
    """
    soup = BeautifulSoup(html_string, "html.parser")
    return soup.get_text()


# ============================================================================
# Person Snippet Tests
# ============================================================================


def test_person_snippet_creation() -> None:
    """Test that a Person snippet can be created."""
    image = get_placeholder_image()
    person = Person.objects.create(
        name="John Doe",
        position="Software Engineer",
        description="<p>A software engineer.</p>",
        image=image,
    )
    assert person.id is not None
    assert person.name == "John Doe"
    assert person.position == "Software Engineer"


def test_person_snippet_str() -> None:
    """Test the string representation of a Person snippet."""
    person = get_test_person()
    assert str(person) == f"{person.name} - {person.position}"


# ============================================================================
# AnonymIndexPage Tests
# ============================================================================


def test_anonym_index_page_creation(minimal_site: Site) -> None:  # noqa: F811
    """Test that an AnonymIndexPage can be created."""
    root_page = minimal_site.root_page
    page = AnonymIndexPage(
        title="Anonym Home",
        slug="anonym-home",
    )
    root_page.add_child(instance=page)
    page.save_revision().publish()

    assert page.id is not None
    assert page.title == "Anonym Home"
    assert page.live is True


def test_anonym_index_page_get_available_sections(minimal_site: Site) -> None:  # noqa: F811
    """Test that get_available_sections returns anchor IDs from content blocks."""
    root_page = minimal_site.root_page
    image = get_placeholder_image()
    person = get_test_person()

    section_variants = get_section_block_variants(image.id, person.id)
    cta_variants = get_call_to_action_variants()

    page = AnonymIndexPage(
        title="Anonym Home",
        slug="anonym-home-sections",
        content=section_variants[:2] + cta_variants[:1],
    )
    root_page.add_child(instance=page)
    page.save_revision().publish()

    sections = page.get_available_sections()
    # Sections should include anchor IDs from content blocks - derive expected from fixture data
    expected_sections = {
        section_variants[0]["value"]["settings"]["anchor_id"],
        section_variants[1]["value"]["settings"]["anchor_id"],
        cta_variants[0]["value"]["settings"]["anchor_id"],
    }
    assert set(sections) == expected_sections


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_anonym_index_page_serve(
    minimal_site: Site,  # noqa: F811
    rf: RequestFactory,
    serving_method: str,
) -> None:
    """Test that AnonymIndexPage can be served."""
    root_page = minimal_site.root_page
    image = get_placeholder_image()
    person = get_test_person()

    section_variants = get_section_block_variants(image.id, person.id)
    # Use only the first two nav links (overview, features) that match section anchor IDs
    nav_variants = get_navigation_link_variants()[:2]

    page = AnonymIndexPage(
        title="Anonym Index",
        slug="anonym-index-serve",
        navigation=nav_variants,
        # Include sections with anchor IDs that match navigation (overview, features)
        content=section_variants[:2],
    )
    root_page.add_child(instance=page)
    page.save_revision().publish()

    _relative_url = page.relative_url(minimal_site)
    request = rf.get(_relative_url)

    resp = getattr(page, serving_method)(request)
    page_content = resp.text

    assert "Anonym Index" in page_content
    # The heading_text from fixtures contains HTML; parse the page to extract just the text
    page_soup = BeautifulSoup(page_content, "html.parser")
    page_text = page_soup.get_text()
    expected_heading_text = get_text_from_html(section_variants[0]["value"]["heading_text"])
    assert expected_heading_text in page_text


# ============================================================================
# AnonymContentSubPage Tests
# ============================================================================


def test_anonym_content_sub_page_creation(minimal_site: Site) -> None:  # noqa: F811
    """Test that an AnonymContentSubPage can be created."""
    index_page = get_test_anonym_index_page()

    page = AnonymContentSubPage(
        title="Content Sub Test",
        slug="content-sub-test",
    )
    index_page.add_child(instance=page)
    page.save_revision().publish()

    assert page.id is not None
    assert page.title == "Content Sub Test"


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_anonym_content_sub_page_serve(
    minimal_site: Site,  # noqa: F811
    rf: RequestFactory,
    serving_method: str,
) -> None:
    """Test that AnonymContentSubPage can be served."""
    index_page = get_test_anonym_index_page()
    image = get_placeholder_image()
    person = get_test_person()

    section_variants = get_section_block_variants(image.id, person.id)
    toggleable_variants = get_toggleable_items_variants(image.id, person.id)

    page = AnonymContentSubPage(
        title="Content Sub Serve Test",
        slug="content-sub-serve-test",
        content=section_variants[:1] + toggleable_variants[:1],
    )
    index_page.add_child(instance=page)
    page.save_revision().publish()

    _relative_url = page.relative_url(minimal_site)
    request = rf.get(_relative_url)

    resp = getattr(page, serving_method)(request)
    page_content = resp.text

    assert "Content Sub Serve Test" in page_content


# ============================================================================
# AnonymNewsPage Tests
# ============================================================================


def test_anonym_news_page_creation(minimal_site: Site) -> None:  # noqa: F811
    """Test that an AnonymNewsPage can be created."""
    index_page = get_test_anonym_index_page()

    page = AnonymNewsPage(
        title="News Test",
        slug="news-test",
    )
    index_page.add_child(instance=page)
    page.save_revision().publish()

    assert page.id is not None
    assert page.title == "News Test"


# ============================================================================
# AnonymNewsItemPage Tests
# ============================================================================


def test_anonym_news_item_page_creation(minimal_site: Site) -> None:  # noqa: F811
    """Test that an AnonymNewsItemPage can be created."""
    index_page = get_test_anonym_index_page()
    news_page = AnonymNewsPage(
        title="News Container",
        slug="news-container-test",
    )
    index_page.add_child(instance=news_page)
    news_page.save_revision().publish()

    image = get_placeholder_image()

    page = AnonymNewsItemPage(
        title="News Item Test",
        slug="news-item-test",
        description="A test news item",
        category="Press",
        logo=image,
        image=image,
    )
    news_page.add_child(instance=page)
    page.save_revision().publish()

    assert page.id is not None
    assert page.title == "News Item Test"
    assert page.category == "Press"


def test_anonym_news_item_page_exclude_from_sitemap(minimal_site: Site) -> None:  # noqa: F811
    """Test that AnonymNewsItemPage excludes from sitemap when external link is set."""
    index_page = get_test_anonym_index_page()
    news_page = AnonymNewsPage(
        title="News Container",
        slug="news-container-sitemap-test",
    )
    index_page.add_child(instance=news_page)
    news_page.save_revision().publish()

    # Page without external link should be in sitemap
    page_internal = AnonymNewsItemPage(
        title="Internal News",
        slug="internal-news-test",
        link="",
    )
    news_page.add_child(instance=page_internal)
    page_internal.save_revision().publish()
    assert page_internal.exclude_from_sitemap is False

    # Page with external link should be excluded from sitemap
    page_external = AnonymNewsItemPage(
        title="External News",
        slug="external-news-test",
        link="https://example.com/external",
    )
    news_page.add_child(instance=page_external)
    page_external.save_revision().publish()
    assert page_external.exclude_from_sitemap is True


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_anonym_news_item_page_serve(
    minimal_site: Site,  # noqa: F811
    rf: RequestFactory,
    serving_method: str,
) -> None:
    """Test that AnonymNewsItemPage can be served."""
    index_page = get_test_anonym_index_page()
    news_page = AnonymNewsPage(
        title="News Container",
        slug="news-container-serve-test",
    )
    index_page.add_child(instance=news_page)
    news_page.save_revision().publish()

    image = get_placeholder_image()
    person = get_test_person()
    section_variants = get_section_block_variants(image.id, person.id)
    stat_variants = get_stat_item_variants()

    page = AnonymNewsItemPage(
        title="News Item Serve Test",
        slug="news-item-serve-test",
        description="Testing news item serving",
        category="Blog",
        logo=image,
        image=image,
        stats=stat_variants[:2],
        content=section_variants[:1],
    )
    news_page.add_child(instance=page)
    page.save_revision().publish()

    _relative_url = page.relative_url(minimal_site)
    request = rf.get(_relative_url)

    resp = getattr(page, serving_method)(request)
    page_content = resp.text

    assert "News Item Serve Test" in page_content


def test_anonym_news_page_get_context_featured(minimal_site: Site, rf: RequestFactory) -> None:  # noqa: F811
    """Test that AnonymNewsPage.get_context selects the most recent featured item."""
    index_page = get_test_anonym_index_page()
    news_page = AnonymNewsPage(
        title="News Container",
        slug="news-container-context-test",
    )
    index_page.add_child(instance=news_page)
    news_page.save_revision().publish()

    # Create three news items — only the middle one is featured
    item_a = AnonymNewsItemPage(title="Item A", slug="item-a")
    news_page.add_child(instance=item_a)
    item_a.save_revision().publish()

    item_b = AnonymNewsItemPage(title="Item B", slug="item-b", is_featured=True)
    news_page.add_child(instance=item_b)
    item_b.save_revision().publish()

    item_c = AnonymNewsItemPage(title="Item C", slug="item-c")
    news_page.add_child(instance=item_c)
    item_c.save_revision().publish()

    request = rf.get("/")
    context = news_page.get_context(request)

    assert context["featured_item"].pk == item_b.pk
    nonfeatured_pks = set(context["nonfeatured_items"].values_list("pk", flat=True))
    assert nonfeatured_pks == {item_a.pk, item_c.pk}


def test_anonym_news_page_get_context_no_featured(minimal_site: Site, rf: RequestFactory) -> None:  # noqa: F811
    """Test that get_context returns no featured item when none is marked."""
    index_page = get_test_anonym_index_page()
    news_page = AnonymNewsPage(
        title="News Container",
        slug="news-container-no-featured-test",
    )
    index_page.add_child(instance=news_page)
    news_page.save_revision().publish()

    item_a = AnonymNewsItemPage(title="Item A", slug="item-a-nf")
    news_page.add_child(instance=item_a)
    item_a.save_revision().publish()

    item_b = AnonymNewsItemPage(title="Item B", slug="item-b-nf")
    news_page.add_child(instance=item_b)
    item_b.save_revision().publish()

    request = rf.get("/")
    context = news_page.get_context(request)

    assert context["featured_item"] is None
    nonfeatured_pks = set(context["nonfeatured_items"].values_list("pk", flat=True))
    assert nonfeatured_pks == {item_a.pk, item_b.pk}


def test_anonym_news_page_get_context_multiple_featured(minimal_site: Site, rf: RequestFactory) -> None:  # noqa: F811
    """Test that only the most recent featured item is selected when multiple are marked."""
    index_page = get_test_anonym_index_page()
    news_page = AnonymNewsPage(
        title="News Container",
        slug="news-container-multi-featured-test",
    )
    index_page.add_child(instance=news_page)
    news_page.save_revision().publish()

    # Create three featured items — the most recently published should win
    item_a = AnonymNewsItemPage(title="Item A", slug="item-a-mf", is_featured=True)
    news_page.add_child(instance=item_a)
    item_a.save_revision().publish()

    item_b = AnonymNewsItemPage(title="Item B", slug="item-b-mf", is_featured=True)
    news_page.add_child(instance=item_b)
    item_b.save_revision().publish()

    item_c = AnonymNewsItemPage(title="Item C", slug="item-c-mf", is_featured=True)
    news_page.add_child(instance=item_c)
    item_c.save_revision().publish()

    request = rf.get("/")
    context = news_page.get_context(request)

    # Most recently published featured item is selected
    assert context["featured_item"].pk == item_c.pk
    nonfeatured_pks = set(context["nonfeatured_items"].values_list("pk", flat=True))
    assert nonfeatured_pks == {item_a.pk, item_b.pk}


# ============================================================================
# AnonymCaseStudyPage Tests
# ============================================================================


def test_anonym_case_study_page_creation(minimal_site: Site) -> None:  # noqa: F811
    """Test that an AnonymCaseStudyPage can be created."""
    index_page = get_test_anonym_index_page()

    page = AnonymCaseStudyPage(
        title="Case Study Test",
        slug="case-study-test",
    )
    index_page.add_child(instance=page)
    page.save_revision().publish()

    assert page.id is not None
    assert page.title == "Case Study Test"


# ============================================================================
# AnonymCaseStudyItemPage Tests
# ============================================================================


def test_anonym_case_study_item_page_creation(minimal_site: Site) -> None:  # noqa: F811
    """Test that an AnonymCaseStudyItemPage can be created."""
    index_page = get_test_anonym_index_page()
    case_study_page = AnonymCaseStudyPage(
        title="Case Study Container",
        slug="case-study-container-test",
    )
    index_page.add_child(instance=case_study_page)
    case_study_page.save_revision().publish()

    image = get_placeholder_image()

    page = AnonymCaseStudyItemPage(
        title="Case Study Item Test",
        slug="case-study-item-test",
        company_name="Test Client",
        description="A test case study",
        logo=image,
    )
    case_study_page.add_child(instance=page)
    page.save_revision().publish()

    assert page.id is not None
    assert page.title == "Case Study Item Test"
    assert page.company_name == "Test Client"


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_anonym_case_study_item_page_serve(
    minimal_site: Site,  # noqa: F811
    rf: RequestFactory,
    serving_method: str,
) -> None:
    """Test that AnonymCaseStudyItemPage can be served."""
    index_page = get_test_anonym_index_page()
    case_study_page = AnonymCaseStudyPage(
        title="Case Study Container",
        slug="case-study-container-serve-test",
    )
    index_page.add_child(instance=case_study_page)
    case_study_page.save_revision().publish()

    image = get_placeholder_image()
    person = get_test_person()
    section_variants = get_section_block_variants(image.id, person.id)

    page = AnonymCaseStudyItemPage(
        title="Case Study Item Serve Test",
        slug="case-study-item-serve-test",
        company_name="Acme Corp",
        description="Testing case study item serving",
        logo=image,
        content=section_variants[:1],
    )
    case_study_page.add_child(instance=page)
    page.save_revision().publish()

    _relative_url = page.relative_url(minimal_site)
    request = rf.get(_relative_url)

    resp = getattr(page, serving_method)(request)
    page_content = resp.text

    assert "Case Study Item Serve Test" in page_content


# ============================================================================
# AnonymContactPage Tests
# ============================================================================


def test_anonym_contact_page_creation(minimal_site: Site) -> None:  # noqa: F811
    """Test that an AnonymContactPage can be created."""
    index_page = get_test_anonym_index_page()

    page = AnonymContactPage(
        title="Contact Test",
        slug="contact-test",
        subheading="Get in touch",
    )
    index_page.add_child(instance=page)
    page.save_revision().publish()

    assert page.id is not None
    assert page.title == "Contact Test"
    assert page.subheading == "Get in touch"


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_anonym_contact_page_serve(
    minimal_site: Site,  # noqa: F811
    rf: RequestFactory,
    serving_method: str,
) -> None:
    """Test that AnonymContactPage can be served."""
    index_page = get_test_anonym_index_page()
    form_field_variants = get_form_field_variants()

    page = AnonymContactPage(
        title="Contact Serve Test",
        slug="contact-serve-test",
        subheading="Contact us today",
        form_fields=form_field_variants[:3],
    )
    index_page.add_child(instance=page)
    page.save_revision().publish()

    _relative_url = page.relative_url(minimal_site)
    request = rf.get(_relative_url)

    resp = getattr(page, serving_method)(request)
    page_content = resp.text

    assert "Contact Serve Test" in page_content
    # Verify form field labels from fixture data
    assert form_field_variants[0]["value"]["label"] in page_content
    assert form_field_variants[2]["value"]["label"] in page_content
