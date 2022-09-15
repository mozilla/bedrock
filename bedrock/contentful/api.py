# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from copy import deepcopy
from functools import partialmethod
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from django.conf import settings
from django.utils.functional import cached_property

import contentful as contentful_api
from crum import get_current_request, set_current_request
from rich_text_renderer import RichTextRenderer
from rich_text_renderer.base_node_renderer import BaseNodeRenderer
from rich_text_renderer.block_renderers import BaseBlockRenderer
from rich_text_renderer.text_renderers import BaseInlineRenderer

from bedrock.contentful.constants import (
    CONTENT_TYPE_PAGE_GENERAL,
    CONTENT_TYPE_PAGE_RESOURCE_CENTER,
)
from lib.l10n_utils import get_locale, render_to_string

# Some of Bedrock and Contentful's locale codes slightly differ, so we translate between them.
# This is not the controlling list of which locales we read from Contentful - that's determined
# by what Contentful has configured/enabled and we try to pull in all of what's offered.
BEDROCK_TO_CONTENTFUL_LOCALE_MAP = {
    "de": "de-DE",
    "fr": "fr-FR",
    "zh-TW": "zh-Hant-TW",  # NB: we should move to zh-Hant-TW in Bedrock - https://github.com/mozilla/bedrock/issues/10891
    "nl": "nl-NL",
    "id": "id-ID",
    "it": "it-IT",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "ms": "ms-MY",
    "pl": "pl-PL",
    "ru": "ru-RU",
    "tr": "tr-TR",
    "vi": "vi-VN",
}
CONTENTFUL_TO_BEDROCK_LOCALE_MAP = {v: k for k, v in BEDROCK_TO_CONTENTFUL_LOCALE_MAP.items()}

ASPECT_RATIOS = {
    "1:1": "1-1",
    "3:2": "3-2",
    "16:9": "16-9",
}
ASPECT_MULTIPLIER = {"1:1": 1, "3:2": 0.6666, "16:9": 0.5625}
PRODUCT_THEMES = {
    "Firefox": "family",
    "Firefox Browser": "firefox",
    "Firefox Browser Beta": "beta",
    "Firefox Browser Developer": "developer",
    "Firefox Browser Nightly": "nightly",
    "Firefox Browser Focus": "focus",
    "Firefox Monitor": "monitor",
    "Firefox Lockwise": "lockwise",
    "Firefox Relay": "relay",
    "Mozilla": "mozilla",
    "Mozilla VPN": "vpn",
    "Pocket": "pocket",
    "MDN Plus": "mdn-plus",
}
WIDTHS = {
    "Extra Small": "xs",
    "Small": "sm",
    "Medium": "md",
    "Large": "lg",
    "Extra Large": "xl",
    "Max": "max",
}
LAYOUT_CLASS = {
    "layout2Cards": "mzp-l-card-half",
    "layout3Cards": "mzp-l-card-third",
    "layout4Cards": "mzp-l-card-quarter",
    "layout5Cards": "mzp-l-card-hero",
}
THEME_CLASS = {
    "Light": "",
    "Light (alternative)": "mzp-t-background-secondary",
    "Dark": "mzp-t-dark",
    "Dark (alternative)": "mzp-t-dark mzp-t-background-secondary",
}
COLUMN_CLASS = {
    "1": "",
    "2": "mzp-l-columns mzp-t-columns-two",
    "3": "mzp-l-columns mzp-t-columns-three",
    "4": "mzp-l-columns mzp-t-columns-four",
}


def get_client(raw_mode=False):
    client = None
    if settings.CONTENTFUL_SPACE_ID and settings.CONTENTFUL_SPACE_KEY:
        client = contentful_api.Client(
            settings.CONTENTFUL_SPACE_ID,
            settings.CONTENTFUL_SPACE_KEY,
            environment=settings.CONTENTFUL_ENVIRONMENT,
            api_url=settings.CONTENTFUL_SPACE_API,
            raw_mode=raw_mode,
            content_type_cache=False,
            timeout_s=settings.CONTENTFUL_API_TIMEOUT,
        )

    return client


def contentful_locale(locale):
    """Returns the Contentful locale for the Bedrock locale"""
    return BEDROCK_TO_CONTENTFUL_LOCALE_MAP.get(locale, locale)


def _get_height(width, aspect):
    return round(width * ASPECT_MULTIPLIER.get(aspect, 0))


def _get_image_url(image, width):
    return "https:" + image.url(
        w=width,
    )


def _get_card_image_url(image, width, aspect):
    return "https:" + image.url(
        w=width,
        h=_get_height(width, aspect),
        fit="fill",
        f="faces",
    )


def _get_product_class(product):
    return f'mzp-t-product-{PRODUCT_THEMES.get(product, "")}'


def _get_layout_class(layout):
    return LAYOUT_CLASS.get(layout, "")


def _get_abbr_from_width(width):
    return WIDTHS.get(width, "")


def _get_aspect_ratio_class(aspect_ratio):
    return f'mzp-has-aspect-{ASPECT_RATIOS.get(aspect_ratio, "")}'


def _get_width_class(width):
    return f'mzp-t-content-{WIDTHS.get(width, "")}' if width else ""


def _get_theme_class(theme):
    return THEME_CLASS.get(theme, "")


def _get_youtube_id(youtube_url):
    url_data = urlparse(youtube_url)
    queries = parse_qs(url_data.query)
    youtube_id = queries["v"][0]
    return youtube_id


def _get_column_class(columns):
    return COLUMN_CLASS.get(columns, "")


def _make_logo(entry):
    fields = entry.fields()
    product = fields.get("product_icon")
    if not product:
        return ""

    data = {
        "product_name": product,
        "product_icon": PRODUCT_THEMES.get(product, ""),
        "icon_size": WIDTHS.get(fields.get("icon_size"), "") if fields.get("icon_size") else "md",
    }

    return render_to_string("includes/contentful/logo.html", data, get_current_request())


def _make_wordmark(entry):
    fields = entry.fields()
    product = fields.get("product_icon")
    if not product:
        return ""

    data = {
        "product_name": product,
        "product_icon": PRODUCT_THEMES.get(product, ""),
        "icon_size": WIDTHS.get(fields.get("icon_size"), "") if fields.get("icon_size") else "md",
    }

    return render_to_string("includes/contentful/wordmark.html", data, get_current_request())


def _make_cta_button(entry):
    fields = entry.fields()
    action = fields.get("action")

    button_class = [
        # TODO, only add on Firefox themed pages
        "mzp-t-product" if action != "Get Mozilla VPN" and action != "Get MDN Plus" else "",
        "mzp-t-secondary" if fields.get("theme") == "Secondary" else "",
        f'mzp-t-{WIDTHS.get(fields.get("size"), "")}' if fields.get("size") else "",
    ]
    data = {
        "action": action,
        "label": fields.get("label"),
        "button_class": " ".join([_class for _class in button_class if _class]),
        # TODO
        "location": "",  # eg primary, secondary
        "cta_text": fields.get("label"),  # TODO needs to use English in all locales
    }
    return render_to_string("includes/contentful/cta.html", data, get_current_request())


def _make_plain_text(node):
    content = node["content"]
    plain = ""

    for child_node in content:
        plain += child_node["value"]

    # TODO
    # return unidecode(plain)
    return plain


def _only_child(node, nodeType):
    content = node["content"]
    found = 0
    only = True
    for child_node in content:
        # if it's not the matching node type
        if child_node["nodeType"] != nodeType and found == 0:
            # and not an empty text node
            if child_node["nodeType"] == "text" and child_node["value"] != "":
                # it's not the only child
                only = False
                break
        # if it's the second matching node type it's not the only child
        elif child_node["nodeType"] == nodeType:
            found += 1
            if found > 1:
                only = False
                break

    return only


class StrongRenderer(BaseInlineRenderer):
    @property
    def _render_tag(self):
        return "strong"


class EmphasisRenderer(BaseInlineRenderer):
    @property
    def _render_tag(self):
        return "em"


class LinkRenderer(BaseBlockRenderer):
    def render(self, node):
        url = urlparse(node["data"]["uri"])
        request = get_current_request()
        ref = ""
        rel = ""
        data_cta = ""

        # add referral info to links to other mozilla properties
        # TODO: can we make this just if url.netloc == "mozilla.org" or are we expecting
        # subdomains, because we set the utm_source to www.mozilla.org
        if "mozilla.org" in url.netloc and url.netloc != "www.mozilla.org":
            # don't add if there's already utms
            if "utm_" not in url.query:
                params = {
                    "utm_source": "www.mozilla.org",
                    "utm_medium": "referral",
                    "utm_campaign": request.page_info["utm_campaign"],
                }
                add = "?" if url.query == "" else "&"
                ref = add + urlencode(params)

        # TODO, should this be based on the current server (ie dev, stage)?
        # add attributes for external links
        if url.netloc != "www.mozilla.org":
            # add security measures
            rel = ' rel="external noopener"'
            # add analytics
            cta_text = _make_plain_text(node)
            data_cta = f' data-cta-type="link" data-cta-text="{cta_text}"'

        return f'<a href="{urlunparse(url)}{ref}"{data_cta}{rel}>{self._render_content(node)}</a>'


def _render_list(tag, content):
    return f"<{tag} class='mzp-u-list-styled'>{content}</{tag}>"


class UlRenderer(BaseBlockRenderer):
    def render(self, node):
        return _render_list("ul", self._render_content(node))


class OlRenderer(BaseBlockRenderer):
    def render(self, node):
        return _render_list("ol", self._render_content(node))


class LiRenderer(BaseBlockRenderer):
    def render(self, node):
        if _only_child(node, "text"):
            # The outer text node gets rendered as a paragraph... don't do that if there's only one p in the li
            return f"<li>{self._render_content(node['content'][0])}</li>"
        else:
            return f"<li>{self._render_content(node)}</li>"


class PRenderer(BaseBlockRenderer):
    def render(self, node):
        # contains only an empty text node
        if len(node["content"]) == 1 and node["content"][0]["nodeType"] == "text" and node["content"][0]["value"] == "":
            # just say no to empty p tags
            return ""
        else:
            return f"<p>{self._render_content(node)}</p>"


class InlineEntryRenderer(BaseNodeRenderer):
    def render(self, node):
        entry_id = node["data"]["target"]["sys"]["id"]
        entry = ContentfulPage.client.entry(entry_id)
        content_type = entry.sys["content_type"].id

        if content_type == "componentLogo":
            return _make_logo(entry)
        elif content_type == "componentWordmark":
            return _make_wordmark(entry)
        elif content_type == "componentCtaButton":
            return _make_cta_button(entry)
        else:
            return content_type


class AssetBlockRenderer(BaseBlockRenderer):
    IMAGE_HTML = '<img src="{src}" srcset="{src_highres} 1.5x" alt="{alt}" loading="lazy" />'

    def render(self, node):
        asset_id = node["data"]["target"]["sys"]["id"]
        asset = ContentfulPage.client.asset(asset_id)
        return self.IMAGE_HTML.format(
            src=_get_image_url(asset, 688),
            src_highres=_get_image_url(asset, 1376),
            alt=asset.description,
        )


class ContentfulPage:
    # TODO: List: stop list items from being wrapped in paragraph tags
    # TODO: Error/ Warn / Transform links to allizom
    client = get_client()
    _renderer = RichTextRenderer(
        {
            "hyperlink": LinkRenderer,
            "bold": StrongRenderer,
            "italic": EmphasisRenderer,
            "unordered-list": UlRenderer,
            "ordered-list": OlRenderer,
            "list-item": LiRenderer,
            "paragraph": PRenderer,
            "embedded-entry-inline": InlineEntryRenderer,
            "embedded-asset-block": AssetBlockRenderer,
        }
    )
    SPLIT_LAYOUT_CLASS = {
        "Even": "",
        "Narrow": "mzp-l-split-body-narrow",
        "Wide": "mzp-l-split-body-wide",
    }

    SPLIT_MEDIA_WIDTH_CLASS = {
        "Fill available width": "",
        "Fill available height": "mzp-l-split-media-constrain-height",
        "Overflow container": "mzp-l-split-media-overflow",
    }

    SPLIT_V_ALIGN_CLASS = {
        "Top": "mzp-l-split-v-start",
        "Center": "mzp-l-split-v-center",
        "Bottom": "mzp-l-split-v-end",
    }

    SPLIT_H_ALIGN_CLASS = {
        "Left": "mzp-l-split-h-start",
        "Center": "mzp-l-split-h-center",
        "Right": "mzp-l-split-h-end",
    }

    SPLIT_POP_CLASS = {
        "None": "",
        "Both": "mzp-l-split-pop",
        "Top": "mzp-l-split-pop-top",
        "Bottom": "mzp-l-split-pop-bottom",
    }
    CONTENT_TYPE_MAP = {
        "componentHero": {
            "proc": "get_hero_data",
            "css": "c-hero",
        },
        "componentSectionHeading": {
            "proc": "get_section_data",
            "css": "c-section-heading",
        },
        "componentSplitBlock": {
            "proc": "get_split_data",
            "css": "c-split",
        },
        "componentCallout": {
            "proc": "get_callout_data",
            "css": "c-call-out",
        },
        "layout2Cards": {"proc": "get_card_layout_data", "css": "c-card"},
        "layout3Cards": {"proc": "get_card_layout_data", "css": "c-card"},
        "layout4Cards": {"proc": "get_card_layout_data", "css": "c-card"},
        "layout5Cards": {"proc": "get_card_layout_data", "css": "c-card"},
        "layoutPictoBlocks": {
            "proc": "get_picto_layout_data",
            "css": ("c-picto", "t-multi-column"),
        },
        "textOneColumn": {
            "proc": "get_text_column_data_1",
            "css": "t-multi-column",
        },
        "textTwoColumns": {
            "proc": "get_text_column_data_2",
            "css": "t-multi-column",
        },
        "textThreeColumns": {
            "proc": "get_text_column_data_3",
            "css": "t-multi-column",
        },
        "textFourColumns": {
            "proc": "get_text_column_data_4",
            "css": "t-multi-column",
        },
    }

    def __init__(self, request, page_id):
        set_current_request(request)
        self.request = request
        self.page_id = page_id
        self.locale = get_locale(request)

    @cached_property
    def page(self):
        return self.client.entry(
            self.page_id,
            {
                "include": 10,
                "locale": self.locale,
                # ie, get ONLY the page for the specificed locale, as long as
                # the locale doesn't have a fallback configured in Contentful
            },
        )

    def render_rich_text(self, node):
        return self._renderer.render(node) if node else ""

    def _get_preview_image_from_fields(self, fields):
        if "preview_image" in fields:
            # TODO request proper size image
            preview_image_url = fields["preview_image"].fields().get("file", {}).get("url", {})
            if preview_image_url:
                return f"https:{preview_image_url}"

    def _get_info_data__slug_title_blurb(self, entry_fields, seo_fields):
        slug = entry_fields.get("slug", "home")  # TODO: check if we can use a better fallback
        title = entry_fields.get("title", "")
        title = entry_fields.get("preview_title", title)
        blurb = entry_fields.get("preview_blurb", "")

        if seo_fields:
            # Defer to SEO fields for blurb if appropriate.
            blurb = seo_fields.get("description", "")

        return {
            "slug": slug,
            "title": title,
            "blurb": blurb,
        }

    def _get_info_data__category_tags_classification(self, entry_fields, page_type):

        data = {}

        # TODO: Check with plans for Contentful use - we may
        # be able to relax this check and use it for page types
        # once we're in all-Compose mode
        if page_type == CONTENT_TYPE_PAGE_RESOURCE_CENTER:
            if "category" in entry_fields:
                data["category"] = entry_fields["category"]
            if "tags" in entry_fields:
                data["tags"] = entry_fields["tags"]
            if "product" in entry_fields:
                # NB: this is a re-mapping with an eye on flexibility - pages may not always have
                # a 'product' key, but they might have something regarding overall classification
                data["classification"] = entry_fields["product"]
        return data

    def _get_info_data__theme_campaign(self, entry_fields, slug):
        _folder = entry_fields.get("folder", "")
        _in_firefox = "firefox-" if "firefox" in _folder else ""
        campaign = f"{_in_firefox}{slug}"
        theme = "firefox" if "firefox" in _folder else "mozilla"
        return {
            "theme": theme,
            "campaign": campaign,
        }

    def _get_info_data__locale(self, page_type, entry_fields, entry_obj):
        # TODO: update this once we have a robust locale field available (ideally
        # via Compose's parent `page`), because double-purposing the "name" field
        # is a bit too brittle.
        if page_type == "pageHome":
            locale = entry_fields["name"]
        else:
            locale = entry_obj.sys["locale"]
        return {"locale": locale}

    def get_info_data(self, entry_obj, seo_obj=None):
        entry_fields = entry_obj.fields()
        if seo_obj:
            seo_fields = seo_obj.fields()
        else:
            seo_fields = None

        page_type = entry_obj.content_type.id

        data = {}

        data.update(self._get_info_data__slug_title_blurb(entry_fields, seo_fields))
        data.update(self._get_info_data__theme_campaign(entry_fields, data["slug"]))
        data.update(self._get_info_data__locale(page_type, entry_fields, entry_obj))
        campaign = data.pop("campaign")
        data.update(
            {
                # eg www.mozilla.org-firefox-accounts or www.mozilla.org-firefox-sync
                "utm_source": f"www.mozilla.org-{campaign}",
                "utm_campaign": campaign,  # eg firefox-sync
            }
        )

        _preview_image = self._get_preview_image_from_fields(entry_fields)
        if _preview_image:
            data["image"] = _preview_image

        if seo_fields:
            _preview_image = self._get_preview_image_from_fields(seo_fields)

            _seo_fields = deepcopy(seo_fields)  # NB: don't mutate the source dict
            if _preview_image:
                _seo_fields["image"] = _preview_image

            # We don't need the preview_image key if we've had it in the past, and
            # if reading it fails then we don't want it sticking around, either
            _seo_fields.pop("preview_image", None)
            data.update({"seo": _seo_fields})

        data.update(
            self._get_info_data__category_tags_classification(
                entry_fields,
                page_type,
            )
        )

        return data

    def get_content(self):
        # Check if it is a page or a connector
        entry_type = self.page.content_type.id
        seo_obj = None
        if entry_type == "connectHomepage":
            # Legacy - TODO: remove me once we're no longer using Connect: Homepage
            entry_obj = self.page.fields()["entry"]
        elif entry_type.startswith("page"):  # WARNING: this requires a consistent naming of page types in Contentful, too
            entry_obj = self.page
            seo_obj = self.page.seo
        else:
            raise ValueError(f"{entry_type} is not a recognized page type")

        if not entry_obj:
            raise Exception(f"No 'Entry' detected for {self.page.content_type.id}")

        self.request.page_info = self.get_info_data(
            entry_obj,
            seo_obj,
        )
        page_type = entry_obj.content_type.id
        page_css = set()
        page_js = set()
        fields = entry_obj.fields()
        content = None
        entries = []

        def proc(item):
            content_type = item.sys.get("content_type").id
            ctype_info = self.CONTENT_TYPE_MAP.get(content_type)
            if ctype_info:
                processor = getattr(self, ctype_info["proc"])
                entries.append(processor(item))
                css = ctype_info.get("css")
                if css:
                    if isinstance(css, str):
                        css = (css,)

                    page_css.update(css)

                js = ctype_info.get("js")
                if js:
                    if isinstance(js, str):
                        js = (js,)

                    page_js.update(js)

        if page_type == CONTENT_TYPE_PAGE_GENERAL:
            # look through all entries and find content ones
            for key, value in fields.items():
                if key == "component_hero":
                    proc(value)
                elif key == "body":
                    entries.append(self.get_text_data(value))
                elif key == "component_callout":
                    proc(value)
        elif page_type == CONTENT_TYPE_PAGE_RESOURCE_CENTER:
            # TODO: can we actually make this generic? Poss not: main_content is a custom field name
            _content = fields.get("main_content", {})
            entries.append(self.get_text_data(_content))
        else:
            # This covers pageVersatile, pageHome, etc
            content = fields.get("content")

        if content:
            # get components from content
            for item in content:
                proc(item)

        return {
            "page_type": page_type,
            "page_css": list(page_css),
            "page_js": list(page_js),
            "info": self.request.page_info,
            "entries": entries,
        }

    def get_text_data(self, value):
        data = {"component": "text", "body": self.render_rich_text(value), "width_class": _get_width_class("Medium")}  # TODO

        return data

    def get_hero_data(self, entry_obj):
        fields = entry_obj.fields()

        hero_image_url = _get_image_url(fields["image"], 800)
        hero_reverse = fields.get("image_side")
        hero_body = self.render_rich_text(fields.get("body"))

        product_class = _get_product_class(fields.get("product_icon")) if fields.get("product_icon") and fields.get("product_icon") != "None" else ""
        data = {
            "component": "hero",
            "theme_class": _get_theme_class(fields.get("theme")),
            "product_class": product_class,
            "title": fields.get("heading"),
            "tagline": fields.get("tagline"),
            "body": hero_body,
            "image": hero_image_url,
            "image_class": "mzp-l-reverse" if hero_reverse == "Left" else "",
            "include_cta": True if fields.get("cta") else False,
            "cta": _make_cta_button(fields.get("cta")) if fields.get("cta") else "",
        }

        return data

    def get_section_data(self, entry_obj):
        fields = entry_obj.fields()

        data = {
            "component": "sectionHeading",
            "heading": fields.get("heading"),
        }

        return data

    def get_split_data(self, entry_obj):
        fields = entry_obj.fields()
        # Checking if the split component is being used on the contentful homepage
        # If so, we will add a class to the body which will match the style of the depreciated hero component
        is_home_page = self.page.content_type.id == "pageHome"

        def get_split_class():
            block_classes = [
                "mzp-l-split-reversed" if fields.get("image_side") == "Left" else "",
                self.SPLIT_LAYOUT_CLASS.get(fields.get("body_width"), ""),
                self.SPLIT_POP_CLASS.get(fields.get("image_pop"), ""),
            ]
            return " ".join(block_classes)

        def get_body_class():
            body_classes = [
                self.SPLIT_V_ALIGN_CLASS.get(fields.get("body_vertical_alignment"), ""),
                self.SPLIT_H_ALIGN_CLASS.get(fields.get("body_horizontal_alignment"), ""),
                "c-home-body" if is_home_page else "",
            ]
            return " ".join(body_classes)

        def get_media_class():
            media_classes = [
                self.SPLIT_MEDIA_WIDTH_CLASS.get(fields.get("image_width"), ""),
                self.SPLIT_V_ALIGN_CLASS.get(fields.get("image_vertical_alignment"), ""),  # this field doesn't appear in Contentful Content Model
                self.SPLIT_H_ALIGN_CLASS.get(fields.get("image_horizontal_alignment"), ""),  # this field doesn't appear in Contentful Content Model
            ]
            return " ".join(media_classes)

        def get_mobile_class():
            mobile_display = fields.get("mobile_display")
            if not mobile_display:
                return ""

            mobile_classes = [
                "mzp-l-split-center-on-sm-md" if "Center content" in mobile_display else "",
                "mzp-l-split-hide-media-on-sm-md" if "Hide image" in mobile_display else "",
            ]
            return " ".join(mobile_classes)

        split_image_url = _get_image_url(fields["image"], 800)

        data = {
            "component": "split",
            "block_class": get_split_class(),
            "theme_class": _get_theme_class(fields.get("theme")),
            "body_class": get_body_class(),
            "body": self.render_rich_text(fields.get("body")),
            "media_class": get_media_class(),
            "media_after": fields.get("mobile_media_after"),
            "image": split_image_url,
            "mobile_class": get_mobile_class(),
        }
        return data

    def get_callout_data(self, entry_obj):
        fields = entry_obj.fields()

        data = {
            "component": "callout",
            "theme_class": _get_theme_class(fields.get("theme")),
            "product_class": _get_product_class(fields.get("product_icon")) if fields.get("product_icon") else "",
            "title": fields.get("heading"),
            "body": self.render_rich_text(fields.get("body")) if fields.get("body") else "",
            "cta": _make_cta_button(fields.get("cta")),
        }

        return data

    def get_card_data(self, entry_obj, aspect_ratio):
        # need a fallback aspect ratio
        aspect_ratio = aspect_ratio or "16:9"
        fields = entry_obj.fields()
        card_body = self.render_rich_text(fields.get("body")) if fields.get("body") else ""
        image_url = highres_image_url = ""

        if "image" in fields:
            card_image = fields.get("image")
            # TODO smaller image files when layout allows it
            if card_image:
                highres_image_url = _get_card_image_url(card_image, 800, aspect_ratio)
                image_url = _get_card_image_url(card_image, 800, aspect_ratio)

        if "you_tube" in fields:
            # TODO: add youtube JS to page_js
            youtube_id = _get_youtube_id(fields.get("you_tube"))
        else:
            youtube_id = ""

        data = {
            "component": "card",
            "heading": fields.get("heading"),
            "tag": fields.get("tag"),
            "link": fields.get("link"),
            "body": card_body,
            "aspect_ratio": _get_aspect_ratio_class(aspect_ratio) if image_url != "" else "",
            "highres_image_url": highres_image_url,
            "image_url": image_url,
            "youtube_id": youtube_id,
        }

        return data

    def get_large_card_data(self, entry_obj, card_obj):
        fields = entry_obj.fields()

        # get card data
        card_data = self.get_card_data(card_obj, "16:9")

        # large card data
        large_card_image = fields.get("image")
        if large_card_image:
            highres_image_url = _get_card_image_url(large_card_image, 1860, "16:9")
            image_url = _get_card_image_url(large_card_image, 1860, "16:9")

            # over-write with large values
            card_data["component"] = "large_card"
            card_data["highres_image_url"] = highres_image_url
            card_data["image_url"] = image_url

        return card_data

    def get_card_layout_data(self, entry_obj):
        fields = entry_obj.fields()
        aspect_ratio = fields.get("aspect_ratio")
        layout = entry_obj.sys.get("content_type").id

        data = {
            "component": "cardLayout",
            "layout_class": _get_layout_class(layout),
            "aspect_ratio": aspect_ratio,
            "cards": [],
        }

        follows_large_card = False
        if layout == "layout5Cards":
            card_layout_obj = fields.get("large_card")
            card_obj = fields.get("large_card").fields().get("card")
            large_card_data = self.get_large_card_data(card_layout_obj, card_obj)

            data.get("cards").append(large_card_data)
            follows_large_card = True

        cards = fields.get("content")
        for card in cards:
            if follows_large_card:
                this_aspect = "1:1"
                follows_large_card = False
            else:
                this_aspect = aspect_ratio
            card_data = self.get_card_data(card, this_aspect)
            data.get("cards").append(card_data)

        return data

    def get_picto_data(self, picto_obj, image_width):

        fields = picto_obj.fields()
        body = self.render_rich_text(fields.get("body")) if fields.get("body") else False

        if "icon" in fields:
            picto_image = fields.get("icon")
            image_url = _get_image_url(picto_image, image_width)
        else:
            image_url = ""  # TODO: this should cause an error, the macro requires an image

        return {
            "component": "picto",
            "heading": fields.get("heading"),
            "body": body,
            "image_url": image_url,
        }

    def get_picto_layout_data(self, entry):
        PICTO_ICON_SIZE = {
            "Small": 32,
            "Medium": 48,
            "Large": 64,
            "Extra Large": 96,
            "Extra Extra Large": 192,
        }
        fields = entry.fields()
        # layout = entry.sys.get('content_type').id

        def get_layout_class():
            column_class = _get_column_class(str(fields.get("blocks_per_row")))
            layout_classes = [
                _get_width_class(fields.get("width")),
                column_class or "3",
                "mzp-t-picto-side" if fields.get("icon_position") == "Side" else "",
                "mzp-t-picto-center" if fields.get("block_alignment") == "Center" else "",
                _get_theme_class(fields.get("theme")),
            ]

            return " ".join(layout_classes)

        image_width = PICTO_ICON_SIZE.get(fields.get("icon_size")) if fields.get("icon_size") else PICTO_ICON_SIZE.get("Large")

        data = {
            "component": "pictoLayout",
            "layout_class": get_layout_class(),
            "heading_level": fields.get("heading_level")[1:] if fields.get("heading_level") else 3,
            "image_width": image_width,
            "pictos": [],
        }

        pictos = fields.get("content")
        for picto_obj in pictos:
            picto_data = self.get_picto_data(picto_obj, image_width)
            data.get("pictos").append(picto_data)

        return data

    def get_text_column_data(self, cols, entry_obj):
        fields = entry_obj.fields()

        def get_content_class():
            content_classes = [
                _get_width_class(fields.get("width")),
                _get_column_class(str(cols)),
                _get_theme_class(fields.get("theme")),
                "mzp-u-center" if fields.get("block_alignment") == "Center" else "",
            ]

            return " ".join(content_classes)

        data = {
            "component": "textColumns",
            "layout_class": get_content_class(),
            "content": [self.render_rich_text(fields.get("body_column_one"))],
        }

        if cols > 1:
            data["content"].append(self.render_rich_text(fields.get("body_column_two")))
        if cols > 2:
            data["content"].append(self.render_rich_text(fields.get("body_column_three")))
        if cols > 3:
            data["content"].append(self.render_rich_text(fields.get("body_column_four")))

        return data

    get_text_column_data_1 = partialmethod(get_text_column_data, 1)
    get_text_column_data_2 = partialmethod(get_text_column_data, 2)
    get_text_column_data_3 = partialmethod(get_text_column_data, 3)
    get_text_column_data_4 = partialmethod(get_text_column_data, 4)


# TODO make optional fields optional
