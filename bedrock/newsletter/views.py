# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import re
from collections import defaultdict
from html import escape
from operator import itemgetter

from django.conf import settings
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache

import basket
import basket.errors
import commonware.log
import requests
from jinja2 import Markup

import lib.l10n_utils as l10n_utils
from bedrock.base import waffle

# Cannot use short "from . import utils" because we need to mock
# utils.get_newsletters in our tests
from bedrock.base.geo import get_country_from_request
from bedrock.base.urlresolvers import reverse
from bedrock.newsletter import utils
from lib.l10n_utils.fluent import ftl, ftl_lazy

from .forms import (
    CountrySelectForm,
    EmailForm,
    ManageSubscriptionsForm,
    NewsletterFooterForm,
    NewsletterForm,
)

log = commonware.log.getLogger("b.newsletter")

FTL_FILES = ["mozorg/newsletters"]

general_error = ftl_lazy("newsletters-we-are-sorry-but-there", ftl_files=FTL_FILES)
thank_you = ftl_lazy("newsletters-your-email-preferences", fallback="newsletters-thanks-for-updating-your", ftl_files=FTL_FILES)
bad_token = ftl_lazy("newsletters-the-supplied-link-has-expired-long", ftl_files=FTL_FILES)
recovery_text = ftl_lazy("newsletters-success-an-email-has-been-sent", ftl_files=FTL_FILES)
invalid_email_address = ftl_lazy("newsletters-this-is-not-a-valid-email", ftl_files=FTL_FILES)

NEWSLETTER_STRINGS = {
    "about-mozilla": {
        "description": ftl_lazy("newsletters-join-mozillians-all-around", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-mozilla-community", ftl_files=FTL_FILES),
    },
    "about-standards": {"title": ftl_lazy("newsletters-about-standards", ftl_files=FTL_FILES)},
    "addon-dev": {"title": ftl_lazy("newsletters-addon-development", ftl_files=FTL_FILES)},
    "affiliates": {
        "description": ftl_lazy("newsletters-a-monthly-newsletter-affiliates", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-affiliates", ftl_files=FTL_FILES),
    },
    "ambassadors": {
        "description": ftl_lazy("newsletters-a-monthly-newsletter-ambassadors", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-student-ambassadors", ftl_files=FTL_FILES),
    },
    "app-dev": {
        "description": ftl_lazy("newsletters-a-developers-guide", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-developer-newsletter", ftl_files=FTL_FILES),
    },
    "aurora": {"description": ftl_lazy("newsletters-aurora", ftl_files=FTL_FILES), "title": ftl_lazy("newsletters-aurora", ftl_files=FTL_FILES)},
    "beta": {
        "description": ftl_lazy("newsletters-read-about-the-latest-features", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-beta-news", ftl_files=FTL_FILES),
    },
    "download-firefox-android": {"title": ftl_lazy("newsletters-download-firefox-for-android", ftl_files=FTL_FILES)},
    "download-firefox-androidsn": {"title": ftl_lazy("newsletters-get-firefox-for-android", ftl_files=FTL_FILES)},
    "download-firefox-androidsnus": {"title": ftl_lazy("newsletters-get-firefox-for-android", ftl_files=FTL_FILES)},
    "download-firefox-ios": {"title": ftl_lazy("newsletters-download-firefox-for-ios", ftl_files=FTL_FILES)},
    "download-firefox-mobile": {"title": ftl_lazy("newsletters-download-firefox-for-mobile", ftl_files=FTL_FILES)},
    "drumbeat": {"title": ftl_lazy("newsletters-drumbeat-newsgroup", ftl_files=FTL_FILES)},
    "firefox-accounts-journey": {
        "description": ftl_lazy("newsletters-get-the-most-firefox-account", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-accounts-tips", ftl_files=FTL_FILES),
    },
    "firefox-desktop": {
        "description": ftl_lazy("newsletters-dont-miss-the-latest", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-for-desktop", ftl_files=FTL_FILES),
    },
    "firefox-flicks": {
        "description": ftl_lazy("newsletters-periodic-email-updates", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-flicks", ftl_files=FTL_FILES),
    },
    "firefox-ios": {
        "description": ftl_lazy("newsletters-be-the-first-to-know", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-ios", ftl_files=FTL_FILES),
    },
    "firefox-os": {
        "description": ftl_lazy("newsletters-dont-miss-important-news", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-os-smartphone-owner", ftl_files=FTL_FILES),
    },
    "firefox-os-news": {
        "description": ftl_lazy("newsletters-a-monthly-newsletter-and-special", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-os-and-you", ftl_files=FTL_FILES),
    },
    "firefox-tips": {
        "description": ftl_lazy("newsletters-get-a-weekly-tip", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-weekly-tips", ftl_files=FTL_FILES),
    },
    "get-android-embed": {"title": ftl_lazy("newsletters-get-firefox-for-android", ftl_files=FTL_FILES)},
    "get-android-notembed": {"title": ftl_lazy("newsletters-get-firefox-for-android", ftl_files=FTL_FILES)},
    "get-involved": {"title": ftl_lazy("newsletters-get-involved", ftl_files=FTL_FILES)},
    "internet-health-report": {
        "title": ftl_lazy("newsletters-insights", fallback="newsletters-internet-health-report", ftl_files=FTL_FILES),
        "description": ftl_lazy(
            "newsletters-mozilla-published-articles-and-deep", fallback="newsletters-keep-up-with-our-annual", ftl_files=FTL_FILES
        ),
    },
    "join-mozilla": {"title": ftl_lazy("newsletters-join-mozilla", ftl_files=FTL_FILES)},
    "knowledge-is-power": {
        "description": ftl_lazy("newsletters-get-all-the-knowledge", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-knowledge-is-power", ftl_files=FTL_FILES),
    },
    "labs": {"title": ftl_lazy("newsletters-about-labs", ftl_files=FTL_FILES)},
    "maker-party": {
        "description": ftl_lazy("newsletters-mozillas-largest-celebration", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-maker-party", ftl_files=FTL_FILES),
    },
    "marketplace": {
        "description": ftl_lazy("newsletters-discover-the-latest", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-os", ftl_files=FTL_FILES),
    },
    "marketplace-android": {"title": ftl_lazy("newsletters-android", ftl_files=FTL_FILES)},
    "marketplace-desktop": {"title": ftl_lazy("newsletters-desktop", ftl_files=FTL_FILES)},
    "mobile": {
        "description": ftl_lazy("newsletters-keep-up-with-releases", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-for-android", ftl_files=FTL_FILES),
    },
    "mozilla-and-you": {
        "description": ftl_lazy("newsletters-get-how-tos", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-news", ftl_files=FTL_FILES),
    },
    "mozilla-festival": {
        "description": ftl_lazy("newsletters-special-announcements-about-mozilla-v2", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-mozilla-festival", ftl_files=FTL_FILES),
    },
    "mozilla-foundation": {
        "description": ftl_lazy("newsletters-regular-updates-to-keep-v2", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-mozilla-news", ftl_files=FTL_FILES),
    },
    "mozilla-general": {
        "description": ftl_lazy("newsletters-special-accouncements-and-messages", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-mozilla", ftl_files=FTL_FILES),
    },
    "mozilla-learning-network": {
        "description": ftl_lazy("newsletters-updates-from-our-global", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-mozilla-learning-network", ftl_files=FTL_FILES),
    },
    "mozilla-phone": {
        "description": ftl_lazy("newsletters-email-updates-from-vouched", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-mozillians", ftl_files=FTL_FILES),
    },
    "mozilla-technology": {
        "description": ftl_lazy("newsletters-were-building-the-technology", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-mozilla-labs", ftl_files=FTL_FILES),
    },
    "os": {
        "description": ftl_lazy("newsletters-firefox-os-news", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-firefox-os", ftl_files=FTL_FILES),
    },
    "shape-web": {
        "description": ftl_lazy("newsletters-news-and-information", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-shapre-of-the-web", ftl_files=FTL_FILES),
    },
    "student-reps": {
        "description": ftl_lazy("newsletters-former-university-program", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-student-reps", ftl_files=FTL_FILES),
    },
    "take-action-for-the-internet": {
        "description": ftl_lazy("newsletters-add-your-voice", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-take-action", ftl_files=FTL_FILES),
    },
    "test-pilot": {
        "description": ftl_lazy("newsletters-help-us-make-a-better", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-new-product-testing", ftl_files=FTL_FILES),
    },
    "webmaker": {
        "description": ftl_lazy("newsletters-special-announcements-helping-you", ftl_files=FTL_FILES),
        "title": ftl_lazy("newsletters-webmaker", ftl_files=FTL_FILES),
    },
}


UNSUB_UNSUBSCRIBED_ALL = 1
UNSUB_REASONS_SUBMITTED = 2

# A UUID looks like: f81d4fae-7dec-11d0-a765-00a0c91e6bf6
# Here's a regex to match a UUID:
UUID_REGEX = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)


def set_country(request, token):
    """Allow a user to set their country"""
    initial = {}
    countrycode = get_country_from_request(request)
    if countrycode:
        initial["country"] = countrycode.lower()

    form = CountrySelectForm("en-US", data=request.POST or None, initial=initial)
    if form.is_valid():
        try:
            basket.request("post", "user-meta", data=form.cleaned_data, token=token)
        except basket.BasketException:
            log.exception("Error updating user's country in basket")
            messages.add_message(request, messages.ERROR, general_error)
        else:
            return redirect(reverse("newsletter.country_success"))

    return l10n_utils.render(request, "newsletter/country.html", {"form": form})


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
        qs = request.META.get("QUERY_STRING", "")
        if qs:
            qparams.append(qs)
        return HttpResponseRedirect("{}?{}".format(reverse("newsletter.existing.token", kwargs={"token": token}), "&".join(qparams)))
    else:
        return l10n_utils.render(
            request, "newsletter/confirm.html", {"success": success, "generic_error": generic_error, "token_error": token_error}, ftl_files=FTL_FILES
        )


@never_cache
def existing(request, token=None):
    """Manage subscriptions.  If token is provided, user can manage their
    existing subscriptions, to subscribe, unsubscribe, change email or
    language preferences, etc.  If no token is provided, user can
    fill in their email and language preferences and sign up for
    newsletters.

    @param HTTPRequest request: Django request object
    @param string token: A UUID that identifies this user to the backend. It's
    sent to users in each newsletter as part of a link to this page, so they
    can manage their subscriptions without needing an account somewhere with
    userid & password.
    """
    locale = l10n_utils.get_locale(request)

    if not token:
        return redirect(reverse("newsletter.recovery"))

    if not UUID_REGEX.match(token):
        # Bad token
        messages.add_message(request, messages.ERROR, bad_token)
        # Redirect to the recovery page
        return redirect(reverse("newsletter.recovery"))

    if waffle.switch("newsletter-maintenance-mode"):
        return l10n_utils.render(request, "newsletter/existing.html", ftl_files=FTL_FILES)

    unsub_parm = None

    # Example user:
    #
    # {u'lang': u'en',
    #  u'format': u'H',
    #  u'country': u'us',
    #  u'newsletters': [u'firefox-tips', u'mobile'],
    #  u'created-date': u'1/30/2013 12:46:05 PM',
    #  u'token': u'some-uuid',
    #  u'email': u'user@example.com'
    # }

    has_fxa = "fxa" in request.GET
    user = None
    if token:
        try:
            # ask for fxa status if not passed in the URL
            params = None if has_fxa else {"fxa": 1}
            user = basket.request("get", "user", token=token, params=params)
        except basket.BasketNetworkException:
            # Something wrong with basket backend, no point in continuing,
            # we'd probably fail to subscribe them anyway.
            log.exception("Basket timeout")
            messages.add_message(request, messages.ERROR, general_error)
            return l10n_utils.render(request, "newsletter/existing.html", ftl_files=FTL_FILES)
        except basket.BasketException as e:
            log.exception("FAILED to get user from token (%s)", e.desc)

    if not user:
        # Bad or no token
        messages.add_message(request, messages.ERROR, bad_token)
        # Redirect to the recovery page
        return redirect(reverse("newsletter.recovery"))

    # if `has_fxa` not returned from basket, set it from the URL
    user.setdefault("has_fxa", has_fxa)
    # Get the newsletter data - it's a dictionary of dictionaries
    newsletter_data = utils.get_newsletters()

    # Figure out which newsletters to display, and whether to show them
    # as already subscribed.
    initial = []
    for newsletter, data in newsletter_data.items():
        # Only show a newsletter if it has ['active'] == True and
        # ['show'] == True or the user is already subscribed
        if not data.get("active", False):
            continue

        if (
            data.get("show", False)
            or newsletter in user["newsletters"]
            or (
                user["has_fxa"] and newsletter in settings.FXA_NEWSLETTERS and any(locale.startswith(loc) for loc in settings.FXA_NEWSLETTERS_LOCALES)
            )
        ):
            langs = data["languages"]
            nstrings = NEWSLETTER_STRINGS.get(newsletter)
            if nstrings:
                if newsletter == "firefox-accounts-journey" and locale.startswith("en"):
                    # alternate english title
                    title = "Firefox Account Tips"
                else:
                    title = nstrings["title"]
                description = nstrings.get("description", "")
            else:
                title = data["title"]
                description = data["description"]

            form_data = {
                "title": Markup(title),
                "subscribed_radio": newsletter in user["newsletters"],
                "subscribed_check": newsletter in user["newsletters"],
                "newsletter": newsletter,
                "description": Markup(description),
                "english_only": len(langs) == 1 and langs[0].startswith("en"),
                "indented": data.get("indent", False),
            }
            if "order" in data:
                form_data["order"] = data["order"]
            initial.append(form_data)

    # Sort by 'order' field if we were given it; otherwise, by title
    if initial:
        keyfield = "order" if "order" in initial[0] else "title"
        initial.sort(key=itemgetter(keyfield))

    NewsletterFormSet = formset_factory(NewsletterForm, extra=0, max_num=len(initial))

    if request.method == "POST":
        form_kwargs = {}

        # Temporary form so we can see if they checked 'remove_all'.  If
        # they did, no point in validating the newsletters formset and it would
        # look dumb to complain about it.
        form = ManageSubscriptionsForm(locale, data=request.POST, initial=user)
        remove_all = form.is_valid() and form.cleaned_data["remove_all"]

        formset_is_valid = False

        if remove_all:
            # We don't care about the newsletter formset
            formset_is_valid = True
            # Make an initialized one in case we fall through to the bottom
            formset = NewsletterFormSet(initial=initial)
        else:
            # We do need to validate the newsletter formset
            formset = NewsletterFormSet(request.POST, initial=initial)
            # Set `newsletters` to the list of newsletters they want.
            # After this, we don't need the formset anymore.
            newsletters = None
            if formset.is_valid():
                formset_is_valid = True
                # What newsletters do they say they want to be subscribed to?
                newsletters = {
                    subform.cleaned_data["newsletter"]
                    for subform in formset
                    if (subform.cleaned_data["subscribed_radio"] or subform.cleaned_data["subscribed_check"])
                }
                form_kwargs["newsletters"] = newsletters

        form = ManageSubscriptionsForm(locale, data=request.POST, initial=user, **form_kwargs)

        if formset_is_valid and form.is_valid():

            data = form.cleaned_data

            # Update their format and locale information, if it has changed.
            # Also pass their updated list of newsletters they want to be
            # subscribed to, for basket to implement.
            kwargs = {}
            for k in ["lang", "format", "country"]:
                if user[k] != data[k]:
                    kwargs[k] = data[k]
            if not remove_all:
                kwargs["newsletters"] = ",".join(newsletters)
            if kwargs:
                if settings.BASKET_API_KEY:
                    kwargs["api_key"] = settings.BASKET_API_KEY
                # always send lang so basket doesn't try to guess
                kwargs["lang"] = data["lang"]
                try:
                    basket.update_user(token, **kwargs)
                except basket.BasketException:
                    log.exception("Error updating user in basket")
                    messages.add_message(request, messages.ERROR, general_error)
                    return l10n_utils.render(request, "newsletter/existing.html", ftl_files=FTL_FILES)

            # If they chose to remove all, tell basket that they've opted out
            if remove_all:
                try:
                    basket.unsubscribe(token, user["email"], optout=True)
                except (basket.BasketException, requests.Timeout):
                    log.exception("Error updating subscriptions in basket")
                    messages.add_message(request, messages.ERROR, general_error)
                    return l10n_utils.render(request, "newsletter/existing.html", ftl_files=FTL_FILES)
                # We need to pass their token to the next view
                url = reverse("newsletter.updated") + f"?unsub={UNSUB_UNSUBSCRIBED_ALL}&token={token}"
                return redirect(url)

            # We're going to redirect, so the only way to tell the next
            # view that we should display the welcome message in the
            # template is to modify the URL
            url = reverse("newsletter.updated")
            if unsub_parm:
                url += f"?unsub={unsub_parm}"
            return redirect(url)

        # FALL THROUGH so page displays errors
    else:
        form = ManageSubscriptionsForm(locale, initial=user)
        formset = NewsletterFormSet(initial=initial)

    # For the template, we want a dictionary whose keys are language codes
    # and each value is the list of newsletter keys that are available in
    # that language code.
    newsletter_languages = defaultdict(list)
    for newsletter, data in newsletter_data.items():
        for lang in data["languages"]:
            newsletter_languages[lang].append(newsletter)
    newsletter_languages = mark_safe(json.dumps(newsletter_languages))

    # We also want a list of the newsletters the user is already subscribed to
    already_subscribed = mark_safe(json.dumps(user["newsletters"]))

    context = {
        "did_confirm": request.GET.get("confirm", None) == "1",
        "form": form,
        "formset": formset,
        "newsletter_languages": newsletter_languages,
        "newsletters_subscribed": already_subscribed,
        "email": user["email"],
    }

    return l10n_utils.render(request, "newsletter/existing.html", context, ftl_files=FTL_FILES)


# Possible reasons for unsubscribing
REASONS = [
    ftl_lazy("newsletters-you-send-too-many-emails", ftl_files=FTL_FILES),
    ftl_lazy("newsletters-your-content-wasnt-relevant", ftl_files=FTL_FILES),
    ftl_lazy("newsletters-your-email-design", ftl_files=FTL_FILES),
    ftl_lazy("newsletters-i-didnt-sign-up", ftl_files=FTL_FILES),
    ftl_lazy("newsletters-im-keeping-in-touch-v2", ftl_files=FTL_FILES),
]


def _post_or_get(request, value, default=None):
    return request.POST.get(value, request.GET.get(value, default))


def updated(request):
    """View that users come to after submitting on the `existing`
    or `updated` pages.

    Optional query args:

    :param unsub: '1' means we are coming here after the user requested
    to unsubscribe all.  We want to ask them why. '2' means we are coming
    back here after they submitted the form saying why they unsubscribed
    all.

    """
    unsub = _post_or_get(request, "unsub", "0")
    try:
        unsub = int(unsub)
    except ValueError:
        unsub = 0

    # Did they do an unsubscribe all?  then unsub=1 was passed
    unsubscribed_all = unsub == UNSUB_UNSUBSCRIBED_ALL
    # Did they submit their reason? then unsub=2 was passed
    reasons_submitted = unsub == UNSUB_REASONS_SUBMITTED

    # Token might also have been passed (on remove_all only)
    token = _post_or_get(request, "token", None)
    # token must be a UUID
    if token is not None and not UUID_REGEX.match(token):
        token = None

    # Say thank you unless we're saying something more specific
    if not unsub:
        messages.add_message(request, messages.INFO, thank_you)

    if request.method == "POST" and reasons_submitted and token:
        # Tell basket about their reasons
        reasons = []

        # Paste together all the reasons that they submitted.  Actually,
        # paste together the English versions of the reasons they submitted,
        # so we can read them.  (Well, except for the free-form reason.)
        for i, reason in enumerate(REASONS):
            if _post_or_get(request, f"reason{i}"):
                reasons.append(str(reason))
        if _post_or_get(request, "reason-text-p"):
            reasons.append(_post_or_get(request, "reason-text", ""))

        reason_text = "\n\n".join(reasons) + "\n\n"

        utils.custom_unsub_reason(token, reason_text)

    context = {
        "unsubscribed_all": unsubscribed_all,
        "reasons_submitted": reasons_submitted,
        "token": token,
        "reasons": enumerate(REASONS),
    }
    return l10n_utils.render(request, "newsletter/updated.html", context, ftl_files=FTL_FILES)


@never_cache
def recovery(request):
    """
    Let user enter their email address and be sent a message with a link
    to manage their subscriptions.
    """

    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                # Try it - basket will return an error if the email is unknown
                basket.send_recovery_message(email)
            except basket.BasketException as e:
                # Was it that their email was not known?  Or it could be invalid,
                # but that doesn't really make a difference.
                if e.code in (basket.errors.BASKET_UNKNOWN_EMAIL, basket.errors.BASKET_INVALID_EMAIL):
                    # Tell them, give them a link to go subscribe if they want
                    url = reverse("newsletter.subscribe")
                    form.errors["email"] = form.error_class([ftl("newsletters-this-email-address-is-not", url=url, ftl_files=FTL_FILES)])
                else:
                    # Log the details
                    log.exception("Error sending recovery message")
                    # and tell the user that something went wrong
                    form.errors["__all__"] = form.error_class([general_error])
            else:
                messages.add_message(request, messages.INFO, recovery_text)
                # Redir as GET, signalling success
                return redirect(request.path + "?success")
    elif "success" in request.GET:
        # We were redirected after a successful submission.
        # A message will be displayed; don't display the form again.
        form = None
    else:
        form = EmailForm()

    # This view is shared between two different templates. For context see bug 1442129.
    if "/newsletter/opt-out-confirmation/" in request.get_full_path():
        template = "newsletter/opt-out-confirmation.html"
        ftl_files = ["newsletter/opt-out-confirmation"]
    else:
        template = "newsletter/recovery.html"
        ftl_files = FTL_FILES

    return l10n_utils.render(request, template, {"form": form}, ftl_files=ftl_files)


def newsletter_subscribe(request):
    if request.method == "POST":
        newsletters = request.POST.get("newsletters", None)
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

            try:
                basket.subscribe(data["email"], data["newsletters"], **kwargs)
            except basket.BasketException as e:
                if e.code == basket.errors.BASKET_INVALID_EMAIL:
                    errors.append(str(invalid_email_address))
                else:
                    log.exception(f"Error subscribing {data['email']} to newsletter {data['newsletters']}")
                    errors.append(str(general_error))

        else:
            if "email" in form.errors:
                errors.append(ftl("newsletter-form-please-enter-a-valid"))
            if "privacy" in form.errors:
                errors.append(ftl("newsletter-form-you-must-agree-to"))
            for fieldname in ("fmt", "lang", "country"):
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
