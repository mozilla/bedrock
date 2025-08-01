# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# coding: utf-8

import re
import urllib.parse
from os import path
from os.path import splitext

from django.conf import settings
from django.contrib.staticfiles.finders import find as find_static
from django.template.defaultfilters import slugify as django_slugify
from django.template.defaulttags import CsrfTokenNode
from django.template.loader import render_to_string
from django.utils.encoding import smart_str

import bleach
import jinja2
from django_jinja import library
from markupsafe import Markup
from product_details import product_details

from bedrock.base.templatetags.helpers import static, urlparams

ALL_FX_PLATFORMS = ("windows", "linux", "mac", "android", "ios")


@library.global_function
def needs_data_consent(country_code):
    """
    Global helper that can be passed a country_code via a template
    in order to determine if cookie consent banner should be shown.
    """
    country_list = settings.DATA_CONSENT_COUNTRIES
    return country_code in country_list


def _strip_img_prefix(url):
    return re.sub(r"^/?img/", "", url)


def _l10n_media_exists(type, locale, url):
    """checks if a localized media file exists for the locale"""
    return find_static(path.join(type, "l10n", locale, url)) is not None


def add_string_to_image_url(url, addition):
    """Add the platform string to an image url."""
    filename, ext = splitext(url)
    return "".join([filename, "-", addition, ext])


def convert_to_high_res(url):
    """Convert a file name to the high-resolution version."""
    return add_string_to_image_url(url, "high-res")


def l10n_img_file_name(ctx, url):
    """Return the filename of the l10n image for use by static()"""
    url = url.lstrip("/")
    locale = getattr(ctx["request"], "locale", None)
    if not locale:
        locale = settings.LANGUAGE_CODE

    # We use the same localized screenshots for all Spanishes
    if locale.startswith("es") and not _l10n_media_exists("img", locale, url):
        locale = "es-ES"

    if locale != settings.LANGUAGE_CODE:
        if not _l10n_media_exists("img", locale, url):
            locale = settings.LANGUAGE_CODE

    return path.join("img", "l10n", locale, url)


@library.global_function
@jinja2.pass_context
def l10n_img(ctx, url):
    """Output the url to a localized image.

    Uses the locale from the current request. Checks to see if the localized
    image exists, and falls back to the image for the default locale if not.

    Examples
    ========

    In Template
    -----------

        {{ l10n_img('firefoxos/screenshot.png') }}

    For en-US this would output:

        {{ static('img/l10n/en-US/firefox/screenshot.png') }}

    For fr this would output:

        {{ static('img/l10n/fr/firefox/screenshot.png') }}

    If that file did not exist it would default to the en-US version (if en-US
    was the default language for this install).

    In the Filesystem
    -----------------

    Put files in folders like the following::

        $ROOT/media/img/l10n/en-US/firefoxos/screenshot.png
        $ROOT/media/img/l10n/fr/firefoxos/screenshot.png

    """
    url = _strip_img_prefix(url)
    return static(l10n_img_file_name(ctx, url))


@library.global_function
@jinja2.pass_context
def l10n_css(ctx):
    """
    Output the URL to a locale-specific stylesheet if exists.

    Examples
    ========

    In Template
    -----------

        {{ l10n_css() }}

    For a locale that has locale-specific stylesheet, this would output:

        <link rel="stylesheet" media="screen,projection,tv"
              href="{{ STATIC_URL }}css/l10n/{{ LANG }}/intl.css">

    For a locale that doesn't have any locale-specific stylesheet, this would
    output nothing.

    In the Filesystem
    -----------------

    Put files in folders like the following::

        $ROOT/media/css/l10n/en-US/intl.css
        $ROOT/media/css/l10n/fr/intl.css

    """
    locale = getattr(ctx["request"], "locale", "en-US")

    if _l10n_media_exists("css", locale, "intl.css"):
        markup = '<link rel="stylesheet" media="screen,projection,tv" href="%s">' % static(path.join("css", "l10n", locale, "intl.css"))
    else:
        markup = ""

    return Markup(markup)


@library.global_function
def field_with_attrs(bfield, **kwargs):
    """Allows templates to dynamically add html attributes to bound
    fields from django forms"""
    bfield.field.widget.attrs.update(kwargs)
    return bfield


@library.global_function
@jinja2.pass_context
def resp_img(ctx={}, url=None, srcset=None, sizes=None, optional_attributes=None):
    alt = ""
    attrs = ""
    final_sizes = ""
    final_srcset = ""
    l10n = False
    loading = ""

    if optional_attributes:
        l10n = optional_attributes.pop("l10n", False)
        alt = optional_attributes.pop("alt", "")

        # Put `loading` before `src` to avoid a bug in Firefox. (https://bugzilla.mozilla.org/show_bug.cgi?id=1647077)
        if "loading" in optional_attributes:
            loading = f'loading="{optional_attributes.pop("loading", "")}" '

        if optional_attributes:
            attrs = " " + " ".join(f'{attr}="{val}"' for attr, val in optional_attributes.items())

    # default src
    if not url.startswith("https://"):
        url = l10n_img(ctx, url) if l10n else static(url)

    if srcset:
        srcset_last_item = list(srcset)[-1]
        for image, size in srcset.items():
            postfix = "" if image == srcset_last_item else ","
            if not image.startswith("https://"):
                image = l10n_img(ctx, image) if l10n else static(image)
            final_srcset = final_srcset + image + " " + size + postfix

    if sizes:
        sizes_last_item = list(sizes)[-1]
        for window_size, img_width in sizes.items():
            postfix = "" if window_size == sizes_last_item else ","

            if window_size == "default":
                final_sizes = final_sizes + img_width + postfix
            else:
                final_sizes = final_sizes + window_size + " " + img_width + postfix

    srcset_str = f'srcset="{final_srcset}" ' if final_srcset else ""
    sizes_str = f'sizes="{final_sizes}" ' if final_sizes else ""
    markup = f'<img {loading}src="{url}" {srcset_str}{sizes_str}alt="{alt}"{attrs}>'

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def picture(ctx={}, url=None, sources=[], optional_attributes=None):
    alt = ""
    attrs = ""
    final_sources = []
    l10n = False
    loading = ""

    if optional_attributes:
        l10n = optional_attributes.pop("l10n", False)
        alt = optional_attributes.pop("alt", "")

        # Put `loading` before `src` to avoid a bug in Firefox. (https://bugzilla.mozilla.org/show_bug.cgi?id=1647077)
        if "loading" in optional_attributes:
            loading = f'loading="{optional_attributes.pop("loading", "")}" '

        if optional_attributes:
            attrs = " " + " ".join(f'{attr}="{val}"' for attr, val in optional_attributes.items())

    # default src
    if not url.startswith("https://"):
        url = l10n_img(ctx, url) if l10n else static(url)

    # sources
    for source in sources:
        final_srcset = ""
        final_sizes = ""
        source_media = source.pop("media", False)
        source_srcset = source.pop("srcset", False)
        source_type = source.pop("type", False)
        source_sizes = source.pop("sizes", False)
        source_width = source.pop("width", False)
        source_height = source.pop("height", False)

        # srcset
        if source_srcset:
            srcset_last_item = list(source_srcset)[-1]
            for image, descriptor in source_srcset.items():
                postfix = "" if image == srcset_last_item else ","
                if not image.startswith("https://"):
                    image = l10n_img(ctx, image) if l10n else static(image)
                if descriptor == "default":
                    final_srcset = final_srcset + image + postfix
                else:
                    final_srcset = final_srcset + image + " " + descriptor + postfix

        # sizes
        if source_sizes:
            sizes_last_item = list(source_sizes)[-1]
            for window_size, img_width in source_sizes.items():
                postfix = "" if window_size == sizes_last_item else ","

                if window_size == "default":
                    final_sizes = final_sizes + img_width + postfix
                else:
                    final_sizes = final_sizes + window_size + " " + img_width + postfix

        media_markup = f' media="{source_media}"' if source_media else ""
        type_markup = f' type="{source_type}"' if source_type else ""
        srcset_markup = f' srcset="{final_srcset}"' if final_srcset != "" else ""
        sizes_markup = f' sizes="{final_sizes}"' if final_sizes != "" else ""
        width_markup = f' width="{source_width}"' if source_width else ""
        height_markup = f' height="{source_height}"' if source_height else ""
        source_markup = f"<source{media_markup}{type_markup}{srcset_markup}{sizes_markup}{width_markup}{height_markup}>"
        final_sources.append(source_markup)

    markup = f'<picture>{"".join(final_sources)}<img {loading}src="{url}" alt="{alt}"{attrs}></picture>'

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def video(ctx, *args, **kwargs):
    """
    HTML5 Video tag helper.

    Accepted kwargs:
    prefix, w, h, autoplay, poster, preload, id

    Use like this:
    {{ video('http://example.com/myvid.mp4', 'http://example.com/myvid.webm',
             poster='http://example.com/myvid.jpg',
             w=640, h=360) }}

    You can also use a prefix like:
    {{ video('myvid.mp4', 'myvid.webm', prefix='http://example.com') }}

    The prefix does not apply to the poster attribute.

    Finally, MIME type detection happens by file extension. Supported: webm,
    mp4, ogv. If you want anything else, patches welcome.
    """

    filetypes = ("webm", "ogv", "mp4")
    mime = {"webm": "video/webm", "ogv": 'video/ogg; codecs="theora, vorbis"', "mp4": "video/mp4"}

    videos = {}
    for v in args:
        try:
            ext = v.rsplit(".", 1)[1].lower()
        except IndexError:
            # TODO: Perhaps we don't want to swallow this quietly in the future
            continue
        if ext not in filetypes:
            continue
        videos[ext] = v if "prefix" not in kwargs else urllib.parse.urljoin(kwargs["prefix"], v)

    if not videos:
        return ""

    # defaults
    data = {
        "w": 640,
        "h": 360,
        "autoplay": False,
        "preload": False,
        "id": "htmlPlayer",
        "fluent_l10n": ctx["fluent_l10n"],
    }

    data.update(**kwargs)
    data.update(filetypes=filetypes, mime=mime, videos=videos)

    return Markup(render_to_string("mozorg/videotag.html", data, request=ctx["request"]))


@library.global_function
@jinja2.pass_context
def donate_url(ctx, location=""):
    """Output a formatted donation link to the donation popup form.

    Location parameter indicates the page or position of the link for attribution.
    The value must be preconfigured in FundraiseUp before it can be accepted.
    Undefined values will not trigger the donation widget.
    If no location parameter is supplied the fallback URL is the standalone
    /donate/ page.

    Examples
    ========

    In Template
    -----------

        {{ donate_url() }}

    This would output:

        https://foundation.mozilla.org/donate/

        {{ donate(location='contribute')}}

    This would output:

        https://foundation.mozilla.org/?form=contribute

    """

    location = "?form=" + location if location else "donate/"

    return settings.DONATE_LINK.format(location=location)


@library.global_function
@jinja2.pass_context
def mozilla_instagram_url(ctx):
    """Output a link to Instagram taking locales into account.

    Uses the locale from the current request. Checks to see if we have
    a Instagram account that match this locale, returns the localized account
    url or falls back to the US account url if not.

    Examples
    ========

    In Template
    -----------

        {{ mozilla_instagram_url() }}

    For en-US this would output:

        https://www.instagram.com/mozilla/

    For DE this would output:

        https://www.instagram.com/mozilla_deutschland/

    """
    locale = getattr(ctx["request"], "locale", "en-US")
    if locale not in settings.MOZILLA_INSTAGRAM_ACCOUNTS:
        locale = "en-US"

    return settings.MOZILLA_INSTAGRAM_ACCOUNTS[locale]


@library.filter
def absolute_url(url):
    """
    Return a fully qualified URL including a protocol especially for the Open
    Graph Protocol image object.

    Examples
    ========

    In Template
    -----------
    This filter can be used in combination with the static helper like this:

        {{ static('path/to/img')|absolute_url }}

    With a block:

        {% filter absolute_url %}
          {% block page_image %}{{ static('path/to/img') }}{% endblock %}
        {% endfilter %}
    """

    if url.startswith("//"):
        prefix = "https:"
    elif url.startswith("/"):
        prefix = settings.CANONICAL_URL
    else:
        prefix = ""

    return prefix + url


@library.filter
def htmlattr(_list, **kwargs):
    """
    Assign an attribute to elements, like jQuery's attr function. The _list
    argument is a BeautifulSoup iterable object. Note that such a code doesn't
    work in a Jinja2 template:

        {% set body.p['id'] = 'great' %}
        {% set body.p['class'] = 'awesome' %}

    Instead, use this htmlattr function like

        {{ body.p|htmlattr(id='great', class='awesome') }}

    """
    for tag in _list:
        for attr, value in kwargs.items():
            tag[attr] = value

    return _list


@library.filter
def slugify(text):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    return django_slugify(text)


@library.filter
def bleach_tags(text):
    return bleach.clean(text, tags=set(), strip=True).replace("&amp;", "&")


# from jingo


@library.global_function
@jinja2.pass_context
def csrf(context):
    """Equivalent of Django's ``{% crsf_token %}``."""
    return Markup(CsrfTokenNode().render(context))


@library.filter
def f(s, *args, **kwargs):
    """
    Uses ``str.format`` for string interpolation.

    **Note**: Always converts to s to text type before interpolation.

    >>> {{ "{0} arguments and {x} arguments"|f('positional', x='keyword') }}
    "positional arguments and keyword arguments"
    """
    s = str(s)
    return s.format(*args, **kwargs)


@library.filter
def datetime(t, fmt=None):
    """Call ``datetime.strftime`` with the given format string."""
    if fmt is None:
        fmt = "%B %e, %Y"
    return smart_str(t.strftime(fmt)) if t else ""


@library.filter
def ifeq(a, b, text):
    """Return ``text`` if ``a == b``."""
    return Markup(text if a == b else "")


@library.global_function
@jinja2.pass_context
def app_store_url(ctx, product, campaign=None):
    """Returns a localised app store URL for a given product"""
    locale = getattr(ctx["request"], "locale", "en-US")
    countries = settings.APPLE_APPSTORE_COUNTRY_MAP
    params = "?pt=373246&ct={cmp}&mt=8"

    if product == "focus" and locale == "de":
        base_url = getattr(settings, "APPLE_APPSTORE_KLAR_LINK")
    else:
        base_url = getattr(settings, f"APPLE_APPSTORE_{product.upper()}_LINK")

    if campaign:
        base_url = base_url + params.format(cmp=campaign)

    if locale in countries:
        return base_url.format(country=countries[locale])
    else:
        return base_url.replace("/{country}/", "/")


@library.global_function
@jinja2.pass_context
def play_store_url(ctx, product, campaign=None):
    """Returns a localised play store URL for a given product"""
    locale = lang_short(ctx)
    base_url = getattr(settings, f"GOOGLE_PLAY_{product.upper()}_LINK")
    params = "&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3D{cmp}"

    if product == "focus" and locale == "de":
        base_url = getattr(settings, "GOOGLE_PLAY_KLAR_LINK")
    else:
        base_url = getattr(settings, f"GOOGLE_PLAY_{product.upper()}_LINK")

    if campaign:
        base_url = base_url + params.format(cmp=campaign)

    if locale:
        base_url = base_url + f"&hl={locale}"

    return base_url


@library.global_function
@jinja2.pass_context
def ms_store_url(ctx, product="firefox", mode="mini", campaign=None, handler=None):
    """
    Returns a Microsoft Windows Store URL for a given product.
    Installer mode parameter options include "direct" or "full", or "mini".
    See https://apps.microsoft.com/badge for details.
    """

    if handler == "ms-windows-store":
        base_url = getattr(settings, f"MICROSOFT_WINDOWS_STORE_{product.upper()}_DIRECT_LINK")
    else:
        base_url = getattr(settings, f"MICROSOFT_WINDOWS_STORE_{product.upper()}_WEB_LINK")

    params = {
        "mode": mode,
        "cid": campaign,
    }

    return urlparams(base_url, **params)


@library.global_function
@jinja2.pass_context
def lang_short(ctx):
    """Returns a shortened locale code e.g. en."""
    locale = getattr(ctx["request"], "locale", "en-US")
    return locale.split("-")[0]


@library.global_function
@jinja2.pass_context
def native_language_name(ctx):
    """Returns translated native language name e.g. `tr` locale would render `Türkçe`"""
    locale = getattr(ctx["request"], "locale", "en-US")
    language = product_details.languages.get(locale)
    return language["native"] if language else locale


def _fxa_product_url(product_url, entrypoint, optional_parameters=None):
    separator = "&" if "?" in product_url else "?"
    url = f"{product_url}{separator}entrypoint={entrypoint}&form_type=button&utm_source={entrypoint}&utm_medium=referral"

    if optional_parameters:
        params = "&".join(f"{param}={val}" for param, val in optional_parameters.items())
        url += f"&{params}"

    return url


def _fxa_product_button(
    product_url,
    entrypoint,
    button_text,
    class_name=None,
    is_button_class=True,
    include_metrics=True,
    optional_parameters=None,
    optional_attributes=None,
):
    href = _fxa_product_url(product_url, entrypoint, optional_parameters)
    css_class = "js-fxa-cta-link"
    attrs = ""

    if optional_attributes:
        attrs += " ".join(f'{attr}="{val}"' for attr, val in optional_attributes.items())

    if include_metrics:
        css_class += " js-fxa-product-button"

    if is_button_class:
        css_class += " mzp-c-button mzp-t-product"

    if class_name:
        css_class += f" {class_name}"

    markup = f'<a href="{href}" data-action="{settings.FXA_ENDPOINT}" class="{css_class}" {attrs}>{button_text}</a>'

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def monitor_fxa_button(
    ctx, entrypoint, button_text, class_name=None, is_button_class=True, include_metrics=True, optional_parameters=None, optional_attributes=None
):
    """
    Render a monitor.mozilla.org link with required params for Mozilla account authentication.

    Examples
    ========

    In Template
    -----------

        {{ monitor_fxa_button(entrypoint='mozilla.org-firefox-accounts', button_text='Sign In to Monitor') }}
    """
    product_url = "https://monitor.mozilla.org/user/dashboard"
    return _fxa_product_button(
        product_url, entrypoint, button_text, class_name, is_button_class, include_metrics, optional_parameters, optional_attributes
    )


@library.global_function
@jinja2.pass_context
def relay_fxa_button(
    ctx, entrypoint, button_text, class_name=None, is_button_class=True, include_metrics=True, optional_parameters=None, optional_attributes=None
):
    """
    Render a relay.firefox.com link with required params for Mozilla account authentication.

    Examples
    ========

    In Template
    -----------

        {{ relay_fxa_button(entrypoint='mozilla.org-firefox-accounts', button_text='Sign In to Relay') }}
    """
    product_url = settings.RELAY_PRODUCT_URL + "accounts/fxa/login/?process=login"
    return _fxa_product_button(
        product_url, entrypoint, button_text, class_name, is_button_class, include_metrics, optional_parameters, optional_attributes
    )


@library.global_function
@jinja2.pass_context
def fxa_link_fragment(ctx, entrypoint, action="signup", optional_parameters=None):
    """
    Returns `href` attribute as a string fragment. This is useful for inline links
    that appear inside a string of localized copy, such as a paragraph.

    Examples
    ========

    In Template
    -----------

        {% set signin = fxa_link_fragment(entrypoint='mozilla.org-firefox-accounts') %}
        {% set class_name = 'js-fxa-cta-link js-fxa-product-button' %}
        <p>Already have an account? <a {{ sign_in }} class="{{ class_name }}">Sign In</a> to start syncing.</p>
    """

    if action == "email":
        action = "?action=email"

    fxa_url = _fxa_product_url(f"{settings.FXA_ENDPOINT}{action}", entrypoint, optional_parameters)

    markup = f'href="{fxa_url}"'

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def fxa_button(
    ctx,
    entrypoint,
    button_text,
    action="signup",
    class_name=None,
    is_button_class=True,
    include_metrics=True,
    optional_parameters=None,
    optional_attributes=None,
):
    """
    Render a accounts.firefox.com link with required params for Mozilla account authentication.

    Examples
    ========

    In Template
    -----------

        {{ fxa_button(entrypoint='mozilla.org-firefox-accounts', button_text='Sign In') }}
    """

    if action == "email":
        action = "?action=email"

    product_url = f"{settings.FXA_ENDPOINT}{action}"

    optional_attributes = optional_attributes or {}

    return _fxa_product_button(
        product_url, entrypoint, button_text, class_name, is_button_class, include_metrics, optional_parameters, optional_attributes
    )
