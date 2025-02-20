# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import hashlib
import hmac
import re
from collections import OrderedDict
from urllib.parse import urlparse

from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect, JsonResponse
from django.utils.cache import patch_response_headers
from django.utils.encoding import force_str
from django.views.decorators.http import require_safe

import querystringsafe_base64
from product_details import product_details
from product_details.version_compare import Version

from bedrock.base.geo import get_country_from_request
from bedrock.base.templatetags.helpers import urlparams
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
    ("client_id_ga4", "(not set)"),
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
def firefox_all(request, product_slug=None, platform=None, locale=None):
    ftl_files = "firefox/all"

    # A product object for android OR ios.
    class MobileRelease:
        slug = "mobile-release"

    mobile_release = MobileRelease()

    product_map = {
        "desktop-release": {
            "slug": "desktop-release",
            "product": firefox_desktop,
            "channel": "release",
            "name": ftl("firefox-all-product-firefox", ftl_files=ftl_files),
        },
        "desktop-beta": {
            "slug": "desktop-beta",
            "product": firefox_desktop,
            "channel": "beta",
            "name": ftl("firefox-all-product-firefox-beta", ftl_files=ftl_files),
        },
        "desktop-developer": {
            "slug": "desktop-developer",
            "product": firefox_desktop,
            "channel": "devedition",
            "name": ftl("firefox-all-product-firefox-developer", ftl_files=ftl_files),
        },
        "desktop-nightly": {
            "slug": "desktop-nightly",
            "product": firefox_desktop,
            "channel": "nightly",
            "name": ftl("firefox-all-product-firefox-nightly", ftl_files=ftl_files),
        },
        "desktop-esr": {
            "slug": "desktop-esr",
            "product": firefox_desktop,
            "channel": "esr",
            "name": ftl("firefox-all-product-firefox-esr", ftl_files=ftl_files),
        },
        "android-release": {
            "slug": "android-release",
            "product": firefox_android,
            "channel": "release",
            "name": ftl("firefox-all-product-firefox-android", ftl_files=ftl_files),
        },
        "android-beta": {
            "slug": "android-beta",
            "product": firefox_android,
            "channel": "beta",
            "name": ftl("firefox-all-product-firefox-android-beta", ftl_files=ftl_files),
        },
        "android-nightly": {
            "slug": "android-nightly",
            "product": firefox_android,
            "channel": "nightly",
            "name": ftl("firefox-all-product-firefox-android-nightly", ftl_files=ftl_files),
        },
        "ios-release": {
            "slug": "ios-release",
            "product": firefox_ios,
            "channel": "release",
            "name": ftl("firefox-all-product-firefox-ios", ftl_files=ftl_files),
        },
        "ios-beta": {
            "slug": "ios-beta",
            "product": firefox_ios,
            "channel": "beta",
            "name": ftl("firefox-all-product-firefox-ios", ftl_files=ftl_files),
        },
        # mobile-release is a special case for both android and ios.
        "mobile-release": {
            "slug": "mobile-release",
            "product": mobile_release,
            "channel": "release",
            "name": ftl("firefox-all-product-firefox", ftl_files=ftl_files),
        },
    }

    platform_map = {
        "win64": "Windows 64-bit",
        "win64-msi": "Windows 64-bit MSI",
        "win64-aarch64": "Windows ARM64/AArch64",
        "win": "Windows 32-bit",
        "win-msi": "Windows 32-bit MSI",
        "win-store": "Microsoft Store",
        "osx": "macOS",
        "linux64": "Linux 64-bit",
        "linux": "Linux 32-bit",
        "linux64-aarch64": "Linux ARM64/AArch64",
    }

    # 404 checks.
    if product_slug and product_slug not in product_map.keys():
        raise Http404()
    if platform and platform not in platform_map.keys():
        raise Http404()
    if locale and locale not in product_details.languages.keys():
        raise Http404()
    # 404 if win-store and not desktop-release.
    if platform == "win-store" and product_slug not in ["desktop-release", "desktop-beta"]:
        raise Http404()

    product = product_map.get(product_slug)
    platform_name = None
    locale_name = None
    download_url = None
    template_name = "firefox/all/base.html"
    lang_multi = ftl("firefox-all-lang-multi", ftl_files=ftl_files)

    if product:
        if product_slug.startswith(("mobile", "android", "ios")):
            locale = "en-US"
            locale_name = lang_multi
            download_url = True  # Set to True to avoid trying to generate this later below.
        if product_slug.startswith("mobile"):
            platform = "mobile"
            platform_name = ftl("firefox-all-plat-mobile", ftl_files=ftl_files)
        elif product_slug.startswith("android"):
            platform = "android"
            platform_name = "Android"
        elif product_slug.startswith("ios"):
            platform = "ios"
            platform_name = "iOS"
        elif product_slug in ("desktop-release", "desktop-beta") and platform == "win-store":
            platform_name = "Microsoft Store"
            locale = "en-US"
            locale_name = lang_multi
            download_url = {
                "desktop-release": settings.MICROSOFT_WINDOWS_STORE_FIREFOX_WEB_LINK,
                "desktop-beta": settings.MICROSOFT_WINDOWS_STORE_FIREFOX_BETA_WEB_LINK,
            }.get(product_slug)
        else:
            platform_name = platform and platform_map[platform]
            locale_name = None
            if locale:
                try:
                    build = list(filter(lambda b: b["locale"] == locale, product["product"].get_filtered_full_builds(product["channel"])))[0]
                except IndexError:
                    raise Http404()
                locale_name = f"{build['name_en']} - {build['name_native']}"

    context = {
        "product": product,
        "platform": platform,
        "platform_name": platform_name,
        "locale": locale,
        "locale_name": locale_name,
    }

    # `firefox_desktop.esr_minor_versions` could have 0, 1, or 2 elements. This adds defaults so we always have 2 to unpack.
    esr_latest_version, esr_next_version = (firefox_desktop.esr_minor_versions + [None, None])[:2]
    if esr_next_version:
        context.update(
            desktop_esr_latest_version=esr_latest_version,
            desktop_esr_next_version=esr_next_version,
        )

    # Show download link
    if locale:
        if not download_url:
            download_url = list(filter(lambda b: b["locale"] == locale, product["product"].get_filtered_full_builds(product["channel"])))[0][
                "platforms"
            ][platform]["download_url"]
        context.update(
            download_url=download_url,
        )
        try:
            if product_slug == "desktop-esr":
                download_esr_115_url = list(filter(lambda b: b["locale"] == locale, firefox_desktop.get_filtered_full_builds("esr115")))[0][
                    "platforms"
                ][platform]["download_url"]
                # ESR115 builds do not exist for "sat" ans "skr" languages (see issue #15437).
                if locale in ["sat", "skr"]:
                    download_esr_115_url = None
                context.update(
                    download_esr_115_url=download_esr_115_url,
                )
        except IndexError:
            pass
        if product_slug == "desktop-esr" and esr_next_version:
            try:
                download_esr_next_url = list(filter(lambda b: b["locale"] == locale, firefox_desktop.get_filtered_full_builds("esr_next")))[0][
                    "platforms"
                ][platform]["download_url"]
                context.update(
                    download_esr_next_url=download_esr_next_url,
                )
            except IndexError:
                # If the ESR next version is not available for the locale, remove the context variables.
                context.pop("desktop_esr_latest_version", None)
                context.pop("desktop_esr_next_version", None)

    # Show platforms with download links
    elif platform:
        locales = []
        for b in product["product"].get_filtered_full_builds(product["channel"]):
            locale_name = f"{b['name_en']} - {b['name_native']}"
            if b["locale"] == request.locale:
                # If locale matches request's locale, put it at the top.
                locales.insert(0, (b["locale"], locale_name))
            else:
                locales.append((b["locale"], locale_name))

        context.update(
            locales=locales,
        )

    # Show locales.
    elif product_slug:
        platforms = product["product"].platforms(product["channel"])
        if product_slug in ["desktop-release", "desktop-beta"]:
            idx = platforms.index(("osx", "macOS"))
            platforms.insert(idx, ("win-store", "Microsoft Store"))
        context.update(platforms=platforms)

    # Show products.
    else:
        context.update(
            products=[{"slug": k, "name": v["name"]} for k, v in product_map.items()],
        )

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


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


class FirstrunView(L10nTemplateView):
    ftl_files_map = {"firefox/developer/firstrun.html": ["firefox/developer"]}

    def get(self, *args, **kwargs):
        version = self.kwargs.get("version") or ""
        new_page_url = urlparams(reverse("firefox.new"), reason="outdated")
        channel = detect_channel(version)

        # redirect legacy /firstrun URLs to /firefox/new/
        if channel != "developer":
            return HttpResponsePermanentRedirect(new_page_url)
        elif channel == "developer" and not show_57_dev_firstrun(version):
            return HttpResponsePermanentRedirect(reverse("firefox.developer.index"))
        else:
            return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # add version to context for use in templates
        ctx["version"] = self.kwargs.get("version") or ""

        return ctx

    def get_template_names(self):
        template = "firefox/developer/firstrun.html"

        # return a list to conform with original intention
        return [template]


class WhatsnewView(L10nTemplateView):
    ftl_files_map = {
        "firefox/developer/whatsnew.html": ["firefox/developer"],
        "firefox/developer/whatsnew-mdnplus.html": ["firefox/whatsnew/whatsnew-developer-mdnplus"],
        "firefox/nightly/whatsnew.html": [
            "firefox/nightly/whatsnew",
            "firefox/whatsnew/whatsnew",
        ],
        "firefox/whatsnew/index.html": [
            "firefox/whatsnew/whatsnew-s2d",
            "firefox/whatsnew/whatsnew",
        ],
        "firefox/whatsnew/index-thanks.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx130.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx131-na.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx131-eu.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx132-na.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx132-eu.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx133-vpn.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx133-eu-newsletter.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx133-na-fakespot.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx133-na-mobile.html": [
            "firefox/whatsnew/whatsnew-s2d",
            "firefox/whatsnew/whatsnew",
        ],
        "firefox/whatsnew/whatsnew-fx133-donation.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx133-donation-eu.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx133-donation-na.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx135beta.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx134-us.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx134-ca.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx134-gb.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx134-de.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx134-fr.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx135-eu.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx135-na.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx136-eu-pip.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx136-na-pip.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx136-vpn.html": ["firefox/whatsnew/whatsnew"],
    }

    # specific templates that should not be rendered in
    # countries where we can't advertise Mozilla VPN.
    vpn_excluded_templates = []

    # place expected ?v= values in this list
    variations = ["1", "2", "3", "4"]

    # Nimbus experiment variation expected values
    nimbus_variations = ["v1", "v2", "v3", "v4"]

    # Language codes for WNP 133 Mozilla VPN page
    wnp_133_vpn_langs = [
        "el",
        "en-CA",
        "en-GB",
        "en-US",
        "es-AR",
        "es-CL",
        "es-ES",
        "es-MX",
        "fr",
        "id",
        "ko",
        "pt-BR",
        "tr",
        "uk",
        "vi",
        "zh-TW",
    ]

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
        nimbus_variant = self.request.GET.get("variant", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        # ensure nimbus_variant matches pre-defined value
        if nimbus_variant not in self.nimbus_variations:
            nimbus_variant = None

        ctx["variant"] = variant
        ctx["nimbus_variant"] = nimbus_variant

        return ctx

    def get_template_names(self):
        country = get_country_from_request(self.request)
        locale = l10n_utils.get_locale(self.request)
        version = self.kwargs.get("version") or ""
        variant = self.request.GET.get("v", None)
        nimbus_branch = self.request.GET.get("branch", None)
        nimbus_variant = self.request.GET.get("variant", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        oldversion = self.request.GET.get("oldversion", "")
        # old versions of Firefox sent a prefixed version
        if oldversion.startswith("rv:"):
            oldversion = oldversion[3:]

        channel = detect_channel(version)

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
        elif channel == "beta":
            if version.startswith("135."):
                if locale.startswith("en-"):
                    template = "firefox/whatsnew/whatsnew-fx135beta.html"
                else:
                    template = "firefox/whatsnew/index.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("136."):
            if locale in ["de", "fr", "en-GB"]:
                template = "firefox/whatsnew/whatsnew-fx136-eu-pip.html"
            elif locale in ["en-US", "en-CA"]:
                template = "firefox/whatsnew/whatsnew-fx136-na-pip.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("135."):
            if locale in ["de", "fr", "en-GB"]:
                template = "firefox/whatsnew/whatsnew-fx135-eu.html"
            elif locale in ["en-US", "en-CA"]:
                template = "firefox/whatsnew/whatsnew-fx135-na.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("134."):
            if locale == "en-US":
                template = "firefox/whatsnew/whatsnew-fx134-us.html"
            elif locale == "en-CA":
                template = "firefox/whatsnew/whatsnew-fx134-ca.html"
            elif locale == "en-GB":
                template = "firefox/whatsnew/whatsnew-fx134-gb.html"
            elif locale == "de":
                template = "firefox/whatsnew/whatsnew-fx134-de.html"
            elif locale == "fr":
                template = "firefox/whatsnew/whatsnew-fx134-fr.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("133."):
            if locale in self.wnp_133_vpn_langs and country in settings.VPN_MOBILE_SUB_COUNTRY_CODES:
                template = "firefox/whatsnew/whatsnew-fx133-vpn.html"
            elif country in ["GB", "FR", "DE"] and locale in ["en-GB", "de", "fr"]:
                if variant == "2" or variant == "3":
                    template = "firefox/whatsnew/whatsnew-fx133-donation-eu.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx133-eu-newsletter.html"
            elif country == "US" and locale in ["en-US", "en-CA"]:
                if variant == "2" or variant == "3":
                    template = "firefox/whatsnew/whatsnew-fx133-donation-na.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx133-na-fakespot.html"
            elif country == "CA" and locale in ["en-US", "en-CA"]:
                if variant == "2" or variant == "3":
                    template = "firefox/whatsnew/whatsnew-fx133-donation-na.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx133-na-mobile.html"
            elif locale in ["fr", "de", "it", "pl", "es-ES", "en-GB", "en-US", "en-CA"]:
                template = "firefox/whatsnew/whatsnew-fx133-donation.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("132."):
            if locale in ["en-US", "en-CA", "en-GB"]:
                template = "firefox/whatsnew/whatsnew-fx132-na.html"
            elif locale in ["de", "fr"]:
                template = "firefox/whatsnew/whatsnew-fx132-eu.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("131."):
            if locale in ["en-US", "en-CA"]:
                if nimbus_variant == "v1":
                    template = "firefox/whatsnew/index.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx131-na.html"
            elif locale in ["en-GB", "de", "fr"]:
                if nimbus_variant == "v1":
                    template = "firefox/whatsnew/index.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx131-eu.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("130."):
            if locale in ["en-US", "en-GB", "en-CA", "de", "fr", "es-ES", "it", "pl"]:
                if nimbus_branch == "experiment-wnp-130-tabs":
                    if nimbus_variant == "v1":
                        template = "firefox/whatsnew/index.html"
                    else:
                        template = "firefox/whatsnew/whatsnew-fx130.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx130.html"
            else:
                template = "firefox/whatsnew/index.html"
        else:
            template = "firefox/whatsnew/index.html"

        # do not promote Mozilla VPN in excluded countries.
        if country in settings.VPN_EXCLUDED_COUNTRY_CODES and template in self.vpn_excluded_templates:
            template = "firefox/whatsnew/index.html"

        # return a list to conform with original intention
        return [template]


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
        variation = self.request.GET.get("variation", None)

        # ensure variant matches pre-defined value
        if variation not in self.variations:
            variation = None

        ctx["variation"] = variation

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

        # note: variation and xv params only allow a-z, A-Z, 0-9, -, and _ characters
        variation = self.request.GET.get("variation", None)

        # ensure variant matches pre-defined value
        if variation not in self.variations:
            variation = None

        ctx["variation"] = variation

        reason = self.request.GET.get("reason", None)
        manual_update = True if reason == "manual-update" else False
        outdated = reason == "outdated"
        ctx["manual_update"] = manual_update
        ctx["outdated"] = outdated

        return ctx

    def get_template_names(self):
        variation = self.request.GET.get("variation", None)
        experience = self.request.GET.get("xv", None)

        # ensure variant matches pre-defined value
        if variation not in self.variations:
            variation = None

        if ftl_file_is_active("firefox/new/desktop") and experience != "basic":
            template = "firefox/new/desktop/download.html"
        else:
            template = "firefox/new/basic/base_download.html"

        return [template]


class PlatformViewLinux(L10nTemplateView):
    # the base_platform template works with either platform.ftl or download.ftl active
    template_name = "firefox/new/basic/download_linux.html"

    ftl_files_map = {
        "firefox/new/basic/download_linux.html": [
            "firefox/new/platform",
            "firefox/new/download",
        ],
    }

    # all active locales, this will make the lang switcher work properly
    activation_files = ["firefox/new/download", "firefox/new/platform"]


class PlatformViewMac(L10nTemplateView):
    # the base_platform template works with either platform.ftl or download.ftl active
    template_name = "firefox/new/basic/download_mac.html"

    ftl_files_map = {
        "firefox/new/basic/download_mac.html": [
            "firefox/new/platform",
            "firefox/new/download",
        ],
    }

    # all active locales, this will make the lang switcher work properly
    activation_files = ["firefox/new/download", "firefox/new/platform"]


class PlatformViewWindows(L10nTemplateView):
    # the base_platform template works with either platform.ftl or download.ftl active
    template_name = "firefox/new/basic/download_windows.html"

    ftl_files_map = {
        "firefox/new/basic/download_windows.html": [
            "firefox/new/platform",
            "firefox/new/download",
        ],
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
    ftl_files_map = {"firefox/index.html": ["firefox/browsers"]}
    template_name = "firefox/index.html"


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
    translate_langs = [
        "bg",
        "ca",
        "hr",
        "cs",
        "da",
        "nl",
        "en-US",
        "et",
        "fi",
        "fr",
        "de",
        "el",
        "hu",
        "id",
        "it",
        "lv",
        "lt",
        "pl",
        "pt-PT",
        "ro",
        "ru",
        "sr",
        "sk",
        "sl",
        "es-ES",
        "sv-SE",
        "tr",
        "uk",
        "vi",
    ]

    names = get_translations_native_names(sorted(translate_langs))

    context = {"context_test": names}

    template_name = "firefox/features/translate.html"

    return l10n_utils.render(
        request,
        template_name,
        context,
        ftl_files=["firefox/features/translate", "firefox/features/shared"],
    )


class firefox_features_fast(L10nTemplateView):
    ftl_files_map = {
        "firefox/features/fast.html": [
            "firefox/features/fast-2023",
            "firefox/features/shared",
        ],
        "firefox/features/fast-2024.html": [
            "firefox/features/fast-2024",
            "firefox/features/shared",
        ],
    }

    def get_template_names(self):
        if ftl_file_is_active("firefox/features/fast-2024"):
            template_name = "firefox/features/fast-2024.html"
        else:
            template_name = "firefox/features/fast.html"

        return [template_name]


class firefox_features_pdf(L10nTemplateView):
    ftl_files_map = {
        "firefox/features/pdf-editor.html": ["firefox/features/pdf-editor-2023", "firefox/features/shared"],
        "firefox/features/pdf-editor-fr.html": ["firefox/features/shared"],
    }

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        if locale == "fr":
            template_name = "firefox/features/pdf-editor-fr.html"
        else:
            template_name = "firefox/features/pdf-editor.html"

        return [template_name]


class firefox_features_adblocker(L10nTemplateView):
    ftl_files_map = {
        "firefox/features/adblocker-2025.html": [
            "firefox/features/adblocker-2025",
            "firefox/features/shared",
        ],
        "firefox/features/adblocker.html": [
            "firefox/features/adblocker",
            "firefox/features/shared",
        ],
    }

    def get_template_names(self):
        if ftl_file_is_active("firefox/features/adblocker-2025"):
            template_name = "firefox/features/adblocker-2025.html"
        else:
            template_name = "firefox/features/adblocker.html"

        return [template_name]


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
