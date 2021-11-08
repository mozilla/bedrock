# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from html import escape
from urllib.parse import quote_plus, unquote_plus

from django.conf import settings
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST, require_safe

import basket
import basket.errors
from sentry_sdk import capture_exception

from bedrock.base.geo import get_country_from_request
from bedrock.contentful.constants import (
    ARTICLE_CATEGORY_LABEL,
    CONTENT_CLASSIFICATION_VPN,
    CONTENT_TYPE_PAGE_RESOURCE_CENTRE,
)
from bedrock.contentful.models import ContentfulEntry
from bedrock.newsletter.views import general_error, invalid_email_address
from bedrock.products.forms import VPNWaitlistForm
from lib import l10n_utils
from lib.l10n_utils.fluent import ftl


def vpn_available(request):
    country = get_country_from_request(request)

    return country in settings.VPN_COUNTRY_CODES


@require_safe
def vpn_landing_page(request):
    template_name = "products/vpn/landing.html"
    ftl_files = ["products/vpn/landing", "products/vpn/shared"]

    context = {
        "vpn_available": vpn_available(request),
        "available_countries": settings.VPN_AVAILABLE_COUNTRIES,
        "connect_servers": settings.VPN_CONNECT_SERVERS,
        "connect_countries": settings.VPN_CONNECT_COUNTRIES,
        "connect_devices": settings.VPN_CONNECT_DEVICES,
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_invite_page(request):
    ftl_files = ["products/vpn/landing", "products/vpn/shared"]
    locale = l10n_utils.get_locale(request)
    newsletter_form = VPNWaitlistForm(locale)

    return l10n_utils.render(request, "products/vpn/invite.html", {"newsletter_form": newsletter_form}, ftl_files=ftl_files)


@require_POST
def vpn_invite_waitlist(request):
    errors = []
    locale = l10n_utils.get_locale(request)
    form = VPNWaitlistForm(locale, request.POST)
    if form.is_valid():
        data = form.cleaned_data
        kwargs = {
            "email": data["email"],
            "fpn_platform": ",".join(data["platforms"]),
            "fpn_country": data["country"],
            "lang": data["lang"],
            "newsletters": "guardian-vpn-waitlist",
        }
        if settings.BASKET_API_KEY:
            kwargs["api_key"] = settings.BASKET_API_KEY

        # NOTE this is not a typo; Referrer is misspelled in the HTTP spec
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.36
        if not kwargs.get("source_url") and request.META.get("HTTP_REFERER"):
            kwargs["source_url"] = request.META["HTTP_REFERER"]

        try:
            basket.subscribe(**kwargs)
        except basket.BasketException as e:
            if e.code == basket.errors.BASKET_INVALID_EMAIL:
                errors.append(str(invalid_email_address))
            else:
                errors.append(str(general_error))
    else:
        if "email" in form.errors:
            errors.append(ftl("newsletter-form-please-enter-a-valid"))
        if "privacy" in form.errors:
            errors.append(ftl("newsletter-form-you-must-agree-to"))
        for fieldname in ("fmt", "lang", "country"):
            if fieldname in form.errors:
                errors.extend(form.errors[fieldname])

    if errors:
        errors = [escape(e) for e in errors]
        resp = {
            "success": False,
            "errors": errors,
        }
    else:
        resp = {"success": True}

    return JsonResponse(resp)


def _build_category_list(entry_list):
    # Template is expecting this format:
    # category_list = [
    #   {"name": "Cat1", "url": "/full/path/to/category"}, ...
    # ]
    category_list = []
    root_url = reverse("products.vpn.resource-center.landing")
    for entry in entry_list:
        category = entry.category
        if category:
            category_list.append(
                {
                    "name": category,
                    "url": f"{root_url}?{ARTICLE_CATEGORY_LABEL}={quote_plus(category)}",
                }
            )

    category_list = sorted(category_list, key=lambda x: x["name"])
    return category_list


def _filter_articles(articles_list, category):

    if not category:
        return articles_list

    return [article for article in articles_list if article.category == category]


def resource_center_landing_view(request):

    ARTICLE_GROUP_SIZE = 6

    active_locales = [
        "en-US",  # Initially, en-US is the only one available in Contentful
    ]
    locale = l10n_utils.get_locale(request)

    template_name = "products/vpn/resource-center/landing.html"
    ctx = {
        "active_locales": active_locales,
    }

    resource_articles = ContentfulEntry.objects.get_entries_by_type(
        locale=locale,
        classification=CONTENT_CLASSIFICATION_VPN,
        content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTRE,
    )
    category_list = _build_category_list(resource_articles)
    selected_category = unquote_plus(request.GET.get(ARTICLE_CATEGORY_LABEL, ""))

    _filtered_articles = _filter_articles(
        resource_articles,
        category=selected_category,
    )

    # The resource_articles are ContentfulEntry objects at the moment, but
    # we really only need their JSON data from here on
    _filtered_article_data = [x.data for x in _filtered_articles]

    first_article_group, second_article_group = (
        _filtered_article_data[:ARTICLE_GROUP_SIZE],
        _filtered_article_data[ARTICLE_GROUP_SIZE:],
    )

    ctx.update(
        {
            "category_list": category_list,
            "selected_category": selected_category,
            "first_article_group": first_article_group,
            "second_article_group": second_article_group,
        }
    )

    return l10n_utils.render(
        request,
        template_name,
        ctx,
        ftl_files=["products/vpn/shared", "products/vpn/resource-center"],
    )


def resource_center_detail_view(request, slug):
    """Individual detail pages for the VPN Resource Center"""

    template_name = "products/vpn/resource-center/article.html"

    # Initially, en-US is the only one available in Contentful
    locale = l10n_utils.get_locale(request)
    active_locales = [
        "en-US",
    ]

    ctx = {
        "active_locales": active_locales,
    }

    article_dict = {}
    try:
        article = ContentfulEntry.objects.get_entry_by_slug(
            slug=slug,
            locale=locale,
            classification=CONTENT_CLASSIFICATION_VPN,
            content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTRE,
        )
        article_dict.update(article.data)

    except ContentfulEntry.DoesNotExist as ex:
        capture_exception(ex)
        # If our selected locale is valid but we get a genuine slug miss
        # we need to 404 rather than fall through, because render()
        # will trigger a 500 at the templating level if we don't have
        # the article data in the context
        if locale in active_locales:
            raise Http404()

    ctx.update(article_dict)

    ctx.update(
        {
            "related_articles": [x.data for x in article.get_related_entries()],
        }
    )

    return l10n_utils.render(
        request,
        template_name,
        ctx,
        ftl_files=["products/vpn/shared", "products/vpn/resource-center"],
    )
