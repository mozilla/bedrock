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

from bedrock.base.urlresolvers import reverse
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
        codes["source"] = "www.firefox.com"
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


class DownloadThanksView(L10nTemplateView):
    ftl_files_map = {
        "firefox/download/basic/thanks.html": ["firefox/new/download"],
        "firefox/download/basic/thanks_direct.html": ["firefox/new/download"],
        "firefox/download/desktop/thanks.html": ["firefox/new/desktop"],
        "firefox/download/desktop/thanks_direct.html": ["firefox/new/desktop"],
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
                template = "firefox/download/desktop/thanks_direct.html"
            else:
                template = "firefox/download/desktop/thanks.html"
        else:
            if source == "direct":
                template = "firefox/download/basic/thanks_direct.html"
            else:
                template = "firefox/download/basic/thanks.html"

        return [template]


class DownloadView(L10nTemplateView):
    ftl_files_map = {
        "firefox/download/basic/base_download.html": ["firefox/new/download"],
        "firefox/download/desktop/download.html": ["firefox/new/desktop"],
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
            return HttpResponsePermanentRedirect(reverse("firefox.download"))

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
            template = "firefox/download/desktop/download.html"
        else:
            template = "firefox/download/basic/base_download.html"

        return [template]


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
