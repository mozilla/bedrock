# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import hashlib
import hmac
import re
from collections import OrderedDict
from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, JsonResponse
from django.utils.cache import patch_response_headers
from django.utils.encoding import force_str
from django.views.decorators.http import require_safe

import querystringsafe_base64
from product_details.version_compare import Version

from bedrock.base.geo import get_country_from_request
from bedrock.base.urlresolvers import reverse
from bedrock.base.waffle import switch
from bedrock.contentful.api import ContentfulPage
from bedrock.firefox.firefox_details import (
    firefox_android,
    firefox_desktop,
    firefox_ios,
)
from bedrock.newsletter.forms import NewsletterFooterForm
from bedrock.releasenotes import version_re
from lib import l10n_utils
from lib.l10n_utils import L10nTemplateView, get_translations_native_names
from lib.l10n_utils.fluent import ftl, ftl_file_is_active

UA_REGEXP = re.compile(r"Firefox/(%s)" % version_re)

INSTALLER_CHANNElS = [
    "release",
    "beta",
    "alpha",
    "nightly",
    "aurora",  # deprecated name for dev edition
]
SEND_TO_DEVICE_MESSAGE_SETS = settings.SEND_TO_DEVICE_MESSAGE_SETS

STUB_VALUE_NAMES = [
    # name, default value
    ("utm_source", "(not set)"),
    ("utm_medium", "(direct)"),
    ("utm_campaign", "(not set)"),
    ("utm_content", "(not set)"),
    ("experiment", "(not set)"),
    ("variation", "(not set)"),
    ("ua", "(not set)"),
    ("client_id", "(not set)"),
    ("session_id", "(not set)"),
    ("dlsource", "mozorg"),
]
STUB_VALUE_RE = re.compile(r"^[a-z0-9-.%():_]+$", flags=re.IGNORECASE)


class InstallerHelpView(L10nTemplateView):
    template_name = "firefox/installer-help.html"
    ftl_files = ["firefox/installer-help"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        installer_lang = self.request.GET.get("installer_lang", None)
        installer_channel = self.request.GET.get("channel", None)
        ctx["installer_lang"] = None
        ctx["installer_channel"] = None

        if installer_lang and installer_lang in firefox_desktop.languages:
            ctx["installer_lang"] = installer_lang

        if installer_channel and installer_channel in INSTALLER_CHANNElS:
            if installer_channel == "aurora":
                ctx["installer_channel"] = "alpha"
            else:
                ctx["installer_channel"] = installer_channel

        return ctx


@require_safe
def stub_attribution_code(request):
    """Return a JSON response containing the HMAC signed stub attribution value"""
    if not request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"error": "Resource only available via XHR"}, status=400)

    response = None
    if not settings.STUB_ATTRIBUTION_RATE:
        # return as though it was rate limited, since it was
        response = JsonResponse({"error": "rate limited"}, status=429)
    elif not settings.STUB_ATTRIBUTION_HMAC_KEY:
        response = JsonResponse({"error": "service not configured"}, status=403)

    if response:
        patch_response_headers(response, 300)  # 5 min
        return response

    data = request.GET
    codes = OrderedDict()
    has_value = False
    for name, default_value in STUB_VALUE_NAMES:
        val = data.get(name, "")
        # remove utm_
        if name.startswith("utm_"):
            name = name[4:]

        if val and STUB_VALUE_RE.match(val):
            codes[name] = val
            has_value = True
        else:
            codes[name] = default_value

    if codes["source"] == "(not set)" and "referrer" in data:
        try:
            domain = urlparse(data["referrer"]).netloc
            if domain and STUB_VALUE_RE.match(domain):
                codes["source"] = domain
                codes["medium"] = "referral"
                has_value = True
        except Exception:
            # any problems and we should just ignore it
            pass

    if not has_value:
        codes["source"] = "www.mozilla.org"
        codes["medium"] = "(none)"

    code_data = sign_attribution_codes(codes)
    if code_data:
        response = JsonResponse(code_data)
    else:
        response = JsonResponse({"error": "Invalid code"}, status=400)

    patch_response_headers(response, 300)  # 5 min
    return response


def get_attrribution_code(codes):
    """
    Take the attribution codes and return the URL encoded string
    respecting max length.
    """
    code = "&".join("=".join(attr) for attr in codes.items())
    if len(codes["campaign"]) > 5 and len(code) > settings.STUB_ATTRIBUTION_MAX_LEN:
        # remove 5 char at a time
        codes["campaign"] = codes["campaign"][:-5] + "_"
        code = get_attrribution_code(codes)

    return code


def sign_attribution_codes(codes):
    """
    Take the attribution codes and return the base64 encoded string
    respecting max length and HMAC signature.
    """
    key = settings.STUB_ATTRIBUTION_HMAC_KEY
    code = get_attrribution_code(codes)
    if len(code) > settings.STUB_ATTRIBUTION_MAX_LEN:
        return None

    code = querystringsafe_base64.encode(code.encode())
    sig = hmac.new(key.encode(), code, hashlib.sha256).hexdigest()
    return {"attribution_code": code.decode(), "attribution_sig": sig}


@require_safe
def firefox_all(request):
    ftl_files = "firefox/all"
    product_android = firefox_android
    product_desktop = firefox_desktop
    product_ios = firefox_ios

    # Human-readable product labels
    products = OrderedDict(
        [
            ("desktop_release", ftl("firefox-all-product-firefox", ftl_files=ftl_files)),
            ("desktop_beta", ftl("firefox-all-product-firefox-beta", ftl_files=ftl_files)),
            ("desktop_developer", ftl("firefox-all-product-firefox-developer", ftl_files=ftl_files)),
            ("desktop_nightly", ftl("firefox-all-product-firefox-nightly", ftl_files=ftl_files)),
            ("desktop_esr", ftl("firefox-all-product-firefox-esr", ftl_files=ftl_files)),
            ("android_release", ftl("firefox-all-product-firefox-android", ftl_files=ftl_files)),
            ("android_beta", ftl("firefox-all-product-firefox-android-beta", ftl_files=ftl_files)),
            ("android_nightly", ftl("firefox-all-product-firefox-android-nightly", ftl_files=ftl_files)),
            ("ios_release", ftl("firefox-all-product-firefox-ios", ftl_files=ftl_files)),
        ]
    )

    channel_release = "release"
    channel_beta = "beta"
    channel_dev = "devedition"
    channel_nightly = "nightly"
    channel_esr = "esr"
    channel_esr_next = "esr_next"

    latest_release_version_desktop = product_desktop.latest_version(channel_release)
    latest_beta_version_desktop = product_desktop.latest_version(channel_beta)
    latest_developer_version_desktop = product_desktop.latest_version(channel_dev)
    latest_nightly_version_desktop = product_desktop.latest_version(channel_nightly)
    latest_esr_version_desktop = product_desktop.latest_version(channel_esr)
    latest_esr_next_version_desktop = product_desktop.latest_version(channel_esr_next)

    latest_release_version_android = product_android.latest_version(channel_release)
    latest_beta_version_android = product_android.latest_version(channel_beta)
    latest_nightly_version_android = product_android.latest_version(channel_nightly)
    latest_release_version_ios = product_ios.latest_version(channel_release)

    lang_multi = ftl("firefox-all-lang-multi", ftl_files=ftl_files)

    context = {
        "products": products.items(),
        "desktop_release_platforms": product_desktop.platforms(channel_release),
        "desktop_release_full_builds": product_desktop.get_filtered_full_builds(channel_release, latest_release_version_desktop),
        "desktop_release_channel_label": product_desktop.channel_labels.get(channel_release, "Firefox"),
        "desktop_release_latest_version": latest_release_version_desktop,
        "desktop_beta_platforms": product_desktop.platforms(channel_beta),
        "desktop_beta_full_builds": product_desktop.get_filtered_full_builds(channel_beta, latest_beta_version_desktop),
        "desktop_beta_channel_label": product_desktop.channel_labels.get(channel_beta, "Firefox"),
        "desktop_beta_latest_version": latest_beta_version_desktop,
        "desktop_developer_platforms": product_desktop.platforms(channel_dev),
        "desktop_developer_full_builds": product_desktop.get_filtered_full_builds(channel_dev, latest_developer_version_desktop),
        "desktop_developer_channel_label": product_desktop.channel_labels.get(channel_dev, "Firefox"),
        "desktop_developer_latest_version": latest_developer_version_desktop,
        "desktop_nightly_platforms": product_desktop.platforms(channel_nightly),
        "desktop_nightly_full_builds": product_desktop.get_filtered_full_builds(channel_nightly, latest_nightly_version_desktop),
        "desktop_nightly_channel_label": product_desktop.channel_labels.get(channel_nightly, "Firefox"),
        "desktop_nightly_latest_version": latest_nightly_version_desktop,
        "desktop_esr_platforms": product_desktop.platforms(channel_esr),
        "desktop_esr_full_builds": product_desktop.get_filtered_full_builds(channel_esr, latest_esr_version_desktop),
        "desktop_esr_channel_label": product_desktop.channel_labels.get(channel_esr, "Firefox"),
        "desktop_esr_latest_version": latest_esr_version_desktop,
        "android_release_platforms": [("android", "Android")],
        "android_release_full_builds": [
            {
                "locale": "multi",
                "name_en": lang_multi,
                "name_native": lang_multi,
                "platforms": {"android": {"download_url": settings.GOOGLE_PLAY_FIREFOX_LINK_UTMS}},
            }
        ],
        "android_release_channel_label": product_android.channel_labels.get(channel_release, "Firefox"),
        "android_release_latest_version": latest_release_version_android,
        "android_beta_platforms": [("android", "Android")],
        "android_beta_full_builds": [
            {
                "locale": "multi",
                "name_en": lang_multi,
                "name_native": lang_multi,
                "platforms": {"android": {"download_url": settings.GOOGLE_PLAY_FIREFOX_BETA_LINK}},
            }
        ],
        "android_beta_channel_label": product_android.channel_labels.get(channel_beta, "Firefox"),
        "android_beta_latest_version": latest_beta_version_android,
        "android_nightly_platforms": [("android", "Android")],
        "android_nightly_full_builds": [
            {
                "locale": "multi",
                "name_en": lang_multi,
                "name_native": lang_multi,
                "platforms": {"android": {"download_url": settings.GOOGLE_PLAY_FIREFOX_NIGHTLY_LINK}},
            }
        ],
        "android_nightly_channel_label": product_android.channel_labels.get(channel_nightly, "Firefox"),
        "android_nightly_latest_version": latest_nightly_version_android,
        "ios_release_platforms": [("ios", "iOS")],
        "ios_release_full_builds": [
            {
                "locale": "multi",
                "name_en": lang_multi,
                "name_native": lang_multi,
                "platforms": {"ios": {"download_url": settings.APPLE_APPSTORE_FIREFOX_LINK.replace("/{country}/", "/")}},
            }
        ],
        "ios_release_channel_label": product_ios.channel_labels.get(channel_release, "Firefox"),
        "ios_release_latest_version": latest_release_version_ios,
    }

    if latest_esr_next_version_desktop:
        context["desktop_esr_platforms_next"] = product_desktop.platforms(channel_esr_next, True)
        context["desktop_esr_full_builds_next"] = product_desktop.get_filtered_full_builds(channel_esr_next, latest_esr_next_version_desktop)
        context["desktop_esr_channel_label_next"] = (product_desktop.channel_labels.get(channel_esr_next, "Firefox"),)
        context["desktop_esr_next_version"] = latest_esr_next_version_desktop

    return l10n_utils.render(request, "firefox/all-unified.html", context, ftl_files=ftl_files)


def detect_channel(version):
    match = re.match(r"\d{1,3}", version)
    if match:
        num_version = int(match.group(0))
        if num_version >= 35:
            if version.endswith("a1"):
                return "nightly"
            if version.endswith("a2"):
                return "developer"
            if version.endswith("beta"):
                return "beta"

    return "unknown"


def show_57_dev_whatsnew(version):
    version = version[:-2]
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version("57.0")


def show_102_dev_whatsnew(version):
    version = version[:-2]
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version("102.0")


def show_57_dev_firstrun(version):
    version = version[:-2]
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version("57.0")


def redirect_old_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version < Version("40.0")


def show_default_account_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version("60.0")


class FirstrunView(L10nTemplateView):
    ftl_files_map = {
        "firefox/firstrun/firstrun.html": ["firefox/firstrun"],
        "firefox/developer/firstrun.html": ["firefox/developer"],
    }

    def get(self, *args, **kwargs):
        version = self.kwargs.get("version") or ""

        # redirect legacy /firstrun URLs to /firefox/new/
        if redirect_old_firstrun(version):
            return HttpResponsePermanentRedirect(reverse("firefox.new"))
        else:
            return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # add version to context for use in templates
        ctx["version"] = self.kwargs.get("version") or ""

        return ctx

    def get_template_names(self):
        version = self.kwargs.get("version") or ""

        if detect_channel(version) == "developer":
            if show_57_dev_firstrun(version):
                template = "firefox/developer/firstrun.html"
            else:
                template = "firefox/firstrun/firstrun.html"
        else:
            template = "firefox/firstrun/firstrun.html"

        # return a list to conform with original intention
        return [template]


class WhatsnewView(L10nTemplateView):
    ftl_files_map = {
        "firefox/developer/whatsnew.html": ["firefox/developer"],
        "firefox/developer/whatsnew-mdnplus.html": ["firefox/whatsnew/whatsnew-developer-mdnplus"],
        "firefox/nightly/whatsnew.html": ["firefox/nightly/whatsnew", "firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/index-account.html": ["firefox/whatsnew/whatsnew-account", "firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/index.html": ["firefox/whatsnew/whatsnew-s2d", "firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx114-en.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx114-en-gb.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx114-de.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx114-fr.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx115-eu-vpn.html": ["firefox/whatsnew/whatsnew-115-vpn", "firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx115-eu-ctd-de.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx115-eu-mobile-fr.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx115-eu-mobile-uk.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx115-na-windows.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx115-na-addons.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx116-na.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx116-uk.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx116-de.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx116-fr.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx117-de-reader-view.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx117-fr-reader-view.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx117-uk-reader-view.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx117-vpn.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx117-na-relay.html": ["firefox/whatsnew/whatsnew"],
    }

    # specific templates that should not be rendered in
    # countries where we can't advertise Mozilla VPN.
    vpn_excluded_templates = [
        "firefox/whatsnew/whatsnew-fx115-eu-vpn.html",
        "firefox/whatsnew/whatsnew-fx117-vpn.html",
    ]

    # place expected ?v= values in this list
    variations = ["1", "2", "3", "4"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        version = self.kwargs.get("version") or ""
        pre_release_channels = ["nightly", "developer", "beta"]
        channel = detect_channel(version)

        # add version to context for use in templates
        match = re.match(r"\d{1,3}", version)
        num_version = int(match.group(0)) if match else ""
        ctx["version"] = version
        ctx["num_version"] = num_version

        # add analytics parameters to context for use in templates
        if channel not in pre_release_channels:
            channel = ""

        analytics_version = str(num_version) + channel
        entrypoint = "mozilla.org-whatsnew" + analytics_version
        campaign = "whatsnew" + analytics_version
        ctx["analytics_version"] = analytics_version
        ctx["entrypoint"] = entrypoint
        ctx["campaign"] = campaign
        ctx["utm_params"] = f"utm_source={entrypoint}&utm_medium=referral&utm_campaign={campaign}&entrypoint={entrypoint}"

        variant = self.request.GET.get("v", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        ctx["variant"] = variant

        return ctx

    def get_template_names(self):
        country = get_country_from_request(self.request)
        locale = l10n_utils.get_locale(self.request)
        version = self.kwargs.get("version") or ""
        variant = self.request.GET.get("v", None)
        experience = self.request.GET.get("xv", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        oldversion = self.request.GET.get("oldversion", "")
        # old versions of Firefox sent a prefixed version
        if oldversion.startswith("rv:"):
            oldversion = oldversion[3:]

        channel = detect_channel(version)

        # Used by WNP 115
        vpn_wave_vi_countries = [
            "BG",  # Bulgaria
            "CY",  # Cyprus
            "CZ",  # Czech Republic
            "DK",  # Denmark
            "EE",  # Estonia
            "HR",  # Croatia
            "HU",  # Hungary
            "LT",  # Lithuania
            "LU",  # Luxembourg
            "LV",  # Latvia
            "MT",  # Malta
            "PL",  # Poland
            "PT",  # Portugal
            "RO",  # Romania
            "SI",  # Slovenia
            "SK",  # Slovakia
        ]

        if channel == "nightly":
            template = "firefox/nightly/whatsnew.html"
        elif channel == "developer":
            if show_102_dev_whatsnew(version):
                if switch("firefox-developer-whatsnew-mdnplus") and ftl_file_is_active("firefox/whatsnew/whatsnew-developer-mdnplus"):
                    template = "firefox/developer/whatsnew-mdnplus.html"
                else:
                    template = "firefox/developer/whatsnew.html"
            elif show_57_dev_whatsnew(version):
                template = "firefox/developer/whatsnew.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("117."):
            if country in WNP117_VPN_EXPANSION_COUNTRIES:
                template = "firefox/whatsnew/whatsnew-fx117-vpn.html"
            elif locale.startswith("en-"):
                if locale == "en-GB" or country == "GB":
                    template = "firefox/whatsnew/whatsnew-fx117-uk-reader-view.html"
                else:
                    if variant == "3":
                        template = "firefox/whatsnew/whatsnew-fx117-na-relay.html"
                    else:
                        template = "firefox/whatsnew/whatsnew-fx117-vpn.html"
            elif locale == "de":
                template = "firefox/whatsnew/whatsnew-fx117-de-reader-view.html"
            elif locale == "fr":
                template = "firefox/whatsnew/whatsnew-fx117-fr-reader-view.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("116."):
            if locale.startswith("en-"):
                if locale == "en-GB" or country == "GB":
                    template = "firefox/whatsnew/whatsnew-fx116-uk.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx116-na.html"
            elif locale == "de":
                template = "firefox/whatsnew/whatsnew-fx116-de.html"
            elif locale == "fr":
                template = "firefox/whatsnew/whatsnew-fx116-fr.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("115."):
            if locale.startswith("en-"):
                if experience == "windows":
                    template = "firefox/whatsnew/whatsnew-fx115-na-windows.html"
                elif locale == "en-GB":
                    template = "firefox/whatsnew/whatsnew-fx115-eu-mobile-uk.html"
                elif country == "GB":
                    template = "firefox/whatsnew/whatsnew-fx115-eu-mobile-uk.html"
                elif country in vpn_wave_vi_countries:
                    template = "firefox/whatsnew/whatsnew-fx115-eu-vpn.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx115-na-addons.html"
            elif country in vpn_wave_vi_countries:
                template = "firefox/whatsnew/whatsnew-fx115-eu-vpn.html"
            elif locale == "de":
                template = "firefox/whatsnew/whatsnew-fx115-eu-ctd-de.html"
            elif locale == "fr":
                template = "firefox/whatsnew/whatsnew-fx115-eu-mobile-fr.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("114."):
            if locale.startswith("en-"):
                if country == "GB" or locale == "en-GB":
                    template = "firefox/whatsnew/whatsnew-fx114-en-gb.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx114-en.html"
            elif locale == "de":
                template = "firefox/whatsnew/whatsnew-fx114-de.html"
            elif locale == "fr":
                template = "firefox/whatsnew/whatsnew-fx114-fr.html"
            else:
                template = "firefox/whatsnew/index.html"
        else:
            if show_default_account_whatsnew(version) and ftl_file_is_active("firefox/whatsnew/whatsnew-account"):
                template = "firefox/whatsnew/index-account.html"
            else:
                template = "firefox/whatsnew/index.html"

        # do not promote Mozilla VPN in excluded countries.
        if country in settings.VPN_EXCLUDED_COUNTRY_CODES and template in self.vpn_excluded_templates:
            template = "firefox/whatsnew/index-account.html"

        # return a list to conform with original intention
        return [template]


WNP117_VPN_EXPANSION_COUNTRIES = [
    "AT",  # Austria
    "BE",  # Belgium
    "BG",  # Bulgaria
    "CH",  # Switzerland
    "CY",  # Cyprus
    "CZ",  # Czech Republic
    "DK",  # Denmark
    "EE",  # Estonia
    "ES",  # Spain
    "FI",  # Finland
    "HR",  # Croatia
    "HU",  # Hungary
    "IE",  # Ireland
    "IT",  # Italy
    "LT",  # Lithuania
    "LU",  # Luxembourg
    "LV",  # Latvia
    "MT",  # Malta
    "NL",  # Netherlands
    "PL",  # Poland
    "PT",  # Portugal
    "RO",  # Romania
    "SE",  # Sweden
    "SI",  # Slovenia
    "SK",  # Slovakia
]


class DownloadThanksView(L10nTemplateView):
    ftl_files_map = {
        "firefox/new/basic/thanks.html": ["firefox/new/download"],
        "firefox/new/basic/thanks_direct.html": ["firefox/new/download"],
        "firefox/new/desktop/thanks.html": ["firefox/new/desktop"],
        "firefox/new/desktop/thanks_direct.html": ["firefox/new/desktop"],
    }
    activation_files = [
        "firefox/new/download",
        "firefox/new/desktop",
    ]

    # place expected ?v= values in this list
    variations = []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        variant = self.request.GET.get("v", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        ctx["variant"] = variant

        return ctx

    def get_template_names(self):
        experience = self.request.GET.get("xv", None)
        source = self.request.GET.get("s", None)

        if ftl_file_is_active("firefox/new/desktop") and experience != "basic":
            if source == "direct":
                template = "firefox/new/desktop/thanks_direct.html"
            else:
                template = "firefox/new/desktop/thanks.html"
        else:
            if source == "direct":
                template = "firefox/new/basic/thanks_direct.html"
            else:
                template = "firefox/new/basic/thanks.html"

        return [template]


class NewView(L10nTemplateView):
    ftl_files_map = {
        "firefox/new/basic/base_download.html": ["firefox/new/download"],
        "firefox/new/desktop/download.html": ["firefox/new/desktop"],
    }
    activation_files = [
        "firefox/new/download",
        "firefox/new/desktop",
    ]

    # place expected ?v= values in this list
    variations = []

    def get(self, *args, **kwargs):
        # Remove legacy query parameters (Bug 1236791)
        if self.request.GET.get("product", None) or self.request.GET.get("os", None):
            return HttpResponsePermanentRedirect(reverse("firefox.new"))

        scene = self.request.GET.get("scene", None)
        if scene == "2":
            # send to new permanent scene2 URL (bug 1438302)
            thanks_url = reverse("firefox.download.thanks")
            query_string = self.request.META.get("QUERY_STRING", "")
            if query_string:
                thanks_url = "?".join([thanks_url, force_str(query_string, errors="ignore")])
            return HttpResponsePermanentRedirect(thanks_url)

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # note: v and xv params only allow a-z, A-Z, 0-9, -, and _ characters
        variant = self.request.GET.get("v", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        ctx["variant"] = variant

        reason = self.request.GET.get("reason", None)
        manual_update = True if reason == "manual-update" else False
        ctx["manual_update"] = manual_update

        return ctx

    def get_template_names(self):
        variant = self.request.GET.get("v", None)
        experience = self.request.GET.get("xv", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        if ftl_file_is_active("firefox/new/desktop") and experience != "basic":
            template = "firefox/new/desktop/download.html"
        else:
            template = "firefox/new/basic/base_download.html"

        return [template]


class PlatformViewLinux(L10nTemplateView):
    # the base_platform template works with either platform.ftl or download.ftl active
    template_name = "firefox/new/basic/download_linux.html"

    ftl_files_map = {
        "firefox/new/basic/download_linux.html": ["firefox/new/platform", "firefox/new/download"],
    }

    # all active locales, this will make the lang switcher work properly
    activation_files = ["firefox/new/download", "firefox/new/platform"]


class PlatformViewMac(L10nTemplateView):
    # the base_platform template works with either platform.ftl or download.ftl active
    template_name = "firefox/new/basic/download_mac.html"

    ftl_files_map = {
        "firefox/new/basic/download_mac.html": ["firefox/new/platform", "firefox/new/download"],
    }

    # all active locales, this will make the lang switcher work properly
    activation_files = ["firefox/new/download", "firefox/new/platform"]


class PlatformViewWindows(L10nTemplateView):
    # the base_platform template works with either platform.ftl or download.ftl active
    template_name = "firefox/new/basic/download_windows.html"

    ftl_files_map = {
        "firefox/new/basic/download_windows.html": ["firefox/new/platform", "firefox/new/download"],
    }

    # all active locales, this will make the lang switcher work properly
    activation_files = ["firefox/new/download", "firefox/new/platform"]


@require_safe
def ios_testflight(request):
    action = settings.BASKET_SUBSCRIBE_URL

    # no country field, so no need to send locale
    newsletter_form = NewsletterFooterForm("ios-beta-test-flight", "")
    ctx = {"action": action, "newsletter_form": newsletter_form}

    return l10n_utils.render(request, "firefox/testflight.html", ctx)


class FirefoxHomeView(L10nTemplateView):
    ftl_files_map = {"firefox/home/index-master.html": ["firefox/home"], "firefox/challenge-the-default/landing-switch.html": ["firefox/home"]}

    # place expected ?v= values in this list
    variations = []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        variant = self.request.GET.get("v", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        ctx["variant"] = variant

        return ctx

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        variant = self.request.GET.get("v", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        if locale == "de":
            template_name = "firefox/challenge-the-default/landing-switch.html"
        else:
            template_name = "firefox/home/index-master.html"

        return [template_name]


BREACH_TIPS_URLS = {
    "de": "https://blog.mozilla.org/firefox/de/was-macht-man-nach-einem-datenleck/",
    "fr": "https://blog.mozilla.org/firefox/fr/que-faire-en-cas-de-fuite-de-donnees/",
    "en-CA": "https://blog.mozilla.org/firefox/what-to-do-after-a-data-breach/",
    "en-GB": "https://blog.mozilla.org/firefox/what-to-do-after-a-data-breach/",
    "en-US": "https://blog.mozilla.org/firefox/what-to-do-after-a-data-breach/",
}


@require_safe
def firefox_welcome_page1(request):
    locale = l10n_utils.get_locale(request)

    # get localized blog post URL for 2019 page
    breach_tips_query = (
        "?utm_source=mozilla.org-firefox-welcome-1&amp;utm_medium=referral"
        "&amp;utm_campaign=welcome-1-monitor&amp;entrypoint=mozilla.org-firefox-welcome-1"
    )
    breach_tips_url = BREACH_TIPS_URLS.get(locale, BREACH_TIPS_URLS["en-US"])

    context = {"breach_tips_url": breach_tips_url + breach_tips_query}

    template_name = "firefox/welcome/page1.html"

    return l10n_utils.render(request, template_name, context, ftl_files="firefox/welcome/page1")


@require_safe
def firefox_features_translate(request):
    to_translate_langs = [
        "af",
        "sq",
        "am-et",
        "ar",
        "hy-AM",
        "az",
        "eu",
        "be",
        "bn",
        "bs",
        "bg",
        "ca",
        "zh-CN",
        "hr",
        "cs",
        "da",
        "nl",
        "en-US",
        "eo",
        "et",
        "fi",
        "fr",
        "fy-NL",
        "gl",
        "ka",
        "de",
        "el",
        "gu",
        "ha",
        "he",
        "hi",
        "hu",
        "is",
        "ig",
        "id",
        "ga",
        "it",
        "ja",
        "kn",
        "kk",
        "km",
        "rw",
        "ko",
        "ku",
        "lo",
        "la",
        "lv",
        "lt",
        "mk",
        "mg",
        "ms",
        "ml",
        "mi",
        "mr",
        "mn",
        "my",
        "ne-NP",
        "nb-NO",
        "or",
        "fa",
        "pl",
        "pt-PT",
        "pa",
        "ro",
        "ru",
        "gd",
        "sr",
        "st",
        "si",
        "sk",
        "sl",
        "es",
        "sw",
        "sv-SE",
        "ta",
        "tt-RU",
        "te",
        "th",
        "tr",
        "uk",
        "ur",
        "uz",
        "vi",
        "cy",
        "xh",
        "yo",
        "zu",
    ]

    names = get_translations_native_names(sorted(to_translate_langs))

    context = {"context_test": names}

    template_name = "firefox/features/translate.html"

    return l10n_utils.render(request, template_name, context, ftl_files=["firefox/features/shared", "firefox/features/translate"])


class FirefoxContentful(L10nTemplateView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        content_id = ctx["content_id"]
        locale = l10n_utils.get_locale(self.request)
        page = ContentfulPage(content_id, locale)
        content = page.get_content()
        self.request.page_info = content["info"]
        ctx.update(content)
        return ctx

    def render_to_response(self, context, **response_kwargs):
        template = "firefox/contentful-all.html"

        return l10n_utils.render(self.request, template, context, **response_kwargs)
