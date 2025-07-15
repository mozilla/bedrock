# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.template.loader import render_to_string

import jinja2
from django_jinja import library
from markupsafe import Markup

from bedrock.base.urlresolvers import reverse
from bedrock.firefox.firefox_details import (
    firefox_android,
    firefox_desktop,
    firefox_ios,
)
from lib.l10n_utils import get_locale


def desktop_builds(
    channel,
    builds=None,
    locale=None,
    force_direct=False,
    force_full_installer=False,
    locale_in_transition=False,
    classified=False,
):
    builds = builds or []

    l_version = firefox_desktop.latest_builds(locale, channel)

    # Developer Edition is now based on the Beta channel, so the build list
    # should be generated from the Beta locales.
    if channel == "alpha":
        l_version = firefox_desktop.latest_builds(locale, "beta")

    if l_version:
        version, platforms = l_version
    else:
        locale = "en-US"
        version, platforms = firefox_desktop.latest_builds("en-US", channel)

    for plat_os, plat_os_pretty in firefox_desktop.platforms(channel, classified):
        os_pretty = plat_os_pretty

        # Firefox Nightly: The Windows stub installer is now universal,
        # automatically detecting a 32-bit and 64-bit desktop, so the
        # win64-specific entry can be skipped.
        if channel == "nightly":
            if plat_os == "win":
                continue
            if plat_os == "win64":
                plat_os = "win"
                os_pretty = "Windows 32/64-bit"

        # And generate all the info
        download_link = firefox_desktop.get_download_url(
            channel,
            version,
            plat_os,
            locale,
            force_direct=force_direct,
            force_full_installer=force_full_installer,
            locale_in_transition=locale_in_transition,
        )

        # If download_link_direct is False the data-direct-link attr
        # will not be output, and the JS won't attempt the IE popup.
        if force_direct:
            # no need to run get_download_url again with the same args
            download_link_direct = False
        else:
            download_link_direct = firefox_desktop.get_download_url(
                channel,
                version,
                plat_os,
                locale,
                force_direct=True,
                force_full_installer=force_full_installer,
            )
            if download_link_direct == download_link:
                download_link_direct = False

        builds.append({"os": plat_os, "os_pretty": os_pretty, "download_link": download_link, "download_link_direct": download_link_direct})

    return builds


def android_builds(channel, builds=None):
    builds = builds or []
    link = firefox_android.get_download_url(channel.lower())
    builds.append({"os": "android", "os_pretty": "Android", "download_link": link})

    return builds


def ios_builds(channel, builds=None):
    builds = builds or []
    link = firefox_ios.get_download_url(channel)
    builds.append({"os": "ios", "os_pretty": "iOS", "download_link": link})

    return builds


@library.global_function
@jinja2.pass_context
def download_firefox(
    ctx,
    channel="release",
    platform="all",
    dom_id=None,
    locale=None,
    force_direct=False,
    force_full_installer=False,
    alt_copy=None,
    button_class="mzp-t-xl",
    locale_in_transition=False,
    download_location=None,
):
    """Output a "download firefox" button.

    :param ctx: context from calling template.
    :param channel: name of channel: 'release', 'beta', 'alpha', or 'nightly'.
    :param platform: Target platform: 'desktop', 'android', 'ios', or 'all'.
    :param dom_id: Use this string as the id attr on the element.
    :param locale: The locale of the download. Default to locale of request.
    :param force_direct: Force the download URL to be direct.
    :param force_full_installer: Force the installer download to not be
            the stub installer (for aurora).
    :param alt_copy: Specifies alternate copy to use for download buttons.
    :param button_class: Classes to add to the download button, contains size mzp-t-xl by default
    :param locale_in_transition: Include the page locale in transitional download link.
    :param download_location: Specify the location of download button for
            GA reporting: 'primary cta', 'nav', 'sub nav', or 'other'.
    """
    show_desktop = platform in ["all", "desktop"]
    show_android = platform in ["all", "android"]
    show_ios = platform in ["all", "ios"]
    alt_channel = "" if channel == "release" else channel
    locale = locale or get_locale(ctx["request"])
    dom_id = dom_id or f"download-button-{'desktop' if platform == 'all' else platform}-{channel}"

    # Gather data about the build for each platform
    builds = []

    if show_desktop:
        version = firefox_desktop.latest_version(channel)
        builds = desktop_builds(channel, builds, locale, force_direct, force_full_installer, locale_in_transition)

    if show_android:
        version = firefox_android.latest_version(channel)
        builds = android_builds(channel, builds)

    if show_ios:
        version = firefox_ios.latest_version(channel)
        builds.append({"os": "ios", "os_pretty": "iOS", "download_link": firefox_ios.get_download_url()})

    # Get the native name for current locale
    langs = firefox_desktop.languages
    locale_name = langs[locale]["native"] if locale in langs else locale

    data = {
        "locale_name": locale_name,
        "version": version,
        "product": f"firefox-{platform}",
        "builds": builds,
        "id": dom_id,
        "channel": alt_channel,
        "show_desktop": show_desktop,
        "show_android": show_android,
        "show_ios": show_ios,
        "alt_copy": alt_copy,
        "button_class": button_class,
        "download_location": download_location,
        "fluent_l10n": ctx["fluent_l10n"],
    }

    html = render_to_string("firefox/includes/download-button.html", data, request=ctx["request"])
    return Markup(html)


@library.global_function
@jinja2.pass_context
def download_firefox_thanks(ctx, dom_id=None, locale=None, alt_copy=None, button_class=None, locale_in_transition=False, download_location=None):
    """Output a simple "download firefox" button that only points to /download/thanks/

    :param ctx: context from calling template.
    :param dom_id: Use this string as the id attr on the element.
    :param locale: The locale of the download. Default to locale of request.
    :param alt_copy: Specifies alternate copy to use for download buttons.
    :param button_class: Classes to add to the download button, contains size mzp-t-xl by default
    :param locale_in_transition: Include the page locale in transitional download link.
    :param download_location: Specify the location of download button for
            GA reporting: 'primary cta', 'nav', 'sub nav', or 'other'.
    """

    channel = "release"
    locale = locale or get_locale(ctx["request"])
    dom_id = dom_id or "download-button-thanks"
    transition_url = "/firefox/download/thanks/"
    version = firefox_desktop.latest_version(channel)

    if locale_in_transition:
        transition_url = f"/{locale}{transition_url}"

    download_link_direct = firefox_desktop.get_download_url(
        channel,
        version,
        "win",
        locale,
        force_direct=True,
        force_full_installer=False,
    )

    data = {
        "id": dom_id,
        "transition_url": transition_url,
        "download_link_direct": download_link_direct,
        "alt_copy": alt_copy,
        "button_class": button_class,
        "download_location": download_location,
        "fluent_l10n": ctx["fluent_l10n"],
    }

    html = render_to_string("firefox/includes/download-button-thanks.html", data, request=ctx["request"])
    return Markup(html)


@library.global_function
@jinja2.pass_context
def download_firefox_desktop_list(ctx, channel="release", dom_id=None, locale=None, force_full_installer=False):
    """
    Return a HTML list of platform download links for Firefox desktop

    :param channel: name of channel: 'release', 'beta',  'alpha' or 'nightly'.
    :param dom_id: Use this string as the id attr on the element.
    :param locale: The locale of the download. Default to locale of request.
    :param force_full_installer: Force the installer download to not be
            the stub installer (for aurora).

    """
    dom_id = dom_id or f"download-platform-list-{channel}"
    locale = locale or get_locale(ctx["request"])

    builds = desktop_builds(
        channel, builds=None, locale=locale, force_direct=True, force_full_installer=force_full_installer, locale_in_transition=False, classified=True
    )

    recommended_builds = []
    traditional_builds = []

    for plat in builds:
        # Add 32-bit label for Windows and Linux builds.
        if channel != "nightly":
            if plat["os"] == "win":
                plat["os_pretty"] = "Windows 32-bit"

        if plat["os"] == "linux":
            plat["os_pretty"] = "Linux 32-bit"

        if plat["os"] in firefox_desktop.platform_classification["recommended"] or channel == "nightly" and plat["os"] == "win":
            recommended_builds.append(plat)
        else:
            traditional_builds.append(plat)

    data = {
        "id": dom_id,
        "builds": {
            "recommended": recommended_builds,
            "traditional": traditional_builds,
        },
    }

    html = render_to_string("firefox/includes/download-list.html", data, request=ctx["request"])
    return Markup(html)


@library.global_function
def firefox_url(platform, page, channel=None):
    """
    Return a product-related URL like /firefox/all/ or /mobile/beta/notes/.

    Examples
    ========

    In Template
    -----------

        {{ firefox_url('desktop', 'all', 'organizations') }}
        {{ firefox_url('desktop', 'sysreq', channel) }}
        {{ firefox_url('android', 'notes') }}
    """

    kwargs = {}

    # Tweak the channel name for the naming URL pattern in urls.py
    if channel == "release":
        channel = None
    if channel == "alpha":
        if platform == "desktop":
            channel = "developer"
        if platform == "android":
            channel = "aurora"
    if channel == "esr":
        channel = "organizations"

    # There is now only one /all page URL - issue 8096
    if page == "all":
        if platform == "desktop":
            if channel == "beta":
                product = "desktop-beta"
            elif channel == "developer":
                product = "desktop-developer"
            elif channel == "nightly":
                product = "desktop-nightly"
            elif channel == "organizations":
                product = "desktop-esr"
            else:
                product = "desktop-release"
        elif platform == "android":
            if channel == "beta":
                product = "android-beta"
            elif channel == "nightly":
                product = "android-nightly"
            else:
                product = "android-release"
    else:
        if channel:
            kwargs["channel"] = channel
        if platform != "desktop":
            kwargs["platform"] = platform

    # Firefox for Android and iOS have the system requirements page on SUMO
    if platform in ["android", "ios"] and page == "sysreq":
        return settings.FIREFOX_MOBILE_SYSREQ_URL

    if page == "all" and product:
        kwargs["product_slug"] = product
        return reverse("firefox.all.platforms", kwargs=kwargs)

    return reverse(f"firefox.{page}", kwargs=kwargs)


@library.global_function
@jinja2.pass_context
def send_to_device(
    ctx,
    platform="all",
    message_set="default",
    dom_id="send-to-device",
    class_name="vertical",
    include_title=True,
    title_text=None,
    input_label=None,
    legal_note_email=None,
    spinner_color="#000",
    button_class=None,
):
    """
    Render a send-to-device form for sending a Firefox download link
    from your desktop web browser to your mobile device.

    Examples
    ========

    In Template
    -----------

        {{ send_to_device(message_set='default', platform='all') }}
    """

    request = ctx["request"]
    context = ctx.get_all()
    basket_url = settings.BASKET_SUBSCRIBE_URL

    if not platform:
        platform = "all"

    if message_set not in settings.SEND_TO_DEVICE_MESSAGE_SETS:
        MESSAGES = settings.SEND_TO_DEVICE_MESSAGE_SETS["default"]
    else:
        MESSAGES = settings.SEND_TO_DEVICE_MESSAGE_SETS[message_set]

    if platform not in MESSAGES["email"]:
        newsletters = MESSAGES["email"]["all"]
    else:
        newsletters = MESSAGES["email"][platform]

    context.update(
        dict(
            basket_url=basket_url,
            button_class=button_class,
            class_name=class_name,
            dom_id=dom_id,
            include_title=include_title,
            input_label=input_label,
            legal_note_email=legal_note_email,
            message_set=message_set,
            newsletters=newsletters,
            platform=platform,
            spinner_color=spinner_color,
            title_text=title_text,
        )
    )

    html = render_to_string("firefox/includes/send-to-device.html", context, request=request)
    return Markup(html)


@library.global_function
@jinja2.pass_context
def firefox_com_canonical_tag(ctx, dest_path=None, root_url=settings.FXC_BASE_URL):
    """Create a <rel='canonical'...> link based on the URL of the current page, but swapping the
    hostname for firefox.com (by default).

    By default uses the same path as the current URL
    By default targets FXC_BASE_URL (firefox.com) as the target root_url

    Examples
    ========

    In Template
    -----------

        {{ firefox_com_canonical_tag() }}
        {{ firefox_com_canonical_tag(dest_path="/some/alernative/path") }}
        {{ firefox_com_canonical_tag(dest_path="/some/alernative/path", root_url="https://getfirefox.de") }}
        {{ firefox_com_canonical_tag(root_url="https://some-subdomain.firefox.com") }}

    """
    if settings.ENABLE_FIREFOX_COM_REDIRECTS is False:
        return ""

    request = ctx["request"]

    _path = request.path if not dest_path else dest_path

    html = f'<link rel="canonical" href="{root_url}{_path}">'

    return Markup(html)
