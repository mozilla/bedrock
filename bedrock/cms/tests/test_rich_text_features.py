# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from bs4 import BeautifulSoup
from wagtail.admin.icons import get_icons
from wagtail.admin.rich_text.converters.contentstate import ContentstateConverter
from wagtail.rich_text import features as feature_registry

from bedrock.mozorg.blocks.common import RICHTEXT_BODY_FEATURES


def test_lede_feature_round_trips_through_the_editor():
    converter = ContentstateConverter(features=["lede"])
    html = '<p class="m24-u-lede">An introductory paragraph.</p><p>A regular paragraph.</p>'

    contentstate = json.loads(converter.from_database_format(html))
    assert [block["type"] for block in contentstate["blocks"]] == ["lede", "unstyled"]

    saved = BeautifulSoup(converter.to_database_format(json.dumps(contentstate)), "html.parser")
    assert [(p.get("class"), p.get_text()) for p in saved.find_all("p")] == [
        (["m24-u-lede"], "An introductory paragraph."),
        (None, "A regular paragraph."),
    ]


def test_rich_text_body_features_round_trip_through_the_editor():
    converter = ContentstateConverter(features=RICHTEXT_BODY_FEATURES)
    html = '<p class="m24-u-lede">Lede copy.</p><ul><li>An item</li></ul><p>See <a href="https://example.com/">the source</a>.</p>'

    saved = BeautifulSoup(converter.to_database_format(converter.from_database_format(html)), "html.parser")

    assert saved.find("p", class_="m24-u-lede").get_text() == "Lede copy."
    assert saved.find("ul").find("li").get_text() == "An item"
    assert saved.find("a", href="https://example.com/").get_text() == "the source"


def test_lede_feature_is_not_a_default_feature():
    assert "lede" not in feature_registry.get_default_features()


def test_lede_feature_uses_the_registered_lede_icon():
    assert feature_registry.get_editor_plugin("draftail", "lede").data["icon"] == "lede"
    assert 'id="icon-lede"' in get_icons()
