# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import re
from cgi import escape
from collections import defaultdict
from operator import itemgetter

from django.conf import settings
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache

import basket
import basket.errors
import commonware.log
from jinja2 import Markup

import lib.l10n_utils as l10n_utils
import requests

from bedrock.base import waffle
from lib.l10n_utils.dotlang import _, _lazy
from bedrock.base.urlresolvers import reverse

from .forms import (CountrySelectForm, EmailForm, ManageSubscriptionsForm,
                    NewsletterForm, NewsletterFooterForm)
# Cannot use short "from . import utils" because we need to mock
# utils.get_newsletters in our tests
from bedrock.base.views import get_geo_from_request
from bedrock.mozorg.util import HttpResponseJSON
from bedrock.newsletter import utils


log = commonware.log.getLogger('b.newsletter')

LANG_FILES = ['mozorg/newsletters']
general_error = _lazy(u'We are sorry, but there was a problem '
                      u'with our system. Please try again later!')
thank_you = _lazy(u'Thanks for updating your email preferences.')
bad_token = _lazy(u'The supplied link has expired or is not valid. You will '
                  u'receive a new one in the next newsletter, or below you '
                  u'can request an email with the link.')
recovery_text = _lazy(
    u'Success! An email has been sent to you with your preference center '
    u'link. Thanks!')

# NOTE: Must format a link into this: (https://www.mozilla.org/newsletter/)
unknown_address_text = _lazy(
    u'This email address is not in our system. Please double check your '
    u'address or <a href="%s">subscribe to our newsletters.</a>')

invalid_email_address = _lazy(u'This is not a valid email address. '
                              u'Please check the spelling.')

NEWSLETTER_STRINGS = {
    u'about-mozilla': {
        'description': _lazy(u'Join Mozillians all around the world and learn about impactful opportunities to support Mozilla\u2019s mission.'),
        'title': _lazy(u'Mozilla Community')},
    u'about-standards': {
        'title': _lazy(u'About Standards')},
    u'addon-dev': {
        'title': _lazy(u'Addon Development')},
    u'affiliates': {
        'description': _lazy(u'A monthly newsletter to keep you up to date with the '
                             u'Firefox Affiliates program.'),
        'title': _lazy(u'Firefox Affiliates')},
    u'ambassadors': {
        'description': _lazy(u'A monthly newsletter on how to get involved with Mozilla on your campus. '),
        'title': _lazy(u'Firefox Student Ambassadors')},
    u'app-dev': {
        'description': _lazy(u'A developer\u2019s guide to highlights of Web platform '
                             u'innovations, best practices, new documentation and more.'),
        'title': _lazy(u'Developer Newsletter')},
    u'aurora': {
        'description': _lazy(u'Aurora'),
        'title': _lazy(u'Aurora')},
    u'beta': {
        'description': _lazy(u'Read about the latest features for Firefox desktop and mobile '
                             u'before the final release.'),
        'title': _lazy(u'Beta News')},
    u'download-firefox-android': {
        'title': _lazy(u'Download Firefox for Android')},
    u'download-firefox-androidsn': {
        'title': _lazy(u'Get Firefox for Android')},
    u'download-firefox-androidsnus': {
        'title': _lazy(u'Get Firefox for Android')},
    u'download-firefox-ios': {
        'title': _lazy(u'Download Firefox for iOS')},
    u'download-firefox-mobile': {
        'title': _lazy(u'Download Firefox for Mobile')},
    u'drumbeat': {
        'title': _lazy(u'Drumbeat Newsgroup')},
    u'firefox-accounts-journey': {
        'description': _lazy(u'Get the most out of your Firefox Account.'),
        'title': _lazy(u'Firefox Accounts Tips')},
    u'firefox-desktop': {
        'description': _lazy(u'Don\u2019t miss the latest announcements about our desktop browser.'),
        'title': _lazy(u'Firefox for desktop')},
    u'firefox-flicks': {
        'description': _lazy(u'Periodic email updates about our annual international film competition.'),
        'title': _lazy(u'Firefox Flicks')},
    u'firefox-ios': {
        'description': _lazy(u'Be the first to know when Firefox is available for iOS devices.'),
        'title': _lazy(u'Firefox iOS')},
    u'firefox-os': {
        'description': _lazy(u'Don\u2019t miss important news and updates about your Firefox OS device.'),
        'title': _lazy(u'Firefox OS smartphone owner?')},
    u'firefox-os-news': {
        'description': _lazy(u'A monthly newsletter and special announcements on how to get the most '
                             u'from your Firefox OS device, including the latest features and coolest '
                             u'Firefox Marketplace apps.'),
        'title': _lazy(u'Firefox OS + You')},
    u'firefox-tips': {
        'description': _lazy(u'Get a weekly tip on how to super-charge your Firefox experience.'),
        'title': _lazy(u'Firefox Weekly Tips')},
    u'get-android-embed': {
        'title': _lazy(u'Get Firefox for Android')},
    u'get-android-notembed': {
        'title': _lazy(u'Get Firefox for Android')},
    u'get-involved': {
        'title': _lazy(u'Get Involved')},
    u'internet-health-report': {
        'title': _lazy(u'Internet Health Report'),
        'description': _lazy(u'Keep up with our annual compilation of research and stories on the issues of privacy '
                             u'&amp; security, openness, digital inclusion, decentralization, and web literacy.')},
    u'join-mozilla': {
        'title': _lazy(u'Join Mozilla')},
    u'knowledge-is-power': {
        'description': _lazy(u'Get all the knowledge you need to stay safer and smarter online.'),
        'title': _lazy(u'Knowledge is Power')},
    u'labs': {
        'title': _lazy(u'About Labs')},
    u'maker-party': {
        'description': u"Mozilla's largest celebration of making and learning on the web.",
        'title': _lazy(u'Maker Party')},
    u'marketplace': {
        'description': _lazy(u'Discover the latest, coolest HTML5 apps on Firefox OS.'),
        'title': _lazy(u'Firefox OS')},
    u'marketplace-android': {
        'title': _lazy(u'Android')},
    u'marketplace-desktop': {
        'title': _lazy(u'Desktop')},
    u'mobile': {
        'description': _lazy(u'Keep up with releases and news about Firefox for Android.'),
        'title': _lazy(u'Firefox for Android')},
    u'mozilla-and-you': {
        'description': _lazy(u'Get how-tos, advice and news to make your Firefox experience work best for you.'),
        'title': _lazy(u'Firefox News')},
    u'mozilla-festival': {
        'description': u"Special announcements about Mozilla's annual, hands-on festival "
                       u"dedicated to forging the future of the open Web.",
        'title': _lazy(u'Mozilla Festival')},
    u'mozilla-foundation': {
        'description': _lazy(u'Regular updates to keep you informed and active in our fight for a better internet.'),
        'title': _lazy(u'Mozilla News')},
    u'mozilla-general': {
        'description': _lazy(u'Special announcements and messages from the team dedicated to keeping '
                             u'the Web free and open.'),
        'title': _lazy(u'Mozilla')},
    u'mozilla-learning-network': {
        'description': _lazy(u'Updates from our global community, helping people learn the most '
                             u'important skills of our age: the ability to read, write and participate '
                             u'in the digital world.'),
        'title': _lazy(u'Mozilla Learning Network')},
    u'mozilla-phone': {
        'description': _lazy(u'Email updates for vouched Mozillians on mozillians.org.'),
        'title': _lazy(u'Mozillians')},
    u'mozilla-technology': {
        'description': _lazy(u"We're building the technology of the future. Come explore with us."),
        'title': _lazy(u'Mozilla Labs')},
    u'os': {
        'description': _lazy(u'Firefox OS news, tips, launch information and where to buy.'),
        'title': _lazy(u'Firefox OS')},
    u'shape-web': {
        'description': _lazy(u'News and information related to the health of the web.'),
        'title': _lazy(u'Shape of the Web')},
    u'student-reps': {
        'description': _lazy(u'Former University program from 2008-2011, now retired and relaunched as '
                             u'the Firefox Student Ambassadors program.'),
        'title': _lazy(u'Student Reps')},
    u'take-action-for-the-internet': {
        'description': _lazy(u'Add your voice to petitions, events and initiatives '
                             u'that fight for the future of the web.'),
        'title': _lazy(u'Take Action for the Internet')},
    u'test-pilot': {
        'description': _lazy(u'Help us make a better Firefox for you by test-driving '
                             u'our latest products and features.'),
        'title': _lazy(u'New Product Testing')},
    u'webmaker': {
        'description': _lazy(u'Special announcements helping you get the most out of Webmaker.'),
        'title': _lazy(u'Webmaker')},
}


UNSUB_UNSUBSCRIBED_ALL = 1
UNSUB_REASONS_SUBMITTED = 2

# A UUID looks like: f81d4fae-7dec-11d0-a765-00a0c91e6bf6
# Here's a regex to match a UUID:
UUID_REGEX = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                        re.IGNORECASE)


@never_cache
def set_country(request, token):
    """Allow a user to set their country"""
    initial = {}
    countrycode = get_geo_from_request(request)
    if countrycode:
        initial['country'] = countrycode.lower()

    form = CountrySelectForm('en-US', data=request.POST or None, initial=initial)
    if form.is_valid():
        try:
            basket.request('post', 'user-meta', data=form.cleaned_data, token=token)
        except basket.BasketException:
            log.exception("Error updating user's country in basket")
            messages.add_message(
                request, messages.ERROR, general_error
            )
        else:
            return redirect(reverse('newsletter.country_success'))

    return l10n_utils.render(request, 'newsletter/country.html', {'form': form})


@never_cache
def confirm(request, token):
    """
    Confirm subscriptions.
    """
    success = generic_error = token_error = rate_limit_error = False

    try:
        result = basket.confirm(token)
    except basket.BasketException as e:
        log.exception("Exception confirming token %s" % token)
        if e.code == basket.errors.BASKET_UNKNOWN_TOKEN:
            token_error = True
        elif e.code == basket.errors.BASKET_USAGE_ERROR:
            rate_limit_error = True
        else:
            # Any other exception
            generic_error = True
    else:
        if result['status'] == 'ok':
            success = True
        else:
            # Shouldn't happen (errors should raise exception),
            # but just in case:
            generic_error = True

    # Assume rate limit error means user already confirmed and clicked confirm
    # link twice in quick succession
    if success or rate_limit_error:
        qparams = ['confirm=1']
        qs = request.META.get('QUERY_STRING', '')
        if qs:
            qparams.append(qs)
        return HttpResponseRedirect("%s?%s" % (reverse('newsletter.existing.token',
                                                       kwargs={'token': token}),
                                               '&'.join(qparams)))
    else:
        return l10n_utils.render(
            request,
            'newsletter/confirm.html',
            {'success': success,
             'generic_error': generic_error,
             'token_error': token_error})


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
        return redirect(reverse('newsletter.recovery'))

    if not UUID_REGEX.match(token):
        # Bad token
        messages.add_message(request, messages.ERROR, bad_token)
        # Redirect to the recovery page
        return redirect(reverse('newsletter.recovery'))

    if waffle.switch('newsletter-maintenance-mode'):
        return l10n_utils.render(request, 'newsletter/existing.html')

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

    has_fxa = 'fxa' in request.GET
    user = None
    if token:
        try:
            # ask for fxa status if not passed in the URL
            params = None if has_fxa else {'fxa': 1}
            user = basket.request('get', 'user', token=token, params=params)
        except basket.BasketNetworkException:
            # Something wrong with basket backend, no point in continuing,
            # we'd probably fail to subscribe them anyway.
            log.exception("Basket timeout")
            messages.add_message(request, messages.ERROR, general_error)
            return l10n_utils.render(request, 'newsletter/existing.html')
        except basket.BasketException as e:
            log.exception("FAILED to get user from token (%s)", e.desc)

    if not user:
        # Bad or no token
        messages.add_message(request, messages.ERROR, bad_token)
        # Redirect to the recovery page
        return redirect(reverse('newsletter.recovery'))

    # if `has_fxa` not returned from basket, set it from the URL
    user.setdefault('has_fxa', has_fxa)
    # Get the newsletter data - it's a dictionary of dictionaries
    newsletter_data = utils.get_newsletters()

    # Figure out which newsletters to display, and whether to show them
    # as already subscribed.
    initial = []
    for newsletter, data in newsletter_data.iteritems():
        # Only show a newsletter if it has ['active'] == True and
        # ['show'] == True or the user is already subscribed
        if not data.get('active', False):
            continue

        if (data.get('show', False) or newsletter in user['newsletters'] or
                (user['has_fxa'] and newsletter in settings.FXA_NEWSLETTERS and
                 any(locale.startswith(l) for l in settings.FXA_NEWSLETTERS_LOCALES))):
            langs = data['languages']
            nstrings = NEWSLETTER_STRINGS.get(newsletter)
            if nstrings:
                if newsletter == 'firefox-accounts-journey' and locale.startswith('en'):
                    # alternate english title
                    title = u'Firefox Account Tips'
                else:
                    title = nstrings['title']
                description = nstrings.get('description', u'')
            else:
                # Firefox Marketplace for Desktop/Android/Firefox OS should be
                # shorten in the titles
                title = _(data['title'].replace('Firefox Marketplace for ', ''))
                description = _(data['description'])

            form_data = {
                'title': Markup(title),
                'subscribed_radio': newsletter in user['newsletters'],
                'subscribed_check': newsletter in user['newsletters'],
                'newsletter': newsletter,
                'description': Markup(description),
                'english_only': len(langs) == 1 and langs[0].startswith('en'),
                'indented': data.get('indent', False),
            }
            if 'order' in data:
                form_data['order'] = data['order']
            initial.append(form_data)

    # Sort by 'order' field if we were given it; otherwise, by title
    if initial:
        keyfield = 'order' if 'order' in initial[0] else 'title'
        initial.sort(key=itemgetter(keyfield))

    NewsletterFormSet = formset_factory(NewsletterForm, extra=0,
                                        max_num=len(initial))

    if request.method == 'POST':
        form_kwargs = {}

        # Temporary form so we can see if they checked 'remove_all'.  If
        # they did, no point in validating the newsletters formset and it would
        # look dumb to complain about it.
        form = ManageSubscriptionsForm(locale, data=request.POST, initial=user)
        remove_all = form.is_valid() and form.cleaned_data['remove_all']

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
                newsletters = set([subform.cleaned_data['newsletter']
                                   for subform in formset
                                   if (subform.cleaned_data['subscribed_radio'] or
                                       subform.cleaned_data['subscribed_check'])])
                form_kwargs['newsletters'] = newsletters

        form = ManageSubscriptionsForm(locale, data=request.POST, initial=user,
                                       **form_kwargs)

        if formset_is_valid and form.is_valid():

            data = form.cleaned_data

            # Update their format and locale information, if it has changed.
            # Also pass their updated list of newsletters they want to be
            # subscribed to, for basket to implement.
            kwargs = {}
            if settings.BASKET_API_KEY:
                kwargs['api_key'] = settings.BASKET_API_KEY
            for k in ['lang', 'format', 'country']:
                if user[k] != data[k]:
                    kwargs[k] = data[k]
            if not remove_all:
                kwargs['newsletters'] = ",".join(newsletters)
            if kwargs:
                # always send lang so basket doesn't try to guess
                kwargs['lang'] = data['lang']
                try:
                    basket.update_user(token, **kwargs)
                except basket.BasketException:
                    log.exception("Error updating user in basket")
                    messages.add_message(
                        request, messages.ERROR, general_error
                    )
                    return l10n_utils.render(request,
                                             'newsletter/existing.html')

            # If they chose to remove all, tell basket that they've opted out
            if remove_all:
                try:
                    basket.unsubscribe(token, user['email'], optout=True)
                except (basket.BasketException, requests.Timeout):
                    log.exception("Error updating subscriptions in basket")
                    messages.add_message(
                        request, messages.ERROR, general_error
                    )
                    return l10n_utils.render(request,
                                             'newsletter/existing.html')
                # We need to pass their token to the next view
                url = reverse('newsletter.updated') \
                    + "?unsub=%s&token=%s" % (UNSUB_UNSUBSCRIBED_ALL, token)
                return redirect(url)

            # We're going to redirect, so the only way to tell the next
            # view that we should display the welcome message in the
            # template is to modify the URL
            url = reverse('newsletter.updated')
            if unsub_parm:
                url += "?unsub=%s" % unsub_parm
            return redirect(url)

        # FALL THROUGH so page displays errors
    else:
        form = ManageSubscriptionsForm(
            locale, initial=user
        )
        formset = NewsletterFormSet(initial=initial)

    # For the template, we want a dictionary whose keys are language codes
    # and each value is the list of newsletter keys that are available in
    # that language code.
    newsletter_languages = defaultdict(list)
    for newsletter, data in newsletter_data.iteritems():
        for lang in data['languages']:
            newsletter_languages[lang].append(newsletter)
    newsletter_languages = mark_safe(json.dumps(newsletter_languages))

    # We also want a list of the newsletters the user is already subscribed to
    already_subscribed = mark_safe(json.dumps(user['newsletters']))

    context = {
        'did_confirm': request.GET.get('confirm', None) == '1',
        'form': form,
        'formset': formset,
        'newsletter_languages': newsletter_languages,
        'newsletters_subscribed': already_subscribed,
        'email': user['email'],
    }

    return l10n_utils.render(request,
                             'newsletter/existing.html',
                             context)


# Possible reasons for unsubscribing
REASONS = [
    _lazy(u"You send too many emails."),
    _lazy(u"Your content wasn't relevant to me."),
    _lazy(u"Your email design was too hard to read."),
    _lazy(u"I didn't sign up for this."),
    _lazy(u"I'm keeping in touch with Mozilla on Facebook and Twitter "
          "instead."),
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
    unsub = _post_or_get(request, 'unsub', '0')
    try:
        unsub = int(unsub)
    except ValueError:
        unsub = 0

    # Did they do an unsubscribe all?  then unsub=1 was passed
    unsubscribed_all = unsub == UNSUB_UNSUBSCRIBED_ALL
    # Did they submit their reason? then unsub=2 was passed
    reasons_submitted = unsub == UNSUB_REASONS_SUBMITTED

    # Token might also have been passed (on remove_all only)
    token = _post_or_get(request, 'token', None)
    # token must be a UUID
    if token is not None and not UUID_REGEX.match(token):
        token = None

    # Say thank you unless we're saying something more specific
    if not unsub:
        messages.add_message(request, messages.INFO, thank_you)

    if request.method == 'POST' and reasons_submitted and token:
        # Tell basket about their reasons
        reasons = []

        # Paste together all the reasons that they submitted.  Actually,
        # paste together the English versions of the reasons they submitted,
        # so we can read them.  (Well, except for the free-form reason.)
        for i, reason in enumerate(REASONS):
            if _post_or_get(request, 'reason%d' % i):
                reasons.append(unicode(reason))
        if _post_or_get(request, 'reason-text-p'):
            reasons.append(_post_or_get(request, 'reason-text', ''))

        reason_text = "\n\n".join(reasons) + "\n\n"

        utils.custom_unsub_reason(token, reason_text)

    context = {
        'unsubscribed_all': unsubscribed_all,
        'reasons_submitted': reasons_submitted,
        'token': token,
        'reasons': enumerate(REASONS),
    }
    return l10n_utils.render(request,
                             'newsletter/updated.html',
                             context)


@never_cache
def recovery(request):
    """
    Let user enter their email address and be sent a message with a link
    to manage their subscriptions.
    """

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                # Try it - basket will return an error if the email is unknown
                basket.send_recovery_message(email)
            except basket.BasketException as e:
                # Was it that their email was not known?  Or it could be invalid,
                # but that doesn't really make a difference.
                if e.code in (basket.errors.BASKET_UNKNOWN_EMAIL,
                              basket.errors.BASKET_INVALID_EMAIL):
                    # Tell them, give them a link to go subscribe if they want
                    url = reverse('newsletter.subscribe')
                    form.errors['email'] = \
                        form.error_class([unknown_address_text % url])
                else:
                    # Log the details
                    log.exception("Error sending recovery message")
                    # and tell the user that something went wrong
                    form.errors['__all__'] = form.error_class([general_error])
            else:
                messages.add_message(request, messages.INFO, recovery_text)
                # Redir as GET, signalling success
                return redirect(request.path + "?success")
    elif 'success' in request.GET:
        # We were redirected after a successful submission.
        # A message will be displayed; don't display the form again.
        form = None
    else:
        form = EmailForm()

    # This view is shared between two different templates. For context see bug 1442129.
    if '/newsletter/opt-out-confirmation/' in request.get_full_path():
        template = "newsletter/opt-out-confirmation.html"
    else:
        template = "newsletter/recovery.html"

    return l10n_utils.render(request, template, {'form': form})


def newsletter_subscribe(request):
    if request.method == 'POST':
        newsletters = request.POST.get('newsletters', None)
        form = NewsletterFooterForm(newsletters,
                                    l10n_utils.get_locale(request),
                                    request.POST)
        errors = []
        if form.is_valid():
            data = form.cleaned_data

            kwargs = {'format': data['fmt']}
            # add optional data
            kwargs.update(dict((k, data[k]) for k in ['country',
                                                      'lang',
                                                      'source_url',
                                                      'first_name',
                                                      'last_name', ]
                               if data[k]))

            # NOTE this is not a typo; Referrer is misspelled in the HTTP spec
            # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.36
            if not kwargs.get('source_url') and request.META.get('HTTP_REFERER'):
                kwargs['source_url'] = request.META['HTTP_REFERER']

            try:
                basket.subscribe(data['email'], data['newsletters'],
                                 **kwargs)
            except basket.BasketException as e:
                if e.code == basket.errors.BASKET_INVALID_EMAIL:
                    errors.append(unicode(invalid_email_address))
                else:
                    log.exception("Error subscribing %s to newsletter %s" %
                                  (data['email'], data['newsletters']))
                    errors.append(unicode(general_error))

        else:
            if 'email' in form.errors:
                errors.append(_('Please enter a valid email address'))
            if 'privacy' in form.errors:
                errors.append(_('You must agree to the privacy notice'))
            for fieldname in ('fmt', 'lang', 'country'):
                if fieldname in form.errors:
                    errors.extend(form.errors[fieldname])

        # form error messages may contain unsanitized user input
        errors = map(escape, errors)

        if request.is_ajax():
            # return JSON
            if errors:
                resp = {
                    'success': False,
                    'errors': errors,
                }
            else:
                resp = {'success': True}

            return HttpResponseJSON(resp)
        else:
            ctx = {'newsletter_form': form}
            if not errors:
                ctx['success'] = True

            return l10n_utils.render(request, 'newsletter/index.html', ctx)

    return l10n_utils.render(request, 'newsletter/index.html')
