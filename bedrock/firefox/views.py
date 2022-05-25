# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import hashlib
import hmac
import logging
import re
from collections import OrderedDict
from random import random
from urllib.parse import urlparse

from django.conf import settings
from django.http import (
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    JsonResponse,
)
from django.utils.cache import add_never_cache_headers, patch_response_headers
from django.utils.encoding import force_str
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_safe

import basket
import querystringsafe_base64
from product_details.version_compare import Version
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient

from bedrock.base.geo import get_country_from_request
from bedrock.base.urlresolvers import reverse
from bedrock.base.waffle_config import DictOf, config
from bedrock.contentful.api import ContentfulPage
from bedrock.firefox.firefox_details import (
    firefox_android,
    firefox_desktop,
    firefox_ios,
)
from bedrock.firefox.forms import SendToDeviceWidgetForm, SMSSendToDeviceForm
from bedrock.newsletter.forms import NewsletterFooterForm
from bedrock.releasenotes import version_re
from lib import l10n_utils
from lib.l10n_utils import L10nTemplateView, get_translations_native_names
from lib.l10n_utils.fluent import ftl, ftl_file_is_active

logger = logging.getLogger(__name__)

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
    ("visit_id", "(not set)"),
]
STUB_VALUE_RE = re.compile(r"^[a-z0-9-.%():_]+$", flags=re.IGNORECASE)

TWILIO_CLIENT = None


def get_twilio_client():
    global TWILIO_CLIENT
    if TWILIO_CLIENT is None:
        # Make sure all TWILIO_* credentials are set.
        if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_MESSAGING_SERVICE_SID]):
            return None
        TWILIO_CLIENT = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    return TWILIO_CLIENT


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


@require_POST
@csrf_exempt
def sms_send_to_device_ajax(request):
    client = get_twilio_client()
    form = SMSSendToDeviceForm(request.POST)

    if not form.is_valid():
        return JsonResponse({"success": False, "errors": form.errors["phone_number"]})

    to_number = form.cleaned_data["phone_number"]

    # For testing purposes, return success.
    if to_number == "5555555555":
        return JsonResponse({"success": True})

    if client is None:
        return JsonResponse({"success": False, "errors": ["SMS not configured"]})

    # NOTE: If needed, content may differ based on `form.cleaned_data["platform"]`

    # `sms_body` is limited to 1600 characters.
    sms_body = "Download the Firefox mobile browser for automatic protection on all your devices. https://app.adjust.com/b83wfbd"

    try:
        client.messages.create(
            to=to_number,
            body=sms_body,
            messaging_service_sid=settings.TWILIO_MESSAGING_SERVICE_SID,
        )
    except TwilioRestException as err:
        logger.error(err)
        return JsonResponse({"success": False, "errors": ["Message failed to send"]})

    return JsonResponse({"success": True})


@require_POST
@csrf_exempt
def send_to_device_ajax(request):
    locale = l10n_utils.get_locale(request)
    email = request.POST.get("s2d-email")

    # ensure a value was entered in phone or email field
    if not email:
        return JsonResponse({"success": False, "errors": ["s2d-email"]})

    # pull message set from POST (not part of form, so wont be in cleaned_data)
    message_set = request.POST.get("message-set", "default")

    # begin collecting data to pass to form constructor
    data = {
        "platform": request.POST.get("platform"),
        "email": email,
    }

    # instantiate the form with processed POST data
    form = SendToDeviceWidgetForm(data)

    if form.is_valid():
        email = form.cleaned_data.get("email")
        platform = form.cleaned_data.get("platform")

        # if no platform specified, default to 'all'
        if not platform:
            platform = "all"

        # ensure we have a valid message set. if not, fall back to default
        if message_set not in SEND_TO_DEVICE_MESSAGE_SETS:
            MESSAGES = SEND_TO_DEVICE_MESSAGE_SETS["default"]
        else:
            MESSAGES = SEND_TO_DEVICE_MESSAGE_SETS[message_set]

        if platform in MESSAGES["email"]:
            try:
                basket.subscribe(
                    email,
                    MESSAGES["email"][platform],
                    source_url=request.POST.get("source-url"),
                    lang=locale,
                )
            except basket.BasketException:
                return JsonResponse({"success": False, "errors": ["system"]}, status=400)
        else:
            return JsonResponse({"success": False, "errors": ["platform"]})

        resp_data = {"success": True}
    else:
        resp_data = {"success": False, "errors": list(form.errors)}

    return JsonResponse(resp_data)


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
        "firefox/nightly/whatsnew.html": ["firefox/nightly/whatsnew", "firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/index-account.html": ["firefox/whatsnew/whatsnew-account", "firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/index.html": ["firefox/whatsnew/whatsnew-s2d", "firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx97-en.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx97-de.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx97-fr.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx98-vpn-eu.html": ["firefox/whatsnew/whatsnew-98-vpn-eu", "firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx98-mobile-de.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx98-mobile-fr.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx98-vpn-en.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx99-de.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx99-fr.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx99-en.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx99-en-rally.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx101-vpn-en.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx101-vpn-de.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx101-vpn-fr.html": ["firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx101-vpn-mobile-unfree-en.html": ["firefox/whatsnew/whatsnew-101-vpn-mobile", "firefox/whatsnew/whatsnew"],
        "firefox/whatsnew/whatsnew-fx101-vpn-mobile.html": ["firefox/whatsnew/whatsnew-101-vpn-mobile", "firefox/whatsnew/whatsnew"],
    }

    # specific templates that should not be rendered in
    # countries where we can't advertise Mozilla VPN.
    vpn_excluded_templates = [
        "firefox/whatsnew/whatsnew-fx98-vpn-en.html",
        "firefox/whatsnew/whatsnew-fx98-vpn-eu.html",
        "firefox/whatsnew/whatsnew-fx101-vpn-en.html",
        "firefox/whatsnew/whatsnew-fx101-vpn-de.html",
        "firefox/whatsnew/whatsnew-fx101-vpn-fr.html",
        "firefox/whatsnew/whatsnew-fx101-vpn-mobile-unfree-en.html",
        "firefox/whatsnew/whatsnew-fx101-vpn-mobile.html",
    ]

    # place expected ?v= values in this list
    variations = ["1", "2", "3"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        version = self.kwargs.get("version") or ""
        pre_release_channels = ["nightly", "developer", "beta"]
        channel = detect_channel(version)

        # add active_locales for hard-coded locale templates
        locale = l10n_utils.get_locale(self.request)
        hard_coded_templates = ["id"]
        if locale in hard_coded_templates and channel not in pre_release_channels:
            ctx["active_locales"] = locale

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
            if show_57_dev_whatsnew(version):
                template = "firefox/developer/whatsnew.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("101."):
            if locale.startswith("en"):
                if variant == "2":
                    template = "firefox/whatsnew/whatsnew-fx101-vpn-mobile-unfree-en.html"
                elif variant == "3":
                    template = "firefox/whatsnew/whatsnew-fx101-vpn-mobile.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx101-vpn-en.html"
            elif locale == "de":
                template = "firefox/whatsnew/whatsnew-fx101-vpn-de.html"
            elif locale == "fr":
                template = "firefox/whatsnew/whatsnew-fx101-vpn-fr.html"
            elif locale in ["es-ES", "fi", "it", "nl", "sv-SE"] and ftl_file_is_active("firefox/whatsnew/whatsnew-101-vpn-mobile"):
                template = "firefox/whatsnew/whatsnew-fx101-vpn-mobile.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("99."):
            if locale.startswith("en"):
                if variant == "2":
                    template = "firefox/whatsnew/whatsnew-fx99-en-rally.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx99-en.html"
            elif locale == "de":
                template = "firefox/whatsnew/whatsnew-fx99-de.html"
            elif locale == "fr":
                template = "firefox/whatsnew/whatsnew-fx99-fr.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("98."):
            if locale.startswith("en"):
                if country in ["SE", "FI"]:
                    template = "firefox/whatsnew/whatsnew-fx98-vpn-eu.html"
                else:
                    template = "firefox/whatsnew/whatsnew-fx98-vpn-en.html"
            elif ftl_file_is_active("firefox/whatsnew/whatsnew-98-vpn-eu") and country in ["SE", "FI"]:
                template = "firefox/whatsnew/whatsnew-fx98-vpn-eu.html"
            elif locale == "de":
                template = "firefox/whatsnew/whatsnew-fx98-mobile-de.html"
            elif locale == "fr":
                template = "firefox/whatsnew/whatsnew-fx98-mobile-fr.html"
            else:
                template = "firefox/whatsnew/index.html"
        elif version.startswith("97.") and locale == "de":
            template = "firefox/whatsnew/whatsnew-fx97-de.html"
        elif version.startswith("97.") and locale == "fr":
            template = "firefox/whatsnew/whatsnew-fx97-fr.html"
        elif version.startswith("97.") and locale.startswith("en"):
            template = "firefox/whatsnew/whatsnew-fx97-en.html"
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
    variations = ["a", "b", "fx94"]

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

    def render_to_response(self, context, **response_kwargs):
        # set experimental percentages per locale with this config
        # e.g. EXP_CONFIG_FX_NEW=de:20,en-US:10,fr:25
        # this would send 20% of de, 10% of en-US, and 25% of fr requests to the experiment page
        # all other locales would be unaffected
        redirect_percents = config("EXP_CONFIG_FX_NEW", default="", parser=DictOf(int))
        skip_exp = "automation" in self.request.GET
        # only engage the experiment infra if some experiments are set
        if redirect_percents and not skip_exp:
            locale = l10n_utils.get_locale(self.request)
            percent = redirect_percents.get(locale, 0)
            if percent:
                percent = percent / 100
                if random() <= percent:
                    exp_url = reverse("exp.firefox.new")
                    query_string = self.request.META.get("QUERY_STRING", "")
                    if query_string:
                        exp_url = "?".join([exp_url, force_str(query_string, errors="ignore")])
                    response = HttpResponseRedirect(exp_url)
                else:
                    response = super().render_to_response(context, **response_kwargs)
                # remove cache for better experiment results
                add_never_cache_headers(response)
                return response

        return super().render_to_response(context, **response_kwargs)

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
    # no country field, so no need to send locale
    newsletter_form = NewsletterFooterForm("ios-beta-test-flight", "")

    return l10n_utils.render(request, "firefox/testflight.html", {"newsletter_form": newsletter_form})


class FirefoxHomeView(L10nTemplateView):
    ftl_files_map = {"firefox/home/index-master.html": ["firefox/home"]}

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
        variant = self.request.GET.get("v", None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

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


class FirefoxMobileView(L10nTemplateView):
    ftl_files_map = {
        "firefox/mobile/index.html": ["firefox/mobile"],
        "firefox/browsers/mobile/index.html": ["firefox/browsers/mobile/index"],
    }
    activation_files = [
        "firefox/mobile",
        "firefox/browsers/mobile/index",
    ]

    def get_template_names(self):
        if ftl_file_is_active("firefox/browsers/mobile/index"):
            template = "firefox/browsers/mobile/index.html"
        else:
            template = "firefox/mobile/index.html"

        return [template]


class FirefoxContenful(L10nTemplateView):
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
