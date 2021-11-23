# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from copy import deepcopy
from unittest.mock import ANY, Mock, patch

from django.test import override_settings

import pytest
from rich_text_renderer.block_renderers import ListItemRenderer
from rich_text_renderer.text_renderers import TextRenderer

from bedrock.contentful.api import (
    AssetBlockRenderer,
    EmphasisRenderer,
    InlineEntryRenderer,
    LinkRenderer,
    OlRenderer,
    PRenderer,
    StrongRenderer,
    UlRenderer,
    _get_abbr_from_width,
    _get_aspect_ratio_class,
    _get_card_image_url,
    _get_column_class,
    _get_height,
    _get_image_url,
    _get_layout_class,
    _get_product_class,
    _get_width_class,
    _get_youtube_id,
    _make_cta_button,
    _make_logo,
    _make_plain_text,
    _make_wordmark,
    _only_child,
    _render_list,
    contentful_locale,
    get_client,
)


@pytest.mark.parametrize("raw_mode", [True, False])
@override_settings(
    CONTENTFUL_SPACE_ID="test_space_id",
    CONTENTFUL_SPACE_KEY="test_space_key",
    CONTENTFUL_ENVIRONMENT="test_environment",
    CONTENTFUL_SPACE_API="https://example.com/test/",
)
@patch("bedrock.contentful.api.contentful_api")
def test_get_client(mock_contentful_api, raw_mode):
    mock_client = Mock()

    mock_contentful_api.Client.return_value = mock_client

    assert get_client(raw_mode=raw_mode) == mock_client

    mock_contentful_api.Client.assert_called_once_with(
        "test_space_id",
        "test_space_key",
        environment="test_environment",
        api_url="https://example.com/test/",
        raw_mode=raw_mode,
        content_type_cache=False,
    )


@override_settings(
    CONTENTFUL_SPACE_ID="",
    CONTENTFUL_SPACE_KEY="",
)
@pytest.mark.parametrize("raw_mode", [True, False])
@patch("bedrock.contentful.api.contentful_api")
def test_get_client__no_credentials(mock_contentful_api, raw_mode):
    mock_client = Mock()
    mock_contentful_api.Client.return_value = mock_client
    assert get_client(raw_mode=raw_mode) is None
    assert not mock_contentful_api.Client.called


@pytest.mark.parametrize(
    "locale, expected",
    (
        ("en-US", "en-US"),
        ("en-GB", "en-GB"),
        ("de", "de-DE"),
        ("fr", "fr"),
        ("fr-CA", "fr-CA"),
        ("es", "es"),
        ("es-mx", "es"),
    ),
)
def test_contentful_locale(locale, expected):
    assert contentful_locale(locale) == expected


@pytest.mark.parametrize(
    "width, aspect, expected",
    (
        (300, "1:1", 300),
        (300, "3:2", 200),
        (300, "16:9", 169),
    ),
)
def test__get_height(width, aspect, expected):
    assert _get_height(width, aspect) == expected


def test__get_image_url():
    mock_image = Mock()
    mock_image.url.return_value = "//example.com/path/to/image/"

    assert _get_image_url(mock_image, 567) == "https://example.com/path/to/image/"
    mock_image.url.assert_called_once_with(w=567)


def test__get_card_image_url():
    mock_image = Mock()
    mock_image.url.return_value = "//example.com/path/to/image/"

    assert _get_card_image_url(mock_image, 300, "3:2") == "https://example.com/path/to/image/"
    mock_image.url.assert_called_once_with(
        w=300,
        h=200,
        fit="fill",
        f="faces",
    )


@pytest.mark.parametrize(
    ("product_name, expected"),
    (
        ("Firefox", "mzp-t-product-family"),
        ("Firefox Browser", "mzp-t-product-firefox"),
        ("Firefox Browser Beta", "mzp-t-product-beta"),
        ("Firefox Browser Developer", "mzp-t-product-developer"),
        ("Firefox Browser Nightly", "mzp-t-product-nightly"),
        ("Firefox Browser Focus", "mzp-t-product-focus"),
        ("Firefox Monitor", "mzp-t-product-monitor"),
        ("Firefox Lockwise", "mzp-t-product-lockwise"),
        ("Firefox Relay", "mzp-t-product-relay"),
        ("Mozilla", "mzp-t-product-mozilla"),
        ("Mozilla VPN", "mzp-t-product-vpn"),
        ("Pocket", "mzp-t-product-pocket"),
    ),
)
def test__get_product_class(product_name, expected):
    assert _get_product_class(product_name) == expected


@pytest.mark.parametrize(
    "layout,expected",
    (
        ("layout2Cards", "mzp-l-card-half"),
        ("layout3Cards", "mzp-l-card-third"),
        ("layout4Cards", "mzp-l-card-quarter"),
        ("layout5Cards", "mzp-l-card-hero"),
    ),
)
def test__get_layout_class(layout, expected):
    assert _get_layout_class(layout) == expected


@pytest.mark.parametrize(
    "width,expected",
    (
        ("Extra Small", "xs"),
        ("Small", "sm"),
        ("Medium", "md"),
        ("Large", "lg"),
        ("Extra Large", "xl"),
        ("Max", "max"),
    ),
)
def test__get_abbr_from_width(width, expected):
    assert _get_abbr_from_width(width) == expected


@pytest.mark.parametrize(
    "ratio,expected",
    (
        ("1:1", "mzp-has-aspect-1-1"),
        ("3:2", "mzp-has-aspect-3-2"),
        ("16:9", "mzp-has-aspect-16-9"),
    ),
)
def test__get_aspect_ratio_class(ratio, expected):
    assert _get_aspect_ratio_class(ratio) == expected


@pytest.mark.parametrize(
    "width,expected",
    (
        ("Extra Small", "mzp-t-content-xs"),
        ("Small", "mzp-t-content-sm"),
        ("Medium", "mzp-t-content-md"),
        ("Large", "mzp-t-content-lg"),
        ("Extra Large", "mzp-t-content-xl"),
        ("Max", "mzp-t-content-max"),
    ),
)
def test__get_width_class(width, expected):
    assert _get_width_class(width) == expected


@pytest.mark.parametrize(
    "url",
    (
        "https://www.youtube.com/watch?v=qldxyjEjjBQ",
        "https://www.youtube.com/watch?v=qldxyjEjjBQ&some=querystring-here",
        "https://www.youtube.com/watch?v=qldxyjEjjBQ&v=BAD_SECOND_VIDEO_ID",
    ),
)
def test__get_youtube_id(url):
    assert _get_youtube_id(url) == "qldxyjEjjBQ"


@pytest.mark.parametrize(
    "classname,expected",
    (
        ("1", ""),
        ("2", "mzp-l-columns mzp-t-columns-two"),
        ("3", "mzp-l-columns mzp-t-columns-three"),
        ("4", "mzp-l-columns mzp-t-columns-four"),
    ),
)
def test__get_column_class(classname, expected):
    assert _get_column_class(classname) == expected


@pytest.mark.parametrize(
    "product_icon, icon_size, expected_data",
    (
        (
            "Firefox",
            "Small",
            {
                "product_name": "Firefox",
                "product_icon": "family",
                "icon_size": "sm",
            },
        ),
        ("", "Medium", None),
        (
            None,
            "Medium",
            None,
        ),
        (
            "Mozilla",
            None,
            {
                "product_name": "Mozilla",
                "product_icon": "mozilla",
                "icon_size": "md",
            },
        ),
    ),
)
@patch("bedrock.contentful.api.render_to_string")
def test__make_logo(
    mock_render_to_string,
    product_icon,
    icon_size,
    expected_data,
):
    mock_entry = Mock()
    data_dict = {}

    if product_icon:
        data_dict.update({"product_icon": product_icon})
    if icon_size:
        data_dict.update({"icon_size": icon_size})
    mock_entry.fields.return_value = data_dict

    _make_logo(mock_entry)

    if expected_data:
        mock_render_to_string.assert_called_once_with(
            "includes/contentful/logo.html",
            expected_data,
            ANY,
        )
    else:
        assert mock_render_to_string.call_count == 0


@pytest.mark.parametrize(
    "product_icon, icon_size, expected_data",
    (
        (
            "Firefox",
            "Small",
            {
                "product_name": "Firefox",
                "product_icon": "family",
                "icon_size": "sm",
            },
        ),
        ("", "Medium", None),
        (
            None,
            "Medium",
            None,
        ),
        (
            "Mozilla",
            None,
            {
                "product_name": "Mozilla",
                "product_icon": "mozilla",
                "icon_size": "md",
            },
        ),
    ),
)
@patch("bedrock.contentful.api.render_to_string")
def test__make_wordmark(
    mock_render_to_string,
    product_icon,
    icon_size,
    expected_data,
):
    mock_entry = Mock()
    data_dict = {}

    if product_icon:
        data_dict.update({"product_icon": product_icon})
    if icon_size:
        data_dict.update({"icon_size": icon_size})
    mock_entry.fields.return_value = data_dict

    _make_wordmark(mock_entry)

    if expected_data:
        mock_render_to_string.assert_called_once_with(
            "includes/contentful/wordmark.html",
            expected_data,
            ANY,
        )
    else:
        assert mock_render_to_string.call_count == 0


@pytest.mark.parametrize(
    "action, label, theme, size, expected_data",
    (
        (
            "Test action",
            "Test button label",
            "Primary",
            "Small",
            {
                "action": "Test action",
                "label": "Test button label",
                "button_class": "mzp-t-product mzp-t-sm",
                "location": "",
                "cta_text": "Test button label",
            },
        ),
        (
            "Get Mozilla VPN",
            "Test button label",
            "Secondary",
            "Large",
            {
                "action": "Get Mozilla VPN",
                "label": "Test button label",
                "button_class": "mzp-t-secondary mzp-t-lg",
                "location": "",
                "cta_text": "Test button label",
            },
        ),
        (
            "Minimal content test",
            "Test button label",
            "irrelevant",
            "unsupported size",
            {
                "action": "Minimal content test",
                "label": "Test button label",
                "button_class": "mzp-t-product mzp-t-",  # broken class, but looks intentional in source
                "location": "",
                "cta_text": "Test button label",
            },
        ),
    ),
)
@patch("bedrock.contentful.api.render_to_string")
def test__make_cta_button(
    mock_render_to_string,
    action,
    label,
    theme,
    size,
    expected_data,
):
    mock_entry = Mock()
    data_dict = {}

    if action:
        data_dict.update({"action": action})
    if label:
        data_dict.update({"label": label})
    if theme:
        data_dict.update({"theme": theme})
    if size:
        data_dict.update({"size": size})

    mock_entry.fields.return_value = data_dict

    _make_cta_button(mock_entry)

    if expected_data:
        mock_render_to_string.assert_called_once_with(
            "includes/contentful/cta.html",
            expected_data,
            ANY,
        )
    else:
        assert mock_render_to_string.call_count == 0


def test__make_plain_text():

    # Note this test will need a fixup when we add unidecode() support
    node = {
        "content": [
            {"value": "one"},
            {"value": "two"},
            {"value": "three"},
        ]
    }

    assert _make_plain_text(node) == "onetwothree"


def test__only_child():
    # TODO: Broaden this out a bit - these aren't sufficient as-is, but are a start.
    # Written as based purely on the source code, not the data from Contentful
    node = {
        "content": [
            {
                "nodeType": "text",
                "value": "some text",
            },
            {
                "nodeType": "dummy-other",
                "value": "",
            },
            {
                "nodeType": "dummy-other",
                "value": "",
            },
            {
                "nodeType": "text",
                "value": "more text",
            },
            {
                "nodeType": "dummy-extra",
                "value": "",
            },
        ]
    }

    assert not _only_child(node, "text")
    assert not _only_child(node, "dummy-other")
    assert not _only_child(node, "dummy-extra")

    node = {
        "content": [
            {
                "nodeType": "text",
                "value": "some text",
            },
        ]
    }
    assert _only_child(node, "text")
    assert not _only_child(node, "dummy-other")


# These are what the rich_text_renderer library use for its own tests
mock_simple_node = {"value": "foo"}
mock_node = {"content": [{"value": "foo", "nodeType": "text"}]}
mock_list_node = {"content": [{"content": [{"value": "foo", "nodeType": "text"}], "nodeType": "list-item"}]}
mock_hyperlink_node = {
    "data": {"uri": "https://example.com"},
    "content": [{"value": "Example", "nodeType": "text", "marks": []}],
}


def test_StrongRenderer():
    assert StrongRenderer().render(mock_simple_node) == "<strong>foo</strong>"


def test_EmphasisRenderer():
    assert EmphasisRenderer().render(mock_simple_node) == "<em>foo</em>"


@patch("bedrock.contentful.api.get_current_request")
def test_LinkRenderer__mozilla_link(mock_get_current_request):

    mock_request = Mock()
    mock_request.page_info = {"utm_campaign": "TEST"}
    mock_get_current_request.return_value = mock_request
    mozilla_mock_hyperlink_node = deepcopy(mock_hyperlink_node)
    mozilla_mock_hyperlink_node["data"]["uri"] = "https://mozilla.org/test/page/"
    output = LinkRenderer({"text": TextRenderer}).render(mozilla_mock_hyperlink_node)
    expected = (
        '<a href="https://mozilla.org/test/page/?utm_source=www.mozilla.org&utm_medium=referral&utm_campaign=TEST" '
        'data-cta-type="link" data-cta-text="Example" rel="external noopener">Example</a>'
    )

    assert output == expected


@patch("bedrock.contentful.api.get_current_request")
def test_LinkRenderer__mozilla_link__existing_utm(mock_get_current_request):

    mock_request = Mock()
    mock_request.page_info = {"utm_campaign": "TEST"}
    mock_get_current_request.return_value = mock_request
    mozilla_mock_hyperlink_node = deepcopy(mock_hyperlink_node)
    mozilla_mock_hyperlink_node["data"]["uri"] = "https://mozilla.org/test/page/?utm_source=UTMTEST"
    output = LinkRenderer({"text": TextRenderer}).render(mozilla_mock_hyperlink_node)
    expected = (
        '<a href="https://mozilla.org/test/page/?utm_source=UTMTEST" '
        'data-cta-type="link" data-cta-text="Example" rel="external noopener">Example</a>'
    )

    assert output == expected


def test_LinkRenderer__non_mozilla():
    assert (
        LinkRenderer(
            {
                "text": TextRenderer,
            }
        ).render(mock_hyperlink_node)
        == '<a href="https://example.com" data-cta-type="link" data-cta-text="Example" rel="external noopener">Example</a>'
    )


def test_UlRenderer():
    assert (
        UlRenderer(
            {
                "text": TextRenderer,
                "list-item": ListItemRenderer,
            }
        ).render(mock_list_node)
        == "<ul class='mzp-u-list-styled'><li>foo</li></ul>"
    )


def test_OlRenderer():
    assert (
        OlRenderer(
            {
                "text": TextRenderer,
                "list-item": ListItemRenderer,
            }
        ).render(mock_list_node)
        == "<ol class='mzp-u-list-styled'><li>foo</li></ol>"
    )


@pytest.mark.skip("TODO")
def test_LiRenderer():
    assert False, "WRITE ME"


def test_PRenderer():
    assert PRenderer({"text": TextRenderer}).render(mock_node) == "<p>foo</p>"


def test_PRenderer__empty():
    empty_node = deepcopy(mock_node)
    empty_node["content"][0]["value"] = ""
    assert PRenderer({"text": TextRenderer}).render(empty_node) == ""


@pytest.mark.parametrize(
    "content_type_label",
    (
        "componentLogo",
        "componentWordmark",
        "componentCtaButton",
        "somethingElse",
    ),
)
@patch("bedrock.contentful.api.ContentfulPage.client")
@patch("bedrock.contentful.api._make_logo")
@patch("bedrock.contentful.api._make_wordmark")
@patch("bedrock.contentful.api._make_cta_button")
def test_InlineEntryRenderer(
    mock_make_cta_button,
    mock_make_wordmark,
    mock_make_logo,
    mock_client,
    content_type_label,
):

    mock_entry = Mock()
    mock_content_type = Mock()
    mock_content_type.id = content_type_label
    mock_entry.sys = {"content_type": mock_content_type}
    mock_client.entry.return_value = mock_entry

    node = {"data": {"target": {"sys": {"id": mock_entry}}}}

    output = InlineEntryRenderer().render(node)

    if content_type_label == "componentLogo":
        mock_make_logo.assert_called_once_with(mock_entry)
    elif content_type_label == "componentWordmark":
        mock_make_wordmark.assert_called_once_with(mock_entry)
    elif content_type_label == "componentCtaButton":
        mock_make_cta_button.assert_called_once_with(mock_entry)
    else:
        assert output == content_type_label


@patch("bedrock.contentful.api._get_image_url")
@patch("bedrock.contentful.api.ContentfulPage.client")
def test_AssetBlockRenderer(mock_client, mock__get_image_url):
    mock_asset = Mock()
    mock_asset.title = "test title"
    mock_client.asset.return_value = mock_asset

    node = {"data": {"target": {"sys": {"id": mock_asset}}}}
    mock__get_image_url.side_effect = [
        "https://example.com/image.png",
        "https://example.com/image-hires.png",
    ]
    output = AssetBlockRenderer().render(node)
    expected = '<img src="https://example.com/image.png" srcset="https://example.com/image-hires.png 1.5x" alt="test title" />'
    assert output == expected

    assert mock__get_image_url.call_args_list[0][0] == (mock_asset, 688)
    assert mock__get_image_url.call_args_list[1][0] == (mock_asset, 1376)


def test__render_list():
    assert _render_list("ol", "test content here") == "<ol class='mzp-u-list-styled'>test content here</ol>"
    assert _render_list("ul", "test content here") == "<ul class='mzp-u-list-styled'>test content here</ul>"
