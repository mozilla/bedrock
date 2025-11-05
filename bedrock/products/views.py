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
from bedrock.contentful.constants import (
    ARTICLE_CATEGORY_LABEL,
    CONTENT_CLASSIFICATION_VPN,
    CONTENT_TYPE_PAGE_RESOURCE_CENTER,
)
from bedrock.contentful.models import ContentfulEntry
from bedrock.contentful.utils import locales_with_available_content
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
    active_locales_for_this_article = ContentfulEntry.objects.get_active_locales_for_slug(
        classification=CONTENT_CLASSIFICATION_VPN,
        content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
        slug=slug,
    )
    return locale in active_locales_for_this_article


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
    mobile_sub_only = vpn_available_mobile_sub_only(request)
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
        "mobile_sub_only": mobile_sub_only,
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


def resource_center_article_available_locales_lookup(*, slug: str) -> list[str]:
    # Helper func to get a list of language codes available for the given
    # Contentful-powered VPN RC slug
    return list(
        ContentfulEntry.objects.filter(
            localisation_complete=True,
            slug=slug,
        ).values_list("locale", flat=True)
    )


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
