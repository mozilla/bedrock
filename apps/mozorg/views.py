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
def contribute_page(request):
    form = ContributeForm(request.POST or None)
    success = handle_contribute_form(request, form)
    return l10n_utils.render(request, 
                             'mozorg/contribute-page.html',
                             {'form': form,
                              'success': success})

@csrf_exempt
def contribute(request):
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
                             'mozorg/contribute.html',
                             {'form': form,
                              'success': success,
                              'newsletter_form': newsletter_form,
                              'newsletter_success': newsletter_success})

def contribute_send(data):
    ccs = {
        'QA': _('qanoreply@mozilla.com'),
        'Thunderbird': _('tb-kb@mozilla.com'),
        'Students': _('studentreps@mozilla.com'),
        'Research': _('diane+contribute@mozilla.com'),
        'Design': _('creative@mozilla.com'),
        'Security': _('security@mozilla.com'),
        'Docs': _('eshepherd@mozilla.com'),
        'Drumbeat': _('drumbeat@mozilla.com'),
        'Browser Choice': _('isandu@mozilla.com'),
        'IT': _('cshields@mozilla.com'),
        'Marketing': _('cnovak@mozilla.com'),
        'Add-ons': _('atsay@mozilla.com'),
    }

    from_ = 'contribute-form@mozilla.org'
    subject = 'Inquiry about Mozilla %s' % data['interest']
    msg = ("Email: %s\r\nArea of Interest: %s\r\nComment: %s\r\n"
           % (data['email'], data['interest'], data['comments']))
    headers = {'Reply-To': data['email']}

    to = ['contribute@mozilla.org']
    if settings.DEV:
        to = [data['email']]

    cc = None
    if data['interest'] in ccs:
        cc = [ccs[data['interest']]]

    email = EmailMessage(subject, msg, from_, to, cc=cc, headers=headers)
    email.send()

def contribute_autorespond(request, data):
    replies = {
        'Support': _('jay@jaygarcia.com'),
        'Localization': _('fiotakis@otenet.gr'),
        'QA': _('qa-contribute@mozilla.com'),
        'Add-ons': _('atsay@mozilla.com'),
        'Marketing': _('cnovak@mozilla.com'),
        'Design': _('creative@mozilla.com'),
        'Students': _('william@mozilla.com'),
        'Documentation': _('jay@jaygarcia.com'),
        'Research': _('jay@jaygarcia.com'),
        'Thunderbird': _('jzickerman@mozilla.com'),
        'Accessibility': _('jay@jaygarcia.com'),
        'Firefox Suggestions': _('jay@jaygarcia.com'),
        'Firefox Issue': _('dboswell@mozilla.com'),
        'Webdev': _('lcrouch@mozilla.com'),
        ' ': _('dboswell@mozilla.com')
    }

    msgs = {
        'Support': 'emails/support.txt',
        'QA': 'emails/qa.txt',
        'Add-ons': 'emails/addons.txt',
        'Marketing': 'emails/marketing.txt',
        'Design': 'emails/design.txt',
        'Students': 'emails/students.txt',
        'Documentation': 'emails/documentation.txt',
        'Firefox Suggestions': 'emails/suggestions.txt',
        'Firefox Issue': 'emails/issue.txt',
        'Webdev': 'emails/webdev.txt',
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
