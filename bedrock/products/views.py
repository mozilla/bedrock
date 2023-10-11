# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from html import escape
from urllib.parse import quote_plus, unquote_plus

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_safe

from sentry_sdk import capture_exception

from bedrock.base.geo import get_country_from_request
from bedrock.base.waffle import switch
from bedrock.contentful.constants import (
    ARTICLE_CATEGORY_LABEL,
    CONTENT_CLASSIFICATION_VPN,
    CONTENT_TYPE_PAGE_RESOURCE_CENTER,
)
from bedrock.contentful.models import ContentfulEntry
from bedrock.contentful.utils import locales_with_available_content
from bedrock.products.forms import MozSocialWaitlistForm, RelayBundleWaitlistForm, RelayPhoneWaitlistForm, RelayPremiumWaitlistForm, VPNWaitlistForm
from lib import l10n_utils
from lib.l10n_utils import L10nTemplateView, ftl_file_is_active


def vpn_available(request):
    country = get_country_from_request(request)
    country_list = settings.VPN_COUNTRY_CODES

    return country in country_list


def relay_available(product, request):
    country = get_country_from_request(request)
    if product == "relay-bundle":
        country_list = settings.RELAY_PLANS_BY_COUNTRY_AND_LANGUAGE["bundle"]
    elif product == "relay-phone":
        country_list = settings.RELAY_PLANS_BY_COUNTRY_AND_LANGUAGE["phone"]
    elif product == "relay-email":
        country_list = settings.RELAY_PLANS_BY_COUNTRY_AND_LANGUAGE["email"]
    else:
        raise Exception("Unrecognized product passed to relay_available()")

    return country in country_list


def active_locale_available(slug, locale):
    active_locales_for_this_article = ContentfulEntry.objects.get_active_locales_for_slug(
        classification=CONTENT_CLASSIFICATION_VPN,
        content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
        slug=slug,
    )
    return locale in active_locales_for_this_article


@require_safe
def vpn_landing_page(request):
    ftl_files = ["products/vpn/landing", "products/vpn/shared"]
    available_countries = settings.VPN_AVAILABLE_COUNTRIES
    country = get_country_from_request(request)
    vpn_available_in_country = vpn_available(request)
    attribution_available_in_country = country in settings.VPN_AFFILIATE_COUNTRIES
    vpn_affiliate_attribution_enabled = vpn_available_in_country and attribution_available_in_country and switch("vpn-affiliate-attribution")
    relay_bundle_available_in_country = vpn_available_in_country and country in settings.VPN_RELAY_BUNDLE_COUNTRY_CODES and switch("vpn-relay-bundle")
    entrypoint_experiment = request.GET.get("entrypoint_experiment", None)
    entrypoint_variation = request.GET.get("entrypoint_variation", None)

    # ensure experiment parameters matches pre-defined values
    if entrypoint_variation not in ["1", "2"]:
        entrypoint_variation = None

    if entrypoint_experiment != "vpn-refresh-pricing":
        entrypoint_variation = None

    if request.locale == "en-US":
        template_name = "products/vpn/landing-refresh.html"
    else:
        template_name = "products/vpn/landing.html"

    context = {
        "vpn_available": vpn_available_in_country,
        "available_countries": available_countries,
        "connect_servers": settings.VPN_CONNECT_SERVERS,
        "connect_countries": settings.VPN_CONNECT_COUNTRIES,
        "connect_devices": settings.VPN_CONNECT_DEVICES,
        "vpn_affiliate_attribution_enabled": vpn_affiliate_attribution_enabled,
        "relay_bundle_available_in_country": relay_bundle_available_in_country,
        "entrypoint_variation": entrypoint_variation,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_pricing_page(request):
    template_name = "products/vpn/pricing-refresh.html" if request.locale == "en-US" else "products/vpn/pricing.html"
    ftl_files = ["products/vpn/landing", "products/vpn/shared"]
    available_countries = settings.VPN_AVAILABLE_COUNTRIES
    country = get_country_from_request(request)
    vpn_available_in_country = vpn_available(request)
    attribution_available_in_country = country in settings.VPN_AFFILIATE_COUNTRIES
    vpn_affiliate_attribution_enabled = vpn_available_in_country and attribution_available_in_country and switch("vpn-affiliate-attribution")
    variant = request.GET.get("v", None)

    # ensure variant matches pre-defined value
    if variant not in ["1", "2"]:
        variant = None

    context = {
        "vpn_available": vpn_available_in_country,
        "available_countries": available_countries,
        "connect_servers": settings.VPN_CONNECT_SERVERS,
        "connect_countries": settings.VPN_CONNECT_COUNTRIES,
        "connect_devices": settings.VPN_CONNECT_DEVICES,
        "vpn_affiliate_attribution_enabled": vpn_affiliate_attribution_enabled,
        "variant": variant,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_features_page(request):
    template_name = "products/vpn/features.html"
    ftl_files = ["products/vpn/shared"]
    vpn_available_in_country = vpn_available(request)

    context = {
        "vpn_available": vpn_available_in_country,
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
    android_download_url = "https://play.google.com/store/apps/details?id=org.mozilla.firefox.vpn"
    ios_download_url = "https://apps.apple.com/us/app/mozilla-vpn/id1489407738"
    block_download = country in settings.VPN_BLOCK_DOWNLOAD_COUNTRY_CODES

    context = {
        "windows_download_url": windows_download_url,
        "mac_download_url": mac_download_url,
        "linux_download_url": linux_download_url,
        "android_download_url": android_download_url,
        "ios_download_url": ios_download_url,
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


class VPNWindowsView(L10nTemplateView):
    template_name = "products/vpn/platforms/v2/windows.html"
    old_template_name = "products/vpn/platforms/windows.html"

    ftl_files_map = {
        old_template_name: ["products/vpn/platforms/windows", "products/vpn/shared"],
        template_name: ["products/vpn/platforms/windows_v2", "products/vpn/shared"],
    }


class VPNLinuxView(L10nTemplateView):
    template_name = "products/vpn/platforms/v2/linux.html"
    old_template_name = "products/vpn/platforms/linux.html"

    ftl_files_map = {
        old_template_name: ["products/vpn/platforms/linux", "products/vpn/shared"],
        template_name: ["products/vpn/platforms/linux_v2", "products/vpn/shared"],
    }


class VPNDesktopView(L10nTemplateView):
    template_name = "products/vpn/platforms/v2/desktop.html"
    old_template_name = "products/vpn/platforms/desktop.html"

    ftl_files_map = {
        old_template_name: ["products/vpn/platforms/desktop", "products/vpn/shared"],
        template_name: ["products/vpn/platforms/desktop_v2", "products/vpn/shared"],
    }


class VPNMacView(L10nTemplateView):
    template_name = "products/vpn/platforms/v2/mac.html"
    old_template_name = "products/vpn/platforms/mac.html"

    ftl_files_map = {
        old_template_name: ["products/vpn/platforms/mac", "products/vpn/shared"],
        template_name: ["products/vpn/platforms/mac_v2", "products/vpn/shared"],
    }


class VPNMobileView(L10nTemplateView):
    template_name = "products/vpn/platforms/v2/mobile.html"
    old_template_name = "products/vpn/platforms/mobile.html"

    ftl_files_map = {
        old_template_name: ["products/vpn/platforms/mobile", "products/vpn/shared"],
        template_name: ["products/vpn/platforms/mobile_v2", "products/vpn/shared"],
    }


class VPNIosView(L10nTemplateView):
    template_name = "products/vpn/platforms/v2/ios.html"
    old_template_name = "products/vpn/platforms/ios.html"

    ftl_files_map = {
        old_template_name: ["products/vpn/platforms/ios", "products/vpn/shared"],
        template_name: ["products/vpn/platforms/ios_v2", "products/vpn/shared"],
    }


class VPNAndroidView(L10nTemplateView):
    template_name = "products/vpn/platforms/v2/android.html"
    old_template_name = "products/vpn/platforms/android.html"

    ftl_files_map = {
        old_template_name: ["products/vpn/platforms/android", "products/vpn/shared"],
        template_name: ["products/vpn/platforms/android_v2", "products/vpn/shared"],
    }


def _build_category_list(entry_list):
    # Template is expecting this format:
    # category_list = [
    #   {"name": "Cat1", "url": "/full/path/to/category"}, ...
    # ]
    categories_seen = set()
    category_list = []
    root_url = reverse("products.vpn.resource-center.landing")
    for entry in entry_list:
        category = entry.category
        if category and category not in categories_seen:
            category_list.append(
                {
                    "name": category,
                    "url": f"{root_url}?{ARTICLE_CATEGORY_LABEL}={quote_plus(category)}",
                }
            )
            categories_seen.add(category)

    category_list = sorted(category_list, key=lambda x: x["name"])
    return category_list


def _filter_articles(articles_list, category):
    if not category:
        return articles_list

    return [article for article in articles_list if article.category == category]


@require_safe
def resource_center_landing_view(request):
    ARTICLE_GROUP_SIZE = 6
    template_name = "products/vpn/resource-center/landing.html"
    vpn_available_in_country = vpn_available(request)
    active_locales = locales_with_available_content(
        classification=CONTENT_CLASSIFICATION_VPN,
        content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
    )
    requested_locale = l10n_utils.get_locale(request)

    if requested_locale not in active_locales:
        return l10n_utils.redirect_to_best_locale(
            request,
            translations=active_locales,
        )

    resource_articles = ContentfulEntry.objects.get_entries_by_type(
        locale=requested_locale,
        classification=CONTENT_CLASSIFICATION_VPN,
        content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
    )
    category_list = _build_category_list(resource_articles)
    selected_category = unquote_plus(request.GET.get(ARTICLE_CATEGORY_LABEL, ""))

    filtered_articles = _filter_articles(
        resource_articles,
        category=selected_category,
    )

    # The resource_articles are ContentfulEntry objects at the moment, but
    # we really only need their JSON data from here on
    filtered_article_data = [x.data for x in filtered_articles]

    first_article_group, second_article_group = (
        filtered_article_data[:ARTICLE_GROUP_SIZE],
        filtered_article_data[ARTICLE_GROUP_SIZE:],
    )

    ctx = {
        "active_locales": active_locales,
        "vpn_available": vpn_available_in_country,
        "category_list": category_list,
        "first_article_group": first_article_group,
        "second_article_group": second_article_group,
        "selected_category": escape(selected_category),
    }
    return l10n_utils.render(
        request,
        template_name,
        ctx,
        ftl_files=["products/vpn/resource-center", "products/vpn/shared"],
    )


@require_safe
def resource_center_article_view(request, slug):
    """Individual detail pages for the VPN Resource Center"""

    template_name = "products/vpn/resource-center/article.html"
    requested_locale = l10n_utils.get_locale(request)
    vpn_available_in_country = vpn_available(request)

    active_locales_for_this_article = ContentfulEntry.objects.get_active_locales_for_slug(
        classification=CONTENT_CLASSIFICATION_VPN,
        content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
        slug=slug,
    )

    if not active_locales_for_this_article:
        # ie, this article just isn't available in any locale
        raise Http404()

    if requested_locale not in active_locales_for_this_article:
        # Calling render() early will redirect the user to the most
        # appropriate default/alternative locale for their browser
        return l10n_utils.redirect_to_best_locale(
            request,
            translations=active_locales_for_this_article,
        )
    ctx = {}
    try:
        article = ContentfulEntry.objects.get_entry_by_slug(
            slug=slug,
            locale=requested_locale,
            classification=CONTENT_CLASSIFICATION_VPN,
            content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
        )
        ctx.update(article.data)
    except ContentfulEntry.DoesNotExist as ex:
        # We shouldn't get this far, given active_locales_for_this_article,
        # should only show up viable locales etc, so log it loudly before 404ing.
        capture_exception(ex)
        raise Http404()

    ctx.update(
        {
            "active_locales": active_locales_for_this_article,
            "vpn_available": vpn_available_in_country,
            "related_articles": [x.data for x in article.get_related_entries()],
        }
    )

    return l10n_utils.render(
        request,
        template_name,
        ctx,
        ftl_files=[
            "products/vpn/resource-center",
            "products/vpn/shared",
        ],
    )


@require_safe
def relay_landing_page(request):
    template_name = "products/relay/landing.html"
    ftl_files = [
        "products/relay/landing",
        "products/relay/features",
        "products/relay/matrix",
        "products/relay/faq",
        "products/relay/bundle",
        "products/relay/shared",
    ]

    country = get_country_from_request(request)
    vpn_available_in_country = vpn_available(request)
    relay_email_available_in_country = relay_available("relay-email", request)
    relay_phone_available_in_country = relay_available("relay-phone", request)
    relay_bundle_available_in_country = vpn_available_in_country and country in settings.RELAY_PLANS_BY_COUNTRY_AND_LANGUAGE["bundle"]

    context = {
        "email_available": relay_email_available_in_country,
        "phone_available": relay_phone_available_in_country,
        "bundle_available": relay_bundle_available_in_country,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def relay_premium_page(request):
    template_name = "products/relay/premium.html"
    ftl_files = ["products/relay/premium", "products/relay/features", "products/relay/matrix", "products/relay/bundle", "products/relay/shared"]

    country = get_country_from_request(request)
    vpn_available_in_country = vpn_available(request)
    relay_email_available_in_country = relay_available("relay-email", request)
    relay_phone_available_in_country = relay_available("relay-phone", request)
    relay_bundle_available_in_country = vpn_available_in_country and country in settings.RELAY_PLANS_BY_COUNTRY_AND_LANGUAGE["bundle"]

    context = {
        "email_available": relay_email_available_in_country,
        "phone_available": relay_phone_available_in_country,
        "bundle_available": relay_bundle_available_in_country,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def relay_pricing_page(request):
    template_name = "products/relay/pricing.html"
    ftl_files = ["products/relay/matrix", "products/relay/shared"]

    country = get_country_from_request(request)
    vpn_available_in_country = vpn_available(request)
    relay_email_available_in_country = relay_available("relay-email", request)
    relay_phone_available_in_country = relay_available("relay-phone", request)
    relay_bundle_available_in_country = vpn_available_in_country and country in settings.RELAY_PLANS_BY_COUNTRY_AND_LANGUAGE["bundle"]

    context = {
        "email_available": relay_email_available_in_country,
        "phone_available": relay_phone_available_in_country,
        "bundle_available": relay_bundle_available_in_country,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def relay_premium_waitlist__page(request):
    ftl_files = ["products/relay/waitlist", "products/relay/shared"]
    locale = l10n_utils.get_locale(request)
    newsletter_form = RelayPremiumWaitlistForm(locale)

    ctx = {"action": settings.BASKET_SUBSCRIBE_URL, "newsletter_form": newsletter_form, "product": "relay-email"}

    return l10n_utils.render(request, "products/relay/waitlist/premium.html", ctx, ftl_files=ftl_files)


@require_safe
def relay_bundle_waitlist__page(request):
    ftl_files = ["products/relay/waitlist", "products/relay/shared"]
    locale = l10n_utils.get_locale(request)
    newsletter_form = RelayBundleWaitlistForm(locale)

    ctx = {"action": settings.BASKET_SUBSCRIBE_URL, "newsletter_form": newsletter_form, "product": "relay-bundle"}

    return l10n_utils.render(request, "products/relay/waitlist/bundle.html", ctx, ftl_files=ftl_files)


@require_safe
def relay_phone_waitlist__page(request):
    ftl_files = ["products/relay/waitlist", "products/relay/shared"]
    locale = l10n_utils.get_locale(request)
    newsletter_form = RelayPhoneWaitlistForm(locale)

    ctx = {"action": settings.BASKET_SUBSCRIBE_URL, "newsletter_form": newsletter_form, "product": "relay-phone"}

    return l10n_utils.render(request, "products/relay/waitlist/phone.html", ctx, ftl_files=ftl_files)


@require_safe
def monitor_landing_page(request):
    template_name = "products/monitor/landing.html"
    ftl_files = ["products/monitor/landing", "products/monitor/shared"]
    breach_scan_url = settings.MONITOR_BREACH_SCAN_URL

    context = {"breach_scan_url": breach_scan_url}

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def mozsocial_waitlist_page(request):
    template_name = "products/mozsocial/invite.html"
    ftl_files = ["products/mozsocial/invite"]
    locale = l10n_utils.get_locale(request)
    newsletter_form = MozSocialWaitlistForm(locale)

    ctx = {"action": settings.BASKET_SUBSCRIBE_URL, "newsletter_form": newsletter_form, "product": "mozilla-social-waitlist"}

    return l10n_utils.render(request, template_name, ctx, ftl_files=ftl_files)


@require_safe
def monitor_waitlist_scan_page(request):
    template_name = "products/monitor/waitlist/scan.html"
    newsletter_id = "monitor-waitlist"
    ctx = {"newsletter_id": newsletter_id}

    return l10n_utils.render(request, template_name, ctx)


@require_safe
def monitor_waitlist_plus_page(request):
    template_name = "products/monitor/waitlist/plus.html"
    newsletter_id = "monitor-waitlist"
    ctx = {"newsletter_id": newsletter_id}

    return l10n_utils.render(request, template_name, ctx)


@require_safe
def vpn_resource_center_redirect(request, slug):
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
    elif ftl_file_is_active(curr_page["ftl_files"][0]):
        return l10n_utils.render(request, template=curr_page["old_template"], ftl_files=curr_page["ftl_files"])
    else:
        return redirect(redirect_link)
