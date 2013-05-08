# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import defaultdict
import json
from operator import itemgetter

from django.contrib import messages
from django.forms.formsets import formset_factory
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache

import basket
import commonware.log
import l10n_utils
import requests
from commonware.decorators import xframe_allow
from funfactory.urlresolvers import reverse
from tower import ugettext_lazy as _lazy

from .forms import (
    ManageSubscriptionsForm, NewsletterForm
)
# Cannot use short "from . import utils" because we need to mock
# utils.get_newsletters in our tests
from newsletter import utils


log = commonware.log.getLogger('b.newsletter')

general_error = _lazy(u'Something is amiss with our system, sorry! Please try '
                      'again later.')
thank_you = _lazy(u'Thank you for updating your email preferences.')
bad_token = _lazy(u'The supplied link has expired. You will receive a new '
                  u'one in the next newsletter.')


UNSUB_UNSUBSCRIBED_ALL = 1
UNSUB_REASONS_SUBMITTED = 2


@xframe_allow
def hacks_newsletter(request):
    return l10n_utils.render(request,
                             'newsletter/hacks.mozilla.org.html')


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
    locale = getattr(request, 'locale', 'en-US')

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

    user_exists = False
    if token:
        try:
            user = basket.user(token)
        except basket.BasketException:
            log.exception("FAILED to get user from token")
        except requests.Timeout:
            # Something wrong with basket backend, no point in continuing,
            # we'd probably fail to subscribe them anyway.
            log.exception("Basket timeout")
            messages.add_message(request, messages.ERROR, general_error)
            return l10n_utils.render(request, 'newsletter/existing.html')
        else:
            user_exists = True

    if not user_exists:
        # Bad or no token
        messages.add_message(request, messages.ERROR, bad_token)
        # If we don't pass the template a formset, most of the page won't
        # be displayed. Our message still will be displayed.
        return l10n_utils.render(request, 'newsletter/existing.html', {})

    # Get the newsletter data - it's a dictionary of dictionaries
    newsletter_data = utils.get_newsletters()

    # Figure out which newsletters to display, and whether to show them
    # as already subscribed.
    initial = []
    for newsletter, data in newsletter_data.iteritems():
        # Only show a newsletter if it has ['show'] == True or the
        # user is already subscribed
        if data.get('show', False) or newsletter in user['newsletters']:
            langs = data['languages']
            initial.append({
                'title': data['title'],
                'subscribed': newsletter in user['newsletters'],
                'newsletter': newsletter,
                'description': data['description'],
                'english_only': len(langs) == 1 and langs[0].startswith('en')
            })

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
                                   if subform.cleaned_data['subscribed']])
                form_kwargs['newsletters'] = newsletters

        form = ManageSubscriptionsForm(locale, data=request.POST, initial=user,
                                       **form_kwargs)

        if formset_is_valid and form.is_valid():

            data = form.cleaned_data

            # Update their format and locale information, if it has changed.
            # Also pass their updated list of newsletters they want to be
            # subscribed to, for basket to implement.
            kwargs = {}
            for k in ['lang', 'format', 'country']:
                if user[k] != data[k]:
                    kwargs[k] = data[k]
            if not remove_all:
                kwargs['newsletters'] = ",".join(newsletters)
            if kwargs:
                try:
                    basket.update_user(token, **kwargs)
                except basket.BasketException:
                    log.exception("Error updating user in basket")
                    messages.add_message(
                        request, messages.ERROR, general_error
                    )
                    return l10n_utils.render(request,
                                             'newsletter/existing.html')
                messages.add_message(request, messages.INFO, thank_you)

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
                if not kwargs:
                    # We haven't told them thank you yet
                    messages.add_message(request, messages.INFO, thank_you)
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

    # We also want a list of the newsletters the user is already subscribed
    # to
    already_subscribed = mark_safe(json.dumps(user['newsletters']))

    context = {
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


def updated(request):
    """View that users come to after submitting on the `existing`
    or `updated` pages.

    Optional query args:

    :param unsub: '1' means we are coming here after the user requested
    to unsubscribe all.  We want to ask them why. '2' means we are coming
    back here after they submitted the form saying why they unsubscribed
    all.

    """

    unsub = request.REQUEST.get('unsub', '0')
    try:
        unsub = int(unsub)
    except ValueError:
        unsub = 0

    # Did they do an unsubscribe all?  then unsub=1 was passed
    unsubscribed_all = unsub == UNSUB_UNSUBSCRIBED_ALL
    # Did they submit their reason? then unsub=2 was passed
    reasons_submitted = unsub == UNSUB_REASONS_SUBMITTED

    # Token might also have been passed (on remove_all only)
    token = request.REQUEST.get('token', None)

    if request.method == 'POST' and reasons_submitted and token:
        # Tell basket about their reasons
        reasons = []

        # Paste together all the reasons that they submitted.  Actually,
        # paste together the English versions of the reasons they submitted,
        # so we can read them.  (Well, except for the free-form reason.)
        for i, reason in enumerate(REASONS):
            if 'reason%d' % i in request.REQUEST:
                reasons.append(unicode(reason))
        if 'reason-text-p' in request.REQUEST:
            reasons.append(request.REQUEST.get('reason-text', ''))

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
