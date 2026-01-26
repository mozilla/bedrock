# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.http import require_safe

from bedrock.base.geo import get_country_from_request
from bedrock.products.forms import VPNWaitlistForm
from lib import l10n_utils
from lib.l10n_utils.fluent import ftl_file_is_active


def vpn_available(request):
    """
    Returns `True` if Mozilla VPN is available via one or more subscription channels
    in a users country. On desktop, users can subscribe via their Mozilla account (FxA).
    On mobile, users can subscribe via the Google Play Store or the Apple App Store.
    """
    country = get_country_from_request(request)
    country_list = settings.VPN_COUNTRY_CODES + settings.VPN_MOBILE_SUB_COUNTRY_CODES

    return country in country_list


def vpn_available_mobile_sub_only(request):
    """
    Returns `True` if Mozilla VPN can ONLY be purchased via a Google Play Store or Apple App
    Store subscription in a users country. This is used to present a different signup flow
    in the pricing section on the main VPN landing page, to prevent people signing up via
    subplat / FxA.
    """
    country = get_country_from_request(request)
    country_list = settings.VPN_MOBILE_SUB_COUNTRY_CODES

    return country in country_list


def vpn_available_android_sub_only(request):
    """
    Returns `True` if Mozilla VPN can ONLY be purchased via a Google Play Store subscription
    in a users country. This is used to prevent showing an Apple App Store badge in countries
    where the Apple App Store is not available.
    """
    country = get_country_from_request(request)
    country_list = settings.VPN_MOBILE_SUB_ANDROID_ONLY_COUNTRY_CODES

    return country in country_list


def active_locale_available(slug, locale):
    # Import inside function to avoid circular import (models.py imports from views.py)
    from bedrock.products.models import VPNResourceCenterDetailPage

    return VPNResourceCenterDetailPage.objects.filter(slug=slug, locale__language_code=locale, live=True).exists()


@require_safe
def vpn_landing_page(request):
    ftl_files = ["products/vpn/landing-2023", "products/vpn/shared", "products/vpn/pricing-2023"]
    vpn_available_in_country = vpn_available(request)
    mobile_sub_only = vpn_available_mobile_sub_only(request)
    android_sub_only = vpn_available_android_sub_only(request)
    experience = request.GET.get("xv", None)
    entrypoint_experiment = request.GET.get("entrypoint_experiment", None)
    entrypoint_variation = request.GET.get("entrypoint_variation", None)

    # ensure experiment parameters matches pre-defined values
    if entrypoint_variation not in []:
        entrypoint_variation = None

    if entrypoint_experiment not in []:
        entrypoint_experiment = None

    template_name = "products/vpn/landing-refresh.html"

    context = {
        "vpn_available": vpn_available_in_country,
        "mobile_sub_only": mobile_sub_only,
        "android_sub_only": android_sub_only,
        "available_countries": settings.VPN_AVAILABLE_COUNTRIES,
        "connect_servers": settings.VPN_CONNECT_SERVERS,
        "connect_countries": settings.VPN_CONNECT_COUNTRIES,
        "connect_devices": settings.VPN_CONNECT_DEVICES,
        "experience": experience,
        "entrypoint_experiment": entrypoint_experiment,
        "entrypoint_variation": entrypoint_variation,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_pricing_page(request):
    ftl_files = ["products/vpn/pricing-2023", "products/vpn/shared"]
    available_countries = settings.VPN_AVAILABLE_COUNTRIES
    vpn_available_in_country = vpn_available(request)
    mobile_sub_only = vpn_available_mobile_sub_only(request)
    android_sub_only = vpn_available_android_sub_only(request)
    experience = request.GET.get("xv", None)
    template_name = "products/vpn/pricing-refresh.html"

    context = {
        "vpn_available": vpn_available_in_country,
        "mobile_sub_only": mobile_sub_only,
        "android_sub_only": android_sub_only,
        "available_countries": available_countries,
        "connect_servers": settings.VPN_CONNECT_SERVERS,
        "connect_countries": settings.VPN_CONNECT_COUNTRIES,
        "connect_devices": settings.VPN_CONNECT_DEVICES,
        "experience": experience,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_features_page(request):
    template_name = "products/vpn/features.html"
    ftl_files = ["products/vpn/features", "products/vpn/shared"]
    vpn_available_in_country = vpn_available(request)
    mobile_sub_only = vpn_available_mobile_sub_only(request)

    context = {
        "vpn_available": vpn_available_in_country,
        "mobile_sub_only": mobile_sub_only,
        "connect_servers": settings.VPN_CONNECT_SERVERS,
        "connect_countries": settings.VPN_CONNECT_COUNTRIES,
        "connect_devices": settings.VPN_CONNECT_DEVICES,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_download_page(request):
    template_name = "products/vpn/download.html"
    country = get_country_from_request(request)
    ftl_files = ["products/vpn/download", "products/vpn/shared"]
    windows_download_url = f"{settings.VPN_ENDPOINT}r/vpn/download/windows"
    mac_download_url = f"{settings.VPN_ENDPOINT}r/vpn/download/mac"
    linux_download_url = f"{settings.VPN_ENDPOINT}r/vpn/download/linux"
    block_download = country in settings.VPN_BLOCK_DOWNLOAD_COUNTRY_CODES

    context = {
        "windows_download_url": windows_download_url,
        "mac_download_url": mac_download_url,
        "linux_download_url": linux_download_url,
        "connect_devices": settings.VPN_CONNECT_DEVICES,
        "block_download": block_download,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_mac_download_page(request):
    template_name = "products/vpn/mac-download.html"
    country = get_country_from_request(request)
    ftl_files = ["products/vpn/platform-post-download", "products/vpn/shared"]
    mac_download_url = f"{settings.VPN_ENDPOINT}r/vpn/download/mac"
    block_download = country in settings.VPN_BLOCK_DOWNLOAD_COUNTRY_CODES

    context = {
        "mac_download_url": mac_download_url,
        "block_download": block_download,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_windows_download_page(request):
    template_name = "products/vpn/windows-download.html"
    country = get_country_from_request(request)
    ftl_files = ["products/vpn/platform-post-download", "products/vpn/shared"]
    windows_download_url = f"{settings.VPN_ENDPOINT}r/vpn/download/windows"
    block_download = country in settings.VPN_BLOCK_DOWNLOAD_COUNTRY_CODES

    context = {
        "windows_download_url": windows_download_url,
        "block_download": block_download,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_invite_page(request):
    ftl_files = ["products/vpn/landing", "products/vpn/shared"]
    locale = l10n_utils.get_locale(request)
    newsletter_form = VPNWaitlistForm(locale)
    action = settings.BASKET_SUBSCRIBE_URL

    ctx = {"action": action, "newsletter_form": newsletter_form}

    return l10n_utils.render(request, "products/vpn/invite.html", ctx, ftl_files=ftl_files)


@require_safe
def monitor_waitlist_scan_page(request):
    template_name = "products/monitor/waitlist/scan.html"
    newsletter_id = "monitor-waitlist"
    ctx = {"newsletter_id": newsletter_id}

    return l10n_utils.render(request, template_name, ctx)


@require_safe
def vpn_resource_center_redirect(request, slug):
    # When a /more url is requested the user should be forwarded to the /resource-centre url
    # If the rc article is not available in their requested language bedrock should display the /more/ article if it is available in their language.
    # 2. If neither is available in their language bedrock should forward to the English rc article.
    VPNRC_SLUGS = {
        "what-is-an-ip-address": {
            "slug": "what-is-an-ip-address",
            "old_template": "products/vpn/more/ip-address.html",
            "ftl_files": ["products/vpn/more/ip-address", "products/vpn/shared"],
        },
        "vpn-or-proxy": {
            "slug": "the-difference-between-a-vpn-and-a-web-proxy",
            "old_template": "products/vpn/more/vpn-or-proxy.html",
            "ftl_files": ["products/vpn/more/vpn-or-proxy", "products/vpn/shared"],
        },
        "what-is-a-vpn": {
            "slug": "what-is-a-vpn",
            "old_template": "products/vpn/more/what-is-a-vpn.html",
            "ftl_files": ["products/vpn/more/what-is-a-vpn", "products/vpn/shared"],
        },
        "when-to-use-a-vpn": {
            "slug": "5-reasons-you-should-use-a-vpn",
            "old_template": "products/vpn/more/when-to-use.html",
            "ftl_files": ["products/vpn/more/when-to-use-a-vpn", "products/vpn/shared"],
        },
    }
    locale = l10n_utils.get_locale(request)
    curr_page = VPNRC_SLUGS[slug]
    rc_slug = curr_page["slug"]
    redirect_link = f"/{locale}/products/vpn/resource-center/{rc_slug}/"
    if active_locale_available(rc_slug, locale):
        return redirect(redirect_link)
    elif ftl_file_is_active(curr_page["ftl_files"][0], locale):
        return l10n_utils.render(request, template=curr_page["old_template"], ftl_files=curr_page["ftl_files"])
    else:
        return redirect(redirect_link)
