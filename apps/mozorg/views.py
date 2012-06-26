from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jingo
from product_details import product_details

import basket
import l10n_utils
from forms import ContributeForm, NewsletterCountryForm


def handle_contribute_form(request, form):
    if form.is_valid():
        data = form.cleaned_data
        contribute_send(data)
        contribute_autorespond(request, data)

        if data['newsletter']:
            try:
                basket.subscribe(data['email'], 'about-mozilla')
            except basket.BasketException, e: pass

        return True
    return False


@csrf_exempt
def contribute(request, template, return_to_form):
    def has_contribute_form():
        return (request.method == 'POST' and
                'contribute-form' in request.POST)

    def has_newsletter_form():
        return (request.method == 'POST' and
                'newsletter-form' in request.POST)


    locale = getattr(request, 'locale', 'en-US')

    success = False
    newsletter_success = False

    # This is ugly, but we need to handle two forms. I would love if
    # these forms could post to separate pages and get redirected
    # back, but we're forced to keep the error/success workflow on the
    # same page. Please change this.
    if has_contribute_form():
        form = ContributeForm(request.POST)
        success = handle_contribute_form(request, form)
        if success:
            # If form was submitted successfully, return a new, empty
            # one.
            form = ContributeForm()
    else:
        form = ContributeForm()

    if has_newsletter_form():
        newsletter_form = NewsletterCountryForm(locale,
                                                request.POST,
                                                prefix='newsletter')
        if newsletter_form.is_valid():
            data = newsletter_form.cleaned_data

            try:
                basket.subscribe(data['email'],
                                 'about-mozilla',
                                 format=data['fmt'],
                                 country=data['country'])
                newsletter_success = True
            except basket.BasketException, e:
                msg = newsletter_form.error_class(
                    ['We apologize, but an error occurred in our system.'
                     'Please try again later.']
                )
                newsletter_form.errors['__all__'] = msg
    else:
        newsletter_form = NewsletterCountryForm(locale, prefix='newsletter')

    return l10n_utils.render(request,
                             template,
                             {'form': form,
                              'success': success,
                              'newsletter_form': newsletter_form,
                              'newsletter_success': newsletter_success,
                              'return_to_form': return_to_form})



def contribute_send(data, locale='en-US'):
    """Forward contributor's email to our contacts.

    For localized contacts, add the local contact's email to the
    dictionary as in the following example
    e.g
    CCS = { 'QA': {'all': 'all@example.com', 'el': 'el@example.com'} }

    Now all emails for QA get send to 'all@example.com' except
    the greek ones which get send to 'el@example.com'.
    """
    CCS = {
        'QA': 'qa-contribute@mozilla.org',
        'Thunderbird': 'tb-kb@mozilla.com',
        'Research': 'diane+contribute@mozilla.com',
        'Design': 'creative@mozilla.com',
        'Security': 'security@mozilla.com',
        'Docs': 'eshepherd@mozilla.com',
        'Drumbeat': 'drumbeat@mozilla.com',
        'Browser Choice': 'isandu@mozilla.com',
        'IT': 'cshields@mozilla.com',
        'Marketing': 'cnovak@mozilla.com',
        'Add-ons': 'atsay@mozilla.com',
        'Education': 'joinmozilla@mozilla.org',
    }

    from_ = 'contribute-form@mozilla.org'
    subject = 'Inquiry about Mozilla %s' % data['interest']
    msg = ("Email: %s\r\nArea of Interest: %s\r\nComment: %s\r\n"
           % (data['email'], data['interest'], data['comments']))
    headers = {'Reply-To': data['email']}

    # Send email To: contribute@mozilla.org and Cc: a team from the
    # CCS list, if applicable. When in DEV mode copy From: to To: and
    # don't add Cc:
    to = ['contribute@mozilla.org']
    if settings.DEV:
        to = [data['email']]

    cc = None
    if not settings.DEV and data['interest'] in CCS:
        email_list = CCS[data['interest']]
        cc = [email_list.get(locale, email_list['all'])]

    email = EmailMessage(subject, msg, from_, to, cc=cc, headers=headers)
    email.send()


def contribute_autorespond(request, data, locale='en-US'):
    """Send an auto-respond email based on chosen field of interest and locale.

    You can add localized responses by creating email messages in
    <EMAIL_TEMPLATE_PATH>/<locale>/<category.txt>
    e.g. emails/el/qa.txt for a QA response in greek.

    To add localized Reply-To header, add the local contributor's email to the
    dictionary as in the following example
    e.g
    replies = { 'Support': {'all': 'all@example.com', 'el': 'el@example.com'} }
    Now all emails for Support get send with 'Reply-To: all@example.com' except
    the greek ones which get send with 'Reply-To: el@example.com'.
    """

    replies = {
        'Support': 'jay@jaygarcia.com',
        'Localization': 'fiotakis@otenet.gr',
        'QA': 'qa-contribute@mozilla.org',
        'Add-ons': 'atsay@mozilla.com',
        'Marketing': 'cnovak@mozilla.com',
        'Design': 'creative@mozilla.com',
        'Documentation': 'jay@jaygarcia.com',
        'Research': 'jay@jaygarcia.com',
        'Thunderbird': 'jzickerman@mozilla.com',
        'Accessibility': 'jay@jaygarcia.com',
        'Firefox Suggestions': 'jay@jaygarcia.com',
        'Firefox Issue': 'dboswell@mozilla.com',
        'Webdev': 'lcrouch@mozilla.com',
        'Education': 'joinmozilla@mozilla.org',
        ' ': 'dboswell@mozilla.com'
    }

    msgs = {
        'Support': 'emails/support.txt',
        'QA': 'emails/qa.txt',
        'Add-ons': 'emails/addons.txt',
        'Marketing': 'emails/marketing.txt',
        'Design': 'emails/design.txt',
        'Documentation': 'emails/documentation.txt',
        'Firefox Suggestions': 'emails/suggestions.txt',
        'Firefox Issue': 'emails/issue.txt',
        'Webdev': 'emails/webdev.txt',
        'Education': 'emails/education.txt',
        ' ': 'emails/other.txt'
        }

    subject = 'Inquiry about Mozilla %s' % data['interest']
    to = [data['email']]
    from_ = 'contribute-form@mozilla.org'
    headers = {}
    msg = ''

    if data['interest'] in msgs:
        msg = jingo.render_to_string(request, msgs[data['interest']], data)
    else:
        return False

    msg = msg.replace('\n', '\r\n')

    if data['interest'] in replies:
        headers = {'Reply-To': replies[data['interest']]}

    email = EmailMessage(subject, msg, from_, to, headers=headers)
    email.send()
