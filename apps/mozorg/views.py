from django.core.mail import EmailMessage
from session_csrf import anonymous_csrf
from django.conf import settings

import basket
import l10n_utils
import jingo
from forms import ContributeForm

@anonymous_csrf
def contribute(request):
    success = False
    form = ContributeForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        contribute_send(data)
        contribute_autorespond(request, data)
    
        if data['optin']:
            # TODO: replace "something" with the actual name of the
            # newsletter
            basket.subscribe(data['email'], 'something')

        success = True

    return l10n_utils.render(request, 
                             'mozorg/contribute.html',
                             {'form': form,
                              'success': success})

def contribute_send(data):
    ccs = {
        'QA': 'qanoreply@mozilla.com',
        'Thunderbird': 'tb-kb@mozilla.com',
        'Students': 'studentreps@mozilla.com',
        'Research': 'diane+contribute@mozilla.com',
        'IT': 'cshields@mozilla.com',
        'Marketing': 'cnovak@mozilla.com',
        'Add-ons': 'atsay@mozilla.com'
    }

    from_ = 'contribute-form@mozilla.org'
    subject = 'Inquiry about Mozilla %s' % data['interest']
    msg = ("Email: %s\r\nArea of Interest: %s\r\n"
           % (data['email'], data['interest']))
    headers = {'Reply-To': data['email']}

    to = ['contribute@mozilla.org']
    if settings.DEV:
        to = [data['email']]

    cc = None
    if data['interest'] in ccs:
        cc = [data['interest']]
        if settings.DEV:
            cc = [data['email']]

    email = EmailMessage(subject, msg, from_, to, cc=cc, headers=headers)
    email.send()

def contribute_autorespond(request, data):
    replies = {
        'Support': 'jay@jaygarcia.com',
        'Localization': 'fiotakis@otenet.gr',
        'QA': 'qa-contribute@mozilla.com',
        'Add-ons': 'atsay@mozilla.com',
        'Marketing': 'cnovak@mozilla.com',
        'Students': 'jhaas@mozilla.com',
        'Documentation': 'jay@jaygarcia.com',
        'Research': 'jay@jaygarcia.com',
        'Thunderbird': 'jzickerman@mozilla.com',
        'Accessibility': 'jay@jaygarcia.com',
        'Firefox Suggestions': 'jay@jaygarcia.com',
        ' ': 'dboswell@mozilla.com'
    }

    msgs = {
        'Support': 'emails/support.html',
        'QA': 'emails/qa.html',
        'Add-ons': 'emails/addons.html',
        'Marketing': 'emails/marketing.html',
        'Students': 'emails/students.html',
        'Documentation': 'emails/documentation.html',
        'Firefox Suggestions': 'emails/suggestions.html',
        ' ': 'emails/other.html'
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

    if data['interest'] in replies:
        headers = {'Reply-To': replies[data['interest']]}

    email = EmailMessage(subject, msg, from_, to, headers=headers)
    email.send()
