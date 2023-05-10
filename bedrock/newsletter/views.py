# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
from html import escape

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.cache import never_cache

import basket
import basket.errors
import commonware.log

import lib.l10n_utils as l10n_utils

# Cannot use short "from . import utils" because we need to mock
# utils.get_newsletters in our tests
from bedrock.base.geo import get_country_from_request
from bedrock.base.urlresolvers import reverse
from lib.l10n_utils.fluent import ftl, ftl_lazy

from .forms import (
    CountrySelectForm,
    EmailForm,
    ManageSubscriptionsForm,
    NewsletterFooterForm,
)

log = commonware.log.getLogger("b.newsletter")

FTL_FILES = ["mozorg/newsletters"]

general_error = ftl_lazy("newsletters-we-are-sorry-but-there", ftl_files=FTL_FILES)
thank_you = ftl_lazy("newsletters-your-email-preferences", fallback="newsletters-thanks-for-updating-your", ftl_files=FTL_FILES)
invalid_email_address = ftl_lazy("newsletters-this-is-not-a-valid-email", ftl_files=FTL_FILES)

UNSUB_UNSUBSCRIBED_ALL = 1

# A UUID looks like: f81d4fae-7dec-11d0-a765-00a0c91e6bf6
# Here's a regex to match a UUID:
UUID_REGEX = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)


def set_country(request, token):
    """Allow a user to set their country"""
    initial = {}
    countrycode = get_country_from_request(request)
    if countrycode:
        initial["country"] = countrycode.lower()

    form = CountrySelectForm("en-US", initial=initial)

    context = {
        "action": f"{settings.BASKET_URL}/news/user-meta/",
        "form": form,
        "recovery_url": reverse("newsletter.recovery"),
    }

    return l10n_utils.render(request, "newsletter/country.html", context)


@never_cache
def confirm(request, token):
    """
    Confirm subscriptions.
    """
    success = generic_error = token_error = rate_limit_error = False

    try:
        result = basket.confirm(token)
    except basket.BasketException as e:
        log.exception(f"Exception confirming token {token}")
        if e.code == basket.errors.BASKET_UNKNOWN_TOKEN:
            token_error = True
        elif e.code == basket.errors.BASKET_USAGE_ERROR:
            rate_limit_error = True
        else:
            # Any other exception
            generic_error = True
    else:
        if result["status"] == "ok":
            success = True
        else:
            # Shouldn't happen (errors should raise exception),
            # but just in case:
            generic_error = True

    # Assume rate limit error means user already confirmed and clicked confirm
    # link twice in quick succession
    if success or rate_limit_error:
        qparams = ["confirm=1"]

        if qs := request.META.get("QUERY_STRING", ""):
            qparams.append(qs)

        return HttpResponseRedirect("{}?{}".format(reverse("newsletter.existing.token", kwargs={"token": token}), "&".join(qparams)))
    else:
        qparams = ["error=1"] if generic_error else ["error=2"] if token_error else ["success=1"]

        if qs := request.META.get("QUERY_STRING", ""):
            qparams.append(qs)

        return HttpResponseRedirect("{}?{}".format(reverse("newsletter.confirm.thanks"), "&".join(qparams)))


def confirm_thanks(request):
    generic_error = request.GET.get("error") == "1"
    token_error = request.GET.get("error") == "2"

    return l10n_utils.render(request, "newsletter/confirm.html", {"token_error": token_error, "generic_error": generic_error}, ftl_files=FTL_FILES)


def newsletter_strings_json(request):
    return l10n_utils.render(request, "newsletter/includes/newsletter-strings.json", content_type="application/json", ftl_files=FTL_FILES)


@never_cache
def existing(request, token=None):
    """Manage subscriptions.  If token is provided, user can manage their
    existing subscriptions, to subscribe, unsubscribe, change email or
    language preferences, etc.  If no token is provided, user is redirected
    to the recovery page where they can request their token via email.

    @param HTTPRequest request: Django request object
    @param string token: A UUID that identifies this user to the backend. It's
    sent to users in each newsletter as part of a link to this page, so they
    can manage their subscriptions without needing an account somewhere with
    userid & password.
    """
    locale = l10n_utils.get_locale(request)

    form = ManageSubscriptionsForm(locale)

    context = {
        "action": f"{settings.BASKET_URL}/news/user/",
        "newsletters_url": f"{settings.BASKET_URL}/news/newsletters/",
        "unsubscribe_url": f"{settings.BASKET_URL}/news/unsubscribe/",
        "strings_url": reverse("newsletter.strings"),
        "updated_url": reverse("newsletter.updated"),
        "recovery_url": reverse("newsletter.recovery"),
        "did_confirm": request.GET.get("confirm") == "1",
        "source_url": reverse("newsletter.existing.token", kwargs={"token": ""}),
        "form": form,
    }

    return l10n_utils.render(request, "newsletter/management.html", context, ftl_files=FTL_FILES)


def updated(request):
    """View that users come to after submitting on the `existing`
    or `updated` pages.

    Optional query args:

    :param unsub: '1' means we are coming here after the user requested
    to unsubscribe all.  We want to ask them why. '2' means we are coming
    back here after they submitted the form saying why they unsubscribed
    all.

    """
    unsub = request.GET.get("unsub", "0")
    try:
        unsub = int(unsub)
    except ValueError:
        unsub = 0

    # Did they do an unsubscribe all?  then unsub=1 was passed
    unsubscribed_all = unsub == UNSUB_UNSUBSCRIBED_ALL

    # Say thank you unless we're saying something more specific
    if not unsub:
        messages.add_message(request, messages.INFO, thank_you)

    context = {
        "action": f"{settings.BASKET_URL}/news/custom_unsub_reason/",
        "unsubscribed_all": unsubscribed_all,
    }
    return l10n_utils.render(request, "newsletter/updated.html", context, ftl_files=FTL_FILES)


@never_cache
def recovery(request):
    """
    Let user enter their email address and be sent a message with a link
    to manage their subscriptions.
    """
    form = EmailForm()

    context = {"form": form, "recovery_url": settings.BASKET_URL + "/news/recover/"}

    # This view is shared between two different templates. For context see bug 1442129.
    if "/newsletter/opt-out-confirmation/" in request.get_full_path():
        template = "newsletter/opt-out-confirmation.html"
        ftl_files = ["newsletter/opt-out-confirmation", "mozorg/newsletters"]
    else:
        template = "newsletter/recovery.html"
        ftl_files = FTL_FILES

    return l10n_utils.render(request, template, context, ftl_files=ftl_files)


def newsletter_subscribe(request):
    if request.method == "POST":
        newsletters = request.POST.getlist("newsletters")
        form = NewsletterFooterForm(newsletters, l10n_utils.get_locale(request), request.POST)
        errors = []
        if form.is_valid():
            data = form.cleaned_data

            kwargs = {"format": data["fmt"]}
            # add optional data
            kwargs.update(
                {
                    k: data[k]
                    for k in [
                        "country",
                        "lang",
                        "source_url",
                        "first_name",
                        "last_name",
                    ]
                    if data[k]
                }
            )

            # NOTE this is not a typo; Referrer is misspelled in the HTTP spec
            # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.36
            if not kwargs.get("source_url") and request.headers.get("Referer"):
                kwargs["source_url"] = request.headers["Referer"]

            # Convert data["newsletters"] to a comma separated string.
            newsletters = data["newsletters"]
            if isinstance(newsletters, list):
                newsletters = ",".join(newsletters)

            try:
                basket.subscribe(data["email"], newsletters, **kwargs)
            except basket.BasketException as e:
                if e.code == basket.errors.BASKET_INVALID_EMAIL:
                    errors.append(str(invalid_email_address))
                else:
                    log.exception(f"Error subscribing {data['email']} to newsletter(s) {newsletters}")
                    errors.append(str(general_error))

        else:
            if "email" in form.errors:
                errors.append(ftl("newsletter-form-please-enter-a-valid"))
            if "privacy" in form.errors:
                errors.append(ftl("newsletter-form-you-must-agree-to"))
            for fieldname in ("newsletters", "fmt", "lang", "country"):
                if fieldname in form.errors:
                    errors.extend(form.errors[fieldname])

        # form error messages may contain unsanitized user input
        errors = [escape(e) for e in errors]

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            # return JSON
            if errors:
                resp = {
                    "success": False,
                    "errors": errors,
                }
            else:
                resp = {"success": True}

            return JsonResponse(resp)
        else:
            ctx = {"newsletter_form": form}
            if not errors:
                ctx["success"] = True

            return l10n_utils.render(request, "newsletter/index.html", ctx, ftl_files=FTL_FILES)

    return l10n_utils.render(request, "newsletter/index.html", ftl_files=FTL_FILES)
