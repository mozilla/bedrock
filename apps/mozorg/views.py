from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import basket
import l10n_utils
import jingo
from forms import ContributeForm

@csrf_exempt
def contribute(request):
    success = False
    form = ContributeForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        contribute_send(data)
        contribute_autorespond(request, data)
    
        if data['newsletter']:
            try:
                basket.subscribe(data['email'], 'about-mozilla')
            except basket.BasketException, e: pass

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
        'Design': 'creative@mozilla.com',
        'Security': 'security@mozilla.com',
        'Docs': 'eshepherd@mozilla.com',
        'Drumbeat': 'drumbeat@mozilla.com',
        'Browser Choice': 'isandu@mozilla.com',
        'IT': 'cshields@mozilla.com',
        'Marketing': 'cnovak@mozilla.com',
        'Add-ons': 'atsay@mozilla.com'
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
        'Webdev': 'lcrouch@mozilla.com',
        ' ': 'dboswell@mozilla.com'
    }

    msgs = {
        'Support': 'emails/support.txt',
        'QA': 'emails/qa.txt',
        'Add-ons': 'emails/addons.txt',
        'Marketing': 'emails/marketing.txt',
        'Students': 'emails/students.txt',
        'Documentation': 'emails/documentation.txt',
        'Firefox Suggestions': 'emails/suggestions.txt',
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
