# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Tests for Protocol m24 component blocks using fixture-based testing.

This module tests that Wagtail blocks render correctly by:
1. Creating test pages with block variants via fixtures
2. Serving the pages and parsing the HTML with BeautifulSoup
3. Asserting that rendered output matches expected structure and content
"""

import pytest
from bs4 import BeautifulSoup

from bedrock.cms.tests.conftest import minimal_site  # noqa: F401
from bedrock.mozorg.fixtures.base_fixtures import get_placeholder_image
from bedrock.mozorg.fixtures.donate_fixtures import get_donate_test_page, get_donate_variants

pytestmark = [pytest.mark.django_db]


def assert_donate_block_structure(donate_element: BeautifulSoup):
    """Verify the donate block has the expected HTML structure.

    Args:
        donate_element: BeautifulSoup element for the .m24-c-donate div
    """
    # Check required child elements exist
    heading = donate_element.find(class_="m24-c-donate-heading")
    assert heading is not None, "Missing .m24-c-donate-heading element"

    body = donate_element.find(class_="m24-c-donate-body")
    assert body is not None, "Missing .m24-c-donate-body element"

    media = donate_element.find(class_="m24-c-donate-media")
    assert media is not None, "Missing .m24-c-donate-media element"

    cta = donate_element.find(class_="m24-c-donate-cta")
    assert cta is not None, "Missing .m24-c-donate-cta element"

    # Check CTA has a link
    cta_link = cta.find("a", class_="m24-c-cta")
    assert cta_link is not None, "Missing .m24-c-cta link in CTA"


def assert_donate_block_content(donate_element: BeautifulSoup, variant_data: dict):
    """Verify the donate block content matches the input data.

    Args:
        donate_element: BeautifulSoup element for the .m24-c-donate div
        variant_data: The block data dictionary used to create the block
    """
    value = variant_data["value"]

    # Check heading text
    heading = donate_element.find(class_="m24-c-donate-heading")
    assert value["heading"] in heading.get_text(), f"Heading text '{value['heading']}' not found"

    # Check heading is h2 by default
    assert heading.name == "h2", f"Expected h2 heading, got {heading.name}"

    # Check body contains expected content (strip HTML tags for comparison)
    body = donate_element.find(class_="m24-c-donate-body")
    body_text = body.get_text()
    # Extract text from the body HTML for comparison
    expected_body = BeautifulSoup(value["body"], "html.parser").get_text()
    assert expected_body in body_text, f"Body text not found. Expected '{expected_body}' in '{body_text}'"

    # Check CTA link
    cta_link = donate_element.find("a", class_="m24-c-cta")
    assert cta_link is not None, "CTA link not found"

    # Check CTA text
    assert value["cta_text"] in cta_link.get_text(), f"CTA text '{value['cta_text']}' not found"

    # Check CTA href (may have UTM parameters appended for Mozilla properties)
    expected_url = value["cta_link"]["custom_url"]
    assert cta_link["href"].startswith(expected_url.rstrip("/")), f"Expected href to start with '{expected_url}', got '{cta_link['href']}'"

    # Check data-cta-text attribute exists (slugified version of cta_text)
    assert "data-cta-text" in cta_link.attrs, "Missing data-cta-text attribute"
    assert cta_link["data-cta-text"], "data-cta-text attribute is empty"


def assert_donate_block_attributes(wrapper_element: BeautifulSoup, variant_data: dict):
    """Verify the donate block wrapper has correct attributes.

    Args:
        wrapper_element: BeautifulSoup element for the wrapper div (parent of .m24-c-donate)
        variant_data: The block data dictionary used to create the block
    """
    value = variant_data["value"]
    settings = value["settings"]

    # Check background color class
    bg_color = settings["background_color"] or "m24-t-gray"
    expected_class = bg_color
    assert expected_class in wrapper_element.get("class", []), f"Expected class '{expected_class}' not found"

    # Check anchor ID if set
    anchor_id = settings["anchor_id"]
    if anchor_id:
        assert wrapper_element.get("id") == anchor_id, f"Expected id '{anchor_id}', got '{wrapper_element.get('id')}'"

    # Check new_window attributes on CTA
    cta_link = wrapper_element.find("a", class_="m24-c-cta")
    if value["cta_link"].get("new_window"):
        assert cta_link.get("target") == "_blank", "Expected target='_blank' for new_window=True"
        assert "noopener" in cta_link.get("rel", []), "Expected 'noopener' in rel for new_window=True"
        assert "external" in cta_link.get("rel", []), "Expected 'external' in rel for new_window=True"
    else:
        assert cta_link.get("target") is None, "Expected no target attribute for new_window=False"


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_donate_block_renders(minimal_site, rf, serving_method):  # noqa: F811
    """Test that DonateBlock renders with correct structure."""
    # Get placeholder image and create test page
    placeholder_image = get_placeholder_image()
    variants = get_donate_variants(placeholder_image.id)
    test_page = get_donate_test_page()

    # Serve the page
    _relative_url = test_page.relative_url(minimal_site)
    request = rf.get(_relative_url)
    response = getattr(test_page, serving_method)(request)

    assert response.status_code == 200

    # Parse the HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all donate blocks
    donate_divs = soup.find_all("div", class_="m24-c-donate")
    assert len(donate_divs) == len(variants), f"Expected {len(variants)} donate blocks, found {len(donate_divs)}"

    # Check each block has correct structure
    for donate_div in donate_divs:
        assert_donate_block_structure(donate_div)


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_donate_block_content(minimal_site, rf, serving_method):  # noqa: F811
    """Test that DonateBlock content matches input data."""
    placeholder_image = get_placeholder_image()
    variants = get_donate_variants(placeholder_image.id)
    test_page = get_donate_test_page()

    _relative_url = test_page.relative_url(minimal_site)
    request = rf.get(_relative_url)
    response = getattr(test_page, serving_method)(request)

    soup = BeautifulSoup(response.content, "html.parser")
    donate_divs = soup.find_all("div", class_="m24-c-donate")

    for index, variant in enumerate(variants):
        assert_donate_block_content(donate_divs[index], variant)


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_donate_block_wrapper_attributes(minimal_site, rf, serving_method):  # noqa: F811
    """Test that DonateBlock wrapper has correct background color and anchor ID."""
    placeholder_image = get_placeholder_image()
    variants = get_donate_variants(placeholder_image.id)
    test_page = get_donate_test_page()

    _relative_url = test_page.relative_url(minimal_site)
    request = rf.get(_relative_url)
    response = getattr(test_page, serving_method)(request)

    soup = BeautifulSoup(response.content, "html.parser")

    # Find wrapper divs (parent of .m24-c-donate with m24-t-* class)
    for index, variant in enumerate(variants):
        bg_color = variant["value"]["settings"]["background_color"] or "m24-t-gray"
        wrapper_class = bg_color

        # Find the wrapper by its background color class
        wrapper = soup.find("div", class_=wrapper_class)
        assert wrapper is not None, f"Wrapper with class '{wrapper_class}' not found for variant {index}"

        assert_donate_block_attributes(wrapper, variant)


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_donate_block_new_window(minimal_site, rf, serving_method):  # noqa: F811
    """Test that new_window=True adds correct link attributes."""
    placeholder_image = get_placeholder_image()
    variants = get_donate_variants(placeholder_image.id)
    test_page = get_donate_test_page()

    _relative_url = test_page.relative_url(minimal_site)
    request = rf.get(_relative_url)
    response = getattr(test_page, serving_method)(request)

    soup = BeautifulSoup(response.content, "html.parser")

    # Find the variant with new_window=True (variant 4)
    new_window_variant = next(v for v in variants if v["value"]["cta_link"].get("new_window"))
    expected_cta_text = new_window_variant["value"]["cta_text"]

    # Find the link by its CTA text (href may have UTM parameters appended)
    cta_links = soup.find_all("a", class_="m24-c-cta")
    cta_link = next((link for link in cta_links if expected_cta_text in link.get_text()), None)
    assert cta_link is not None, f"CTA link with text '{expected_cta_text}' not found"

    assert cta_link.get("target") == "_blank", "Expected target='_blank'"
    assert "noopener" in cta_link.get("rel", []), "Expected 'noopener' in rel"
    assert "external" in cta_link.get("rel", []), "Expected 'external' in rel"
