# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import ANY, Mock, patch

from django.test import override_settings

import pytest

from bedrock.contentful.api import (
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
