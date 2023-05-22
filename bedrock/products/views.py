# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from html import escape
from urllib.parse import quote_plus, unquote_plus

from django.conf import settings
from django.http import Http404
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
from bedrock.products.forms import VPNWaitlistForm
from lib import l10n_utils


def vpn_available(request):
    country = get_country_from_request(request)
    country_list = settings.VPN_COUNTRY_CODES

    if switch("vpn-wave-vi"):
        country_list = settings.VPN_COUNTRY_CODES + settings.VPN_COUNTRY_CODES_WAVE_VI

    return country in country_list


@require_safe
def vpn_landing_page(request):
    template_name = "products/vpn/landing.html"
    ftl_files = ["products/vpn/landing", "products/vpn/shared"]
    available_countries = settings.VPN_AVAILABLE_COUNTRIES
    country = get_country_from_request(request)
    vpn_available_in_country = vpn_available(request)
    attribution_available_in_country = country in settings.VPN_AFFILIATE_COUNTRIES
    vpn_affiliate_attribution_enabled = vpn_available_in_country and attribution_available_in_country and switch("vpn-affiliate-attribution")
    relay_bundle_available_in_country = vpn_available_in_country and country in settings.VPN_RELAY_BUNDLE_COUNTRY_CODES and switch("vpn-relay-bundle")

    if switch("vpn-wave-vi"):
        available_countries = settings.VPN_AVAILABLE_COUNTRIES_WAVE_VI

    context = {
        "vpn_available": vpn_available_in_country,
        "available_countries": available_countries,
        "connect_servers": settings.VPN_CONNECT_SERVERS,
        "connect_countries": settings.VPN_CONNECT_COUNTRIES,
        "connect_devices": settings.VPN_CONNECT_DEVICES,
        "vpn_affiliate_attribution_enabled": vpn_affiliate_attribution_enabled,
        "relay_bundle_available_in_country": relay_bundle_available_in_country,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_pricing_page(request):
    template_name = "products/vpn/pricing.html"
    ftl_files = ["products/vpn/landing", "products/vpn/shared"]
    available_countries = settings.VPN_AVAILABLE_COUNTRIES
    country = get_country_from_request(request)
    vpn_available_in_country = vpn_available(request)
    attribution_available_in_country = country in settings.VPN_AFFILIATE_COUNTRIES
    vpn_affiliate_attribution_enabled = vpn_available_in_country and attribution_available_in_country and switch("vpn-affiliate-attribution")

    if switch("vpn-wave-vi"):
        available_countries = settings.VPN_AVAILABLE_COUNTRIES_WAVE_VI

    context = {
        "vpn_available": vpn_available_in_country,
        "available_countries": available_countries,
        "connect_servers": settings.VPN_CONNECT_SERVERS,
        "connect_countries": settings.VPN_CONNECT_COUNTRIES,
        "connect_devices": settings.VPN_CONNECT_DEVICES,
        "vpn_affiliate_attribution_enabled": vpn_affiliate_attribution_enabled,
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
    ios_download_url = "https://apps.apple.com/us/app/firefox-private-network-vpn/id1489407738"
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
