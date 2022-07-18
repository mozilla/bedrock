# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from copy import deepcopy
from unittest.mock import ANY, Mock, call, patch

from django.conf import settings
from django.test import override_settings

import pytest
from rich_text_renderer.block_renderers import ListItemRenderer
from rich_text_renderer.text_renderers import TextRenderer

from bedrock.contentful.api import (
    AssetBlockRenderer,
    ContentfulPage,
    EmphasisRenderer,
    InlineEntryRenderer,
    LinkRenderer,
    LiRenderer,
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
from bedrock.contentful.constants import (
    COMPOSE_MAIN_PAGE_TYPE,
    CONTENT_TYPE_CONNECT_HOMEPAGE,
    CONTENT_TYPE_PAGE_RESOURCE_CENTER,
)


@pytest.mark.parametrize("raw_mode", [True, False])
@override_settings(
    CONTENTFUL_SPACE_ID="test_space_id",
    CONTENTFUL_SPACE_KEY="test_space_key",
    CONTENTFUL_ENVIRONMENT="test_environment",
    CONTENTFUL_SPACE_API="https://example.com/test/",
    CONTENTFUL_API_TIMEOUT=987654321,
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
        timeout_s=987654321,
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
    "bedrock_locale, expected",
    (
        ("en-US", "en-US"),
        ("en-GB", "en-GB"),
        ("de", "de-DE"),
        ("fr", "fr-FR"),
        ("fr-CA", "fr-CA"),
        ("es-ES", "es-ES"),
        ("es-MX", "es-MX"),
    ),
)
def test_contentful_locale(bedrock_locale, expected):
    assert contentful_locale(bedrock_locale) == expected


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
    # Here we're assuming that we need to set a subdomain, because if we
    # used a naked mozilla.org domain we'd get 30Xed to www.mozilla.org
    mozilla_mock_hyperlink_node["data"]["uri"] = "https://subdomain.mozilla.org/test/page/"
    output = LinkRenderer({"text": TextRenderer}).render(mozilla_mock_hyperlink_node)
    expected = (
        '<a href="https://subdomain.mozilla.org/test/page/?utm_source=www.mozilla.org&utm_medium=referral&utm_campaign=TEST" '
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


@patch("bedrock.contentful.api._only_child")
def test__LiRenderer(mock__only_child):

    li_renderer = LiRenderer()

    li_renderer._render_content = Mock("mocked__render_content")
    li_renderer._render_content.return_value = "rendered_content"

    mock__only_child.return_value = True

    output = li_renderer.render(mock_node)
    assert output == "<li>rendered_content</li>"
    mock__only_child.assert_called_once_with(mock_node, "text")

    mock__only_child.reset_mock()
    mock__only_child.return_value = False

    output = li_renderer.render(mock_node)
    assert output == "<li>rendered_content</li>"
    mock__only_child.assert_called_once_with(mock_node, "text")


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
    mock_asset.title = "test_title.png"
    mock_asset.description = "Test Description"
    mock_client.asset.return_value = mock_asset

    node = {"data": {"target": {"sys": {"id": mock_asset}}}}
    mock__get_image_url.side_effect = [
        "https://example.com/image.png",
        "https://example.com/image-hires.png",
    ]
    output = AssetBlockRenderer().render(node)
    expected = '<img src="https://example.com/image.png" srcset="https://example.com/image-hires.png 1.5x" alt="Test Description" loading="lazy" />'

    assert mock__get_image_url.call_args_list[0][0] == (mock_asset, 688)
    assert mock__get_image_url.call_args_list[1][0] == (mock_asset, 1376)

    assert output == expected


def test__render_list():
    assert _render_list("ol", "test content here") == "<ol class='mzp-u-list-styled'>test content here</ol>"
    assert _render_list("ul", "test content here") == "<ul class='mzp-u-list-styled'>test content here</ul>"


@pytest.fixture
def basic_contentful_page(rf):
    """Naive reusable fixutre for setting up a ContentfulPage
    Note that it does NOTHING with set_current_request / thread-locals
    """
    with patch("bedrock.contentful.api.set_current_request"):
        with patch("bedrock.contentful.api.get_locale") as mock_get_locale:
            mock_get_locale.return_value = settings.LANGUAGE_CODE  # use the fallback
            mock_request = rf.get("/")
            page = ContentfulPage(mock_request, "test-page-id")

    return page


@pytest.mark.parametrize("locale_to_patch", ("fr", "de-DE", "es-MX"))
@patch("bedrock.contentful.api.set_current_request")
@patch("bedrock.contentful.api.get_locale")
def test_ContentfulPage__init(
    mock_get_locale,
    mock_set_current_request,
    locale_to_patch,
    rf,
):

    mock_get_locale.side_effect = lambda x: x.locale
    mock_request = rf.get("/")
    mock_request.locale = locale_to_patch
    page = ContentfulPage(mock_request, "test-page-id")

    mock_get_locale.assert_called_once_with(mock_request)
    mock_set_current_request.assert_called_once_with(mock_request)
    assert page.request == mock_request
    assert page.page_id == "test-page-id"
    assert page.locale == locale_to_patch


@pytest.mark.parametrize("locale_to_patch", ("fr", "de-DE", "es-MX"))
def test_ContentfulPage__page_property(basic_contentful_page, locale_to_patch):
    page = basic_contentful_page
    page.locale = locale_to_patch
    page.client = Mock()
    page.client.entry.return_value = "fake page data"

    output = page.page
    assert output == "fake page data"
    page.client.entry.assert_called_once_with(
        "test-page-id",
        {
            "include": 10,
            "locale": locale_to_patch,
        },
    )


def test_ContentfulPage__render_rich_text(basic_contentful_page):

    # The actual/underlying RichTextRenderer is tested in its own package
    # - this test just checks our usage

    basic_contentful_page._renderer.render = Mock()
    basic_contentful_page._renderer.render.return_value = "mock rendered rich text"
    output = basic_contentful_page.render_rich_text(mock_node)
    assert output == "mock rendered rich text"
    basic_contentful_page._renderer.render.assert_called_once_with(mock_node)

    basic_contentful_page._renderer.render.reset_mock()
    output = basic_contentful_page.render_rich_text(None)
    assert output == ""
    assert not basic_contentful_page._renderer.render.called

    basic_contentful_page._renderer.render.reset_mock()
    output = basic_contentful_page.render_rich_text("")
    assert output == ""
    assert not basic_contentful_page._renderer.render.called


def test_ContentfulPage___get_preview_image_from_fields__data_present(basic_contentful_page):
    mock_image = Mock(name="preview_image")
    mock_image.fields.return_value = {
        "file": {
            "url": "//example.com/image.png",
        }
    }

    fields = {"preview_image": mock_image}

    output = basic_contentful_page._get_preview_image_from_fields(fields)
    assert output == "https://example.com/image.png"


def test_ContentfulPage___get_preview_image_from_fields__no_data(
    basic_contentful_page,
):
    assert basic_contentful_page._get_preview_image_from_fields({}) is None


def test_ContentfulPage___get_preview_image_from_fields__bad_data(
    basic_contentful_page,
):
    mock_image = Mock(name="preview_image")
    mock_image.fields.return_value = {
        # no file key
    }
    fields = {"preview_image": mock_image}
    output = basic_contentful_page._get_preview_image_from_fields(fields)
    assert output is None

    mock_image = Mock(name="preview_image")
    mock_image.fields.return_value = {"file": {}}  # no url key
    fields = {"preview_image": mock_image}
    output = basic_contentful_page._get_preview_image_from_fields(fields)
    assert output is None


@pytest.mark.parametrize(
    "entry_fields, expected",
    (
        (
            {"folder": "firefox"},
            {"theme": "firefox", "campaign": "firefox-test-test-test"},
        ),
        (
            {"folder": "mentions-firefox-in-title"},
            {"theme": "firefox", "campaign": "firefox-test-test-test"},
        ),
        (
            {"folder": "other-thing"},
            {"theme": "mozilla", "campaign": "test-test-test"},
        ),
        (
            {"folder": ""},
            {"theme": "mozilla", "campaign": "test-test-test"},
        ),
        (
            {},
            {"theme": "mozilla", "campaign": "test-test-test"},
        ),
    ),
)
def test_ContentfulPage__get_info_data__theme_campaign(
    basic_contentful_page,
    entry_fields,
    expected,
):

    slug = "test-test-test"

    output = basic_contentful_page._get_info_data__theme_campaign(entry_fields, slug)

    assert output == expected


@pytest.mark.parametrize(
    "page_type, entry_fields, entry_obj__sys__locale, expected",
    (
        (
            "pageHome",
            {
                "name": "locale temporarily in overridden name field",
            },
            "Not used",
            {"locale": "locale temporarily in overridden name field"},
        ),
        (
            "pagePageResourceCenter",
            {"name": "NOT USED"},
            "fr-CA",
            {"locale": "fr-CA"},
        ),
    ),
)
def test_ContentfulPage__get_info_data__locale(
    basic_contentful_page,
    page_type,
    entry_fields,
    entry_obj__sys__locale,
    expected,
):
    entry_obj = Mock()
    entry_obj.sys = {"locale": entry_obj__sys__locale}
    output = basic_contentful_page._get_info_data__locale(
        page_type,
        entry_fields,
        entry_obj,
    )
    assert output == expected


@pytest.mark.parametrize(
    "page_title, page_type, page_fields, entry_fields, seo_fields, expected",
    (
        (
            "test page one",
            COMPOSE_MAIN_PAGE_TYPE,
            {"slug": "compose-main-page-slug"},
            {},
            {},
            {
                "slug": "compose-main-page-slug",
                "title": "test page one",
                "blurb": "",
            },
        ),
        (
            "",
            COMPOSE_MAIN_PAGE_TYPE,
            {"slug": "compose-main-page-slug"},
            {},
            {},
            {
                "slug": "compose-main-page-slug",
                "title": "",
                "blurb": "",
            },
        ),
        (
            "",
            COMPOSE_MAIN_PAGE_TYPE,
            {"slug": "compose-main-page-slug"},
            {
                "preview_title": "preview title",
                "preview_blurb": "preview blurb",
            },
            {},
            {
                "slug": "compose-main-page-slug",
                "title": "preview title",
                "blurb": "preview blurb",
            },
        ),
        (
            "",
            COMPOSE_MAIN_PAGE_TYPE,
            {"slug": "compose-main-page-slug"},
            {
                "preview_title": "preview title",
                "preview_blurb": "preview blurb",
            },
            {"description": "seo description"},
            {
                "slug": "compose-main-page-slug",
                "title": "preview title",
                "blurb": "seo description",
            },
        ),
        (
            "page title",
            CONTENT_TYPE_CONNECT_HOMEPAGE,
            {},
            {
                "slug": "homepage-slug",
                "preview_title": "preview title",
                "preview_blurb": "preview blurb",
            },
            {},  # SEO fields not present for non-Compose pages
            {
                "slug": "homepage-slug",
                "title": "preview title",
                "blurb": "preview blurb",
            },
        ),
        (
            "page title",
            CONTENT_TYPE_CONNECT_HOMEPAGE,
            {},
            {
                # no slug field, so will fall back to default of 'home'
                "preview_title": "preview title",
                "preview_blurb": "preview blurb",
            },
            {},  # SEO fields not present for non-Compose pages
            {
                "slug": "home",
                "title": "preview title",
                "blurb": "preview blurb",
            },
        ),
    ),
    ids=[
        "compose page with slug, title, no blurb",
        "compose page with slug, no title, no blurb",
        "compose page with slug, title from entry, blurb from entry",
        "compose page with slug, no title, blurb from seo",
        "Non-Compose page with slug, title, blurb from entry",
        "Non-Compose page with default slug, title, blurb from entry",
    ],
)
def test_ContentfulPage__get_info_data__slug_title_blurb(
    basic_contentful_page,
    page_title,
    page_type,
    page_fields,
    entry_fields,
    seo_fields,
    expected,
):
    basic_contentful_page.page = Mock()
    basic_contentful_page.page.content_type.id = page_type
    basic_contentful_page.page.fields = Mock(return_value=page_fields)
    if page_title:
        basic_contentful_page.page.title = page_title
    else:
        basic_contentful_page.page.title = ""

    assert (
        basic_contentful_page._get_info_data__slug_title_blurb(
            entry_fields,
            seo_fields,
        )
        == expected
    )


@pytest.mark.parametrize(
    "entry_fields, page_type, expected",
    (
        (
            {
                "category": "test category",
                "tags": [
                    "test tag1",
                    "test tag2",
                ],
                "product": "test product",
            },
            CONTENT_TYPE_PAGE_RESOURCE_CENTER,
            {
                "category": "test category",
                "tags": [
                    "test tag1",
                    "test tag2",
                ],
                "classification": "test product",
            },
        ),
        (
            {
                "category": "test category",
                "tags": [
                    "test tag1",
                    "test tag2",
                ],
                "product": "test product",
            },
            "NOT A CONTENT_TYPE_PAGE_RESOURCE_CENTER",
            {},  # no data expected if it's not a VRC page
        ),
    ),
)
def test_ContentfulPage__get_info_data__category_tags_classification(
    basic_contentful_page,
    entry_fields,
    page_type,
    expected,
):

    assert basic_contentful_page._get_info_data__category_tags_classification(entry_fields, page_type) == expected


@pytest.mark.parametrize(
    "entry_obj__fields, seo_obj__fields, expected",
    (
        (
            {
                "dummy": "entry fields",
                "preview_image": "https://example.com/test-entry.png",
            },
            {
                "dummy": "seo fields",
                "preview_image": "https://example.com/test-seo.png",
            },
            {
                "title": "test title",
                "blurb": "test blurb",
                "slug": "test-slug",
                "locale": "fr-CA",
                "theme": "test-theme",
                "utm_source": "www.mozilla.org-test-campaign",
                "utm_campaign": "test-campaign",
                "image": "https://example.com/test-entry.png",
                "category": "test category",
                "tags": [
                    "test tag1",
                    "test tag2",
                ],
                "product": "test product",
                "seo": {
                    "dummy": "seo fields",
                    "image": "https://example.com/test-seo.png",
                },
            },
        ),
        (
            {
                "dummy": "entry fields",
                "preview_image": "https://example.com/test-entry.png",
            },
            None,  # no SEO fields
            {
                "title": "test title",
                "blurb": "test blurb",
                "slug": "test-slug",
                "locale": "fr-CA",
                "theme": "test-theme",
                "utm_source": "www.mozilla.org-test-campaign",
                "utm_campaign": "test-campaign",
                "image": "https://example.com/test-entry.png",
                "category": "test category",
                "tags": [
                    "test tag1",
                    "test tag2",
                ],
                "product": "test product",
            },
        ),
    ),
    ids=["entry_obj and seo_obj", "entry_obj, no seo_obj"],
)
@patch("bedrock.contentful.api.ContentfulPage._get_preview_image_from_fields")
@patch("bedrock.contentful.api.ContentfulPage._get_info_data__locale")
@patch("bedrock.contentful.api.ContentfulPage._get_info_data__theme_campaign")
@patch("bedrock.contentful.api.ContentfulPage._get_info_data__slug_title_blurb")
@patch("bedrock.contentful.api.ContentfulPage._get_info_data__category_tags_classification")
def test_ContentfulPage__get_info_data(
    mock__get_info_data__category_tags_classification,
    mock__get_info_data__slug_title_blurb,
    mock__get_info_data__theme_campaign,
    mock__get_info_data__locale,
    mock__get_preview_image_from_fields,
    basic_contentful_page,
    entry_obj__fields,
    seo_obj__fields,
    expected,
):

    mock__get_preview_image_from_fields.side_effect = [
        "https://example.com/test-entry.png",
        "https://example.com/test-seo.png",
    ]
    mock__get_info_data__theme_campaign.return_value = {
        "theme": "test-theme",
        "campaign": "test-campaign",
    }
    mock__get_info_data__locale.return_value = {
        "locale": "fr-CA",
    }
    mock__get_info_data__slug_title_blurb.return_value = {
        "slug": "test-slug",
        "title": "test title",
        "blurb": "test blurb",
    }
    mock__get_info_data__category_tags_classification.return_value = {
        "category": "test category",
        "tags": [
            "test tag1",
            "test tag2",
        ],
        "product": "test product",
    }

    mock_entry_obj = Mock()
    mock_entry_obj.fields.return_value = entry_obj__fields
    mock_entry_obj.content_type.id = "mock-page-type"

    if seo_obj__fields:
        mock_seo_obj = Mock()
        mock_seo_obj.fields.return_value = seo_obj__fields
    else:
        mock_seo_obj = None

    output = basic_contentful_page.get_info_data(mock_entry_obj, mock_seo_obj)

    assert output == expected

    if seo_obj__fields:
        assert mock__get_preview_image_from_fields.call_count == 2
        assert (
            call(
                {
                    "dummy": "entry fields",
                    "preview_image": "https://example.com/test-entry.png",
                }
            )
            in mock__get_preview_image_from_fields.call_args_list
        )
        assert (
            call(
                {
                    "dummy": "seo fields",
                    "preview_image": "https://example.com/test-seo.png",
                },
            )
            in mock__get_preview_image_from_fields.call_args_list
        )

    else:
        assert mock__get_preview_image_from_fields.call_count == 1
        mock__get_preview_image_from_fields.assert_called_once_with(entry_obj__fields)

    mock__get_info_data__category_tags_classification.assert_called_once_with(
        entry_obj__fields,
        "mock-page-type",
    )
    mock__get_info_data__slug_title_blurb.assert_called_once_with(
        entry_obj__fields,
        seo_obj__fields,
    )
    mock__get_info_data__theme_campaign.assert_called_once_with(
        entry_obj__fields,
        "test-slug",
    )
    mock__get_info_data__locale.assert_called_once_with(
        "mock-page-type",
        entry_obj__fields,
        mock_entry_obj,
    )


@patch("bedrock.contentful.api._get_image_url")
def test_ContentfulPage__get_split_data(mock__get_image_url, basic_contentful_page):
    # mock self and entry data
    basic_contentful_page.page = Mock()
    basic_contentful_page.page.content_type.id = "mockPage"
    basic_contentful_page.render_rich_text = Mock()
    mock_entry_obj = Mock()
    # only set required and default fields
    mock_entry_obj.fields.return_value = {
        "name": "Split Test",
        "image": "Stub image",
        "body": "Stub body",
        "mobile_media_after": False,
    }
    mock_entry_obj.content_type.id = "mock-split-type"

    output = basic_contentful_page.get_split_data(mock_entry_obj)

    def is_empty_string(string):
        return len(string.strip()) == 0

    assert output["component"] == "split"
    assert is_empty_string(output["block_class"])
    assert is_empty_string(output["theme_class"])
    assert is_empty_string(output["body_class"])
    basic_contentful_page.render_rich_text.assert_called_once()
    assert is_empty_string(output["media_class"])
    assert output["media_after"] is False
    mock__get_image_url.assert_called_once()
    assert is_empty_string(output["mobile_class"])


@pytest.mark.parametrize(
    "split_class_fields, expected",
    (
        (None, ""),
        ({"image_side": "Right"}, ""),
        ({"image_side": "Left"}, "mzp-l-split-reversed"),
        ({"body_width": "Even"}, ""),
        ({"body_width": "Narrow"}, "mzp-l-split-body-narrow"),
        ({"body_width": "Wide"}, "mzp-l-split-body-wide"),
        ({"image_pop": "None"}, ""),
        ({"image_pop": "Both"}, "mzp-l-split-pop"),
        ({"image_pop": "Top"}, "mzp-l-split-pop-top"),
        ({"image_pop": "Bottom"}, "mzp-l-split-pop-bottom"),
        ({"image_side": "Left", "body_width": "Narrow", "image_pop": "Both"}, "mzp-l-split-reversed mzp-l-split-body-narrow mzp-l-split-pop"),
    ),
)
@patch("bedrock.contentful.api._get_image_url")
def test_ContentfulPage__get_split_data__get_split_class(
    mock__get_image_url,
    basic_contentful_page,
    split_class_fields,
    expected,
):
    # mock self and entry data
    basic_contentful_page.page = Mock()
    basic_contentful_page.page.content_type.id = "mockPage"
    basic_contentful_page.render_rich_text = Mock()
    mock_entry_obj = Mock()
    mock_entry_obj.fields.return_value = {
        "name": "Split Test",
        "image": "Stub image",
        "body": "Stub body",
        "mobile_media_after": False,
    }
    if split_class_fields:
        mock_entry_obj.fields.return_value.update(split_class_fields)

    mock_entry_obj.content_type.id = "mock-split-type"

    output = basic_contentful_page.get_split_data(mock_entry_obj)

    assert output["block_class"].strip() == expected


@pytest.mark.parametrize(
    "page_id, body_class_fields, expected",
    (
        ("mockPage", None, ""),
        ("pageHome", None, "c-home-body"),
        ("mockPage", {"body_vertical_alignment": "Top"}, "mzp-l-split-v-start"),
        ("mockPage", {"body_vertical_alignment": "Center"}, "mzp-l-split-v-center"),
        ("mockPage", {"body_vertical_alignment": "Bottom"}, "mzp-l-split-v-end"),
        ("mockPage", {"body_horizontal_alignment": "Left"}, "mzp-l-split-h-start"),
        ("mockPage", {"body_horizontal_alignment": "Center"}, "mzp-l-split-h-center"),
        ("mockPage", {"body_horizontal_alignment": "Right"}, "mzp-l-split-h-end"),
        (
            "pageHome",
            {"body_vertical_alignment": "Top", "body_horizontal_alignment": "Center"},
            "mzp-l-split-v-start mzp-l-split-h-center c-home-body",
        ),
    ),
)
@patch("bedrock.contentful.api._get_image_url")
def test_ContentfulPage__get_split_data__get_body_class(
    mock__get_image_url,
    basic_contentful_page,
    page_id,
    body_class_fields,
    expected,
):
    # mock self and entry data
    basic_contentful_page.page = Mock()
    basic_contentful_page.page.content_type.id = page_id
    basic_contentful_page.render_rich_text = Mock()
    mock_entry_obj = Mock()
    mock_entry_obj.fields.return_value = {
        "name": "Split Test",
        "image": "Stub image",
        "body": "Stub body",
        "mobile_media_after": False,
    }
    if body_class_fields:
        mock_entry_obj.fields.return_value.update(body_class_fields)

    mock_entry_obj.content_type.id = "mock-split-type"

    output = basic_contentful_page.get_split_data(mock_entry_obj)

    assert output["body_class"].strip() == expected


@pytest.mark.parametrize(
    "media_class_fields, expected",
    (
        (None, ""),
        ({"image_width": "Fill available width"}, ""),
        ({"image_width": "Fill available height"}, "mzp-l-split-media-constrain-height"),
        ({"image_width": "Overflow container"}, "mzp-l-split-media-overflow"),
    ),
)
@patch("bedrock.contentful.api._get_image_url")
def test_ContentfulPage__get_split_data__get_media_class(mock__get_image_url, basic_contentful_page, media_class_fields, expected):
    # mock self and entry data
    basic_contentful_page.page = Mock()
    basic_contentful_page.page.content_type.id = "mockPage"
    basic_contentful_page.render_rich_text = Mock()
    mock_entry_obj = Mock()
    mock_entry_obj.fields.return_value = {
        "name": "Split Test",
        "image": "Stub image",
        "body": "Stub body",
        "mobile_media_after": False,
    }
    if media_class_fields:
        mock_entry_obj.fields.return_value.update(media_class_fields)

    mock_entry_obj.content_type.id = "mock-split-type"

    output = basic_contentful_page.get_split_data(mock_entry_obj)

    assert output["media_class"].strip() == expected


@pytest.mark.parametrize(
    "mobile_class_fields, expected",
    (
        (None, ""),
        ({"mobile_display": "Center content"}, "mzp-l-split-center-on-sm-md"),
        ({"mobile_display": "Hide image"}, "mzp-l-split-hide-media-on-sm-md"),
    ),
)
@patch("bedrock.contentful.api._get_image_url")
def test_ContentfulPage__get_split_data__get_mobile_class(mock__get_image_url, basic_contentful_page, mobile_class_fields, expected):
    # mock self and entry data
    basic_contentful_page.page = Mock()
    basic_contentful_page.page.content_type.id = "mockPage"
    basic_contentful_page.render_rich_text = Mock()
    mock_entry_obj = Mock()
    mock_entry_obj.fields.return_value = {
        "name": "Split Test",
        "image": "Stub image",
        "body": "Stub body",
        "mobile_media_after": False,
    }
    if mobile_class_fields:
        mock_entry_obj.fields.return_value.update(mobile_class_fields)

    mock_entry_obj.content_type.id = "mock-split-type"

    output = basic_contentful_page.get_split_data(mock_entry_obj)

    assert output["mobile_class"].strip() == expected


# FURTHER TESTS TO COME
# def test_ContentfulPage__get_content():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_content__proc():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_text_data():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_hero_data():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_section_data():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_callout_data():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_card_data():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_large_card_data():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_card_layout_data():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_picto_data():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_picto_layout_data():
#     assert False, "WRITE ME"


# def test_ContentfulPage__get_text_column_data():
#     assert False, "WRITE ME"
