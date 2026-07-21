# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.management import call_command

import pytest
from wagtail.models import Site

from bedrock.anonym.fixtures.base_fixtures import get_test_anonym_index_page
from bedrock.anonym.models import (
    AnonymCaseStudyItemPage,
    AnonymCaseStudyPage,
    AnonymContentSubPage,
    AnonymIndexPage,
    AnonymNewsItemPage,
    AnonymNewsPage,
)
from bedrock.cms.tests.conftest import minimal_site  # noqa: F401

pytestmark = [pytest.mark.django_db]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _cta_block(anchor_id="cta", label="Contact"):
    """call_to_action block whose button settings.analytics_id is empty."""
    return {
        "type": "call_to_action",
        "value": {
            "settings": {"anchor_id": anchor_id},
            "heading": f"<p>{label}</p>",
            "button": [
                {
                    "type": "item",
                    "value": {
                        "label": label,
                        "link": {
                            "link_to": "custom_url",
                            "custom_url": "https://example.com",
                            "new_window": False,
                        },
                        "settings": {"analytics_id": ""},
                    },
                    "id": f"btn-{anchor_id}",
                }
            ],
        },
        "id": f"cta-{anchor_id}",
    }


def _section_block(anchor_id="s", label="Learn More"):
    """section block whose action link settings.analytics_id is empty."""
    return {
        "type": "section",
        "value": {
            "settings": {"anchor_id": anchor_id, "theme": ""},
            "superheading_text": "",
            "heading_text": "<p>Test</p>",
            "subheading_text": "",
            "section_content": [],
            "action": [
                {
                    "type": "item",
                    "value": {
                        "label": label,
                        "link": {
                            "link_to": "custom_url",
                            "custom_url": "https://example.com",
                            "new_window": False,
                        },
                        "settings": {"analytics_id": ""},
                    },
                    "id": f"action-{anchor_id}",
                }
            ],
        },
        "id": f"section-{anchor_id}",
    }


def _cs_section_block(case_study_pk, item_id="cs-item-uuid"):
    """section block with a case_study_item_list_block whose analytics_id is empty."""
    return {
        "type": "section",
        "value": {
            "settings": {"anchor_id": "cs", "theme": ""},
            "superheading_text": "",
            "heading_text": "<p>Case Studies</p>",
            "subheading_text": "",
            "section_content": [
                {
                    "type": "case_study_item_list_block",
                    "value": {
                        "case_study_items": [
                            {
                                "type": "item",
                                "value": {"page": case_study_pk, "analytics_id": ""},
                                "id": item_id,
                            }
                        ]
                    },
                    "id": "cs-list",
                }
            ],
            "action": [],
        },
        "id": "section-cs",
    }


def _nav_button_link(slug_suffix, has_button=True, analytics_id=None):
    """navigation link block, optionally with has_button_appearance and/or analytics_id."""
    value = {
        "link_text": "Contact",
        "link": {
            "link_to": "custom_url",
            "custom_url": "https://example.com/contact",
            "new_window": False,
        },
        "has_button_appearance": has_button,
    }
    if analytics_id is not None:
        value["analytics_id"] = analytics_id
    return {"type": "link", "value": value, "id": f"nav-{slug_suffix}"}


# ---------------------------------------------------------------------------
# populate_link_block_analytics_ids
# ---------------------------------------------------------------------------


def test_populate_link_block_analytics_ids_section_action(minimal_site: Site) -> None:  # noqa: F811
    """Injects settings.analytics_id into section.action links that are missing it."""
    root_page = minimal_site.root_page
    page = AnonymIndexPage(
        title="LBAI Section Test",
        slug="lbai-section-test",
        content=[_section_block("lbai-s")],
    )
    root_page.add_child(instance=page)
    page.save_revision().publish()
    # Confirm pre-condition: settings exists but analytics_id is not yet populated
    assert not list(page.content.raw_data)[0]["value"]["action"][0]["value"]["settings"].get("analytics_id")

    call_command("populate_link_block_analytics_ids")

    page.refresh_from_db()
    action_link = list(page.content.raw_data)[0]["value"]["action"][0]["value"]
    assert "settings" in action_link
    assert action_link["settings"].get("analytics_id")


def test_populate_link_block_analytics_ids_cta_button(minimal_site: Site) -> None:  # noqa: F811
    """Injects settings.analytics_id into call_to_action.button links that are missing it."""
    root_page = minimal_site.root_page
    page = AnonymIndexPage(
        title="LBAI CTA Test",
        slug="lbai-cta-test",
        content=[_cta_block("lbai-c")],
    )
    root_page.add_child(instance=page)
    page.save_revision().publish()
    # Confirm pre-condition: settings exists but analytics_id is not yet populated
    assert not list(page.content.raw_data)[0]["value"]["button"][0]["value"]["settings"].get("analytics_id")

    call_command("populate_link_block_analytics_ids")

    page.refresh_from_db()
    button = list(page.content.raw_data)[0]["value"]["button"][0]["value"]
    assert "settings" in button
    assert button["settings"].get("analytics_id")


def test_populate_link_block_analytics_ids_idempotent(minimal_site: Site) -> None:  # noqa: F811
    """Does not overwrite an existing analytics_id when the command is run again."""
    existing_uid = "fixed-uid-lbai-1234"
    root_page = minimal_site.root_page
    section = _section_block("lbai-idem")
    section["value"]["action"][0]["value"]["settings"] = {"analytics_id": existing_uid}
    page = AnonymIndexPage(
        title="LBAI Idempotent Test",
        slug="lbai-idem-test",
        content=[section],
    )
    root_page.add_child(instance=page)
    page.save_revision().publish()

    call_command("populate_link_block_analytics_ids")

    page.refresh_from_db()
    action_link = list(page.content.raw_data)[0]["value"]["action"][0]["value"]
    assert action_link["settings"]["analytics_id"] == existing_uid


def test_populate_link_block_analytics_ids_all_page_types(minimal_site: Site) -> None:  # noqa: F811
    """Processes AnonymIndexPage, AnonymContentSubPage, AnonymNewsItemPage, and AnonymCaseStudyItemPage."""
    index_page = get_test_anonym_index_page()
    cta = _cta_block("lbai-all")

    sub_page = AnonymContentSubPage(title="LBAI Sub", slug="lbai-all-sub", content=[cta])
    index_page.add_child(instance=sub_page)
    sub_page.save_revision().publish()

    news_page = AnonymNewsPage(title="LBAI News", slug="lbai-all-news")
    index_page.add_child(instance=news_page)
    news_page.save_revision().publish()
    news_item = AnonymNewsItemPage(title="LBAI News Item", slug="lbai-all-news-item", content=[cta])
    news_page.add_child(instance=news_item)
    news_item.save_revision().publish()

    cs_page = AnonymCaseStudyPage(title="LBAI CS", slug="lbai-all-cs")
    index_page.add_child(instance=cs_page)
    cs_page.save_revision().publish()
    cs_item = AnonymCaseStudyItemPage(title="LBAI CS Item", slug="lbai-all-cs-item", content=[cta])
    cs_page.add_child(instance=cs_item)
    cs_item.save_revision().publish()
    # Confirm pre-condition: settings exists but analytics_id is not yet populated on any page
    for page_obj in [sub_page, news_item, cs_item]:
        assert not list(page_obj.content.raw_data)[0]["value"]["button"][0]["value"]["settings"].get("analytics_id")

    call_command("populate_link_block_analytics_ids")

    for page_obj in [sub_page, news_item, cs_item]:
        page_obj.refresh_from_db()
        button = list(page_obj.content.raw_data)[0]["value"]["button"][0]["value"]
        assert "settings" in button
        assert button["settings"].get("analytics_id")


# ---------------------------------------------------------------------------
# populate_case_study_analytics_ids
# ---------------------------------------------------------------------------


def test_populate_case_study_analytics_ids_populates_empty_analytics_id(minimal_site: Site) -> None:  # noqa: F811
    """Fills in analytics_id for case_study_item_list_block items where it is empty."""
    index_page = get_test_anonym_index_page()

    cs_page = AnonymCaseStudyPage(title="PCSA CS", slug="pcsa-cs-page")
    index_page.add_child(instance=cs_page)
    cs_page.save_revision().publish()
    cs_item = AnonymCaseStudyItemPage(title="PCSA CS Item", slug="pcsa-cs-item")
    cs_page.add_child(instance=cs_item)
    cs_item.save_revision().publish()

    page = AnonymIndexPage(
        title="PCSA Index",
        slug="pcsa-index",
        content=[_cs_section_block(cs_item.pk)],
    )
    minimal_site.root_page.add_child(instance=page)
    page.save_revision().publish()
    # Confirm pre-condition: analytics_id exists but is not yet populated
    item_before = list(page.content.raw_data)[0]["value"]["section_content"][0]["value"]["case_study_items"][0]
    assert not item_before["value"].get("analytics_id")

    call_command("populate_case_study_analytics_ids")

    page.refresh_from_db()
    item_value = list(page.content.raw_data)[0]["value"]["section_content"][0]["value"]["case_study_items"][0]["value"]
    assert item_value["page"] == cs_item.pk
    assert item_value.get("analytics_id")


def test_populate_case_study_analytics_ids_idempotent(minimal_site: Site) -> None:  # noqa: F811
    """Does not overwrite an existing analytics_id when the item is already restructured."""
    existing_uid = "fixed-uid-pcsa-5678"
    index_page = get_test_anonym_index_page()

    cs_page = AnonymCaseStudyPage(title="PCSA CS Idem", slug="pcsa-idem-cs")
    index_page.add_child(instance=cs_page)
    cs_page.save_revision().publish()
    cs_item = AnonymCaseStudyItemPage(title="PCSA CS Item Idem", slug="pcsa-idem-cs-item")
    cs_page.add_child(instance=cs_item)
    cs_item.save_revision().publish()

    section = _cs_section_block(cs_item.pk, item_id="cs-idem-uuid")
    # Pre-set the post-migration struct form with an existing analytics_id
    section["value"]["section_content"][0]["value"]["case_study_items"][0]["value"] = {
        "page": cs_item.pk,
        "analytics_id": existing_uid,
    }
    page = AnonymIndexPage(
        title="PCSA Index Idem",
        slug="pcsa-idem-index",
        content=[section],
    )
    minimal_site.root_page.add_child(instance=page)
    page.save_revision().publish()

    call_command("populate_case_study_analytics_ids")

    page.refresh_from_db()
    item_value = list(page.content.raw_data)[0]["value"]["section_content"][0]["value"]["case_study_items"][0]["value"]
    assert item_value["analytics_id"] == existing_uid


# ---------------------------------------------------------------------------
# populate_nav_button_analytics_ids
# ---------------------------------------------------------------------------


def test_populate_nav_button_analytics_ids_injects_uuid(minimal_site: Site) -> None:  # noqa: F811
    """Injects analytics_id into nav links with has_button_appearance=True."""
    page = AnonymIndexPage(
        title="PNBA Inject Test",
        slug="pnba-inject",
        navigation=[_nav_button_link("inject")],
    )
    minimal_site.root_page.add_child(instance=page)
    page.save_revision().publish()
    # Confirm pre-condition: analytics_id exists but is not yet populated
    assert not list(page.navigation.raw_data)[0]["value"].get("analytics_id")

    call_command("populate_nav_button_analytics_ids")

    page.refresh_from_db()
    nav_value = list(page.navigation.raw_data)[0]["value"]
    assert nav_value.get("analytics_id")


def test_populate_nav_button_analytics_ids_skips_non_button_links(minimal_site: Site) -> None:  # noqa: F811
    """Does not inject analytics_id into nav links without has_button_appearance."""
    page = AnonymIndexPage(
        title="PNBA Skip Test",
        slug="pnba-skip",
        navigation=[_nav_button_link("skip", has_button=False)],
    )
    minimal_site.root_page.add_child(instance=page)
    page.save_revision().publish()
    # Confirm pre-condition: analytics_id is absent on non-button links
    assert not list(page.navigation.raw_data)[0]["value"].get("analytics_id")

    call_command("populate_nav_button_analytics_ids")

    page.refresh_from_db()
    nav_value = list(page.navigation.raw_data)[0]["value"]
    assert not nav_value.get("analytics_id")


def test_populate_nav_button_analytics_ids_idempotent(minimal_site: Site) -> None:  # noqa: F811
    """Does not overwrite an existing analytics_id when the command is run again."""
    existing_uid = "fixed-uid-pnba-9012"
    page = AnonymIndexPage(
        title="PNBA Idem Test",
        slug="pnba-idem",
        navigation=[_nav_button_link("idem", has_button=True, analytics_id=existing_uid)],
    )
    minimal_site.root_page.add_child(instance=page)
    page.save_revision().publish()

    call_command("populate_nav_button_analytics_ids")

    page.refresh_from_db()
    nav_value = list(page.navigation.raw_data)[0]["value"]
    assert nav_value["analytics_id"] == existing_uid
