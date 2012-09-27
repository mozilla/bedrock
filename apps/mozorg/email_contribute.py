from collections import namedtuple

from django.core.mail import EmailMessage

import basket
import jingo
from jinja2.exceptions import TemplateNotFound

from l10n_utils.dotlang import _lazy as _

fa = namedtuple('FunctionalArea', ['id', 'name', 'contacts'])

FUNCTIONAL_AREAS = (
    fa('support',
        _('Support'),
        ['jay@jaygarcia.com', 'rardila@mozilla.com', 'madasan@gmail.com'],
    ),
    fa('qa',
        _('QA'),
        ['qa-contribute@mozilla.org'],
    ),
    fa('coding',
        _('Coding'),
        ['josh@joshmatthews.net'],
    ),
    fa('marketing',
        _('Marketing'),
        ['cnovak@mozilla.com'],
    ),
    fa('localization',
        _('Localization'),
        ['rardila@mozilla.com', 'jbeatty@mozilla.com', 'arky@mozilla.com'],
    ),
    fa('webdev',
        _('Webdev'),
        ['lcrouch@mozilla.com'],
    ),
    fa('addons',
        _('Add-ons'),
        ['atsay@mozilla.com'],
    ),
    fa('design',
        _('Design'),
        ['mnovak@mozilla.com'],
    ),
    fa('documentation',
        _('Documentation'),
        ['jswisher@mozilla.com'],
    ),
    fa('accessibility',
        _('Accessibility'),
        ['jay@jaygarcia.com'],
    ),
    fa('it',
        _('IT'),
        ['cshields@mozilla.com'],
    ),
    fa('research',
        _('Research'),
        ['jay@jaygarcia.com'],
    ),
    fa('education',
        _('Education'),
        ['bsimon@mozillafoundation.org'],
    ),
    fa('thunderbird',
        'Thunderbird',
        ['jzickerman@mozilla.com', 'rtanglao@mozilla.com'],
    ),
    fa('other',
        _(''),
        ['dboswell@mozilla.com'],
    ),
    fa('suggestions',
        _('Firefox Suggestions'),
        ['jay@jaygarcia.com'],
    ),
    fa('issues',
        _('Firefox Issue'),
        ['jay@jaygarcia.com'],
    ),
)

INTEREST_CHOICES = (('', _('Area of interest?')),) + tuple(
                    (area.id, area.name) for area in FUNCTIONAL_AREAS)
FUNCTIONAL_AREAS_DICT = dict((area.id, area) for area in FUNCTIONAL_AREAS)

LOCALE_CONTACTS = {
    'bn-BD': ['mahayalamkhan@gmail.com'],
    'es-ES': ['nukeador@mozilla-hispano.org'],
    'pt-BR': ['marcelo.araldi@yahoo.com.br'],
}


def handle_form(request, form):
    if form.is_valid():
        data = form.cleaned_data
        send(request, data)
        autorespond(request, data)

        if data['newsletter']:
            try:
                basket.subscribe(data['email'], 'about-mozilla')
            except basket.BasketException:
                pass

        return True
    return False


def send(request, data):
    """Forward contributor's email to our contacts.

    All emails are sent to contribute@mozilla.org

    For locales with points of contact, it is also sent to them.
    For locales without, it is also sent to functional area contacts.
    """

    from_ = 'contribute-form@mozilla.org'
    subject = 'Inquiry about Mozilla %s' % data['interest']
    msg = jingo.render_to_string(request, 'mozorg/emails/infos.txt', data)
    headers = {'Reply-To': data['email']}

    to = ['contribute@mozilla.org']

    cc = None
    if request.locale in LOCALE_CONTACTS:
        cc = LOCALE_CONTACTS[request.locale]
    else:
        cc = FUNCTIONAL_AREAS_DICT[data['interest']].contacts

    email = EmailMessage(subject, msg, from_, to, cc=cc, headers=headers)
    email.send()


def autorespond(request, data):
    """Send an auto-respond email based on chosen field of interest and locale.

    You can add localized responses by creating email messages in
    mozorg/emails/<category.txt>
    """
    functional_area = FUNCTIONAL_AREAS_DICT[data['interest']]

    subject = 'Inquiry about Mozilla %s' % data['interest']
    to = [data['email']]
    from_ = 'contribute-form@mozilla.org'
    headers = {}
    msg = ''

    template = 'mozorg/emails/%s.txt' % functional_area.id
    if request.locale != 'en-US' and request.locale in LOCALE_CONTACTS:
        template = '%s/templates/%s' % (request.locale, template)
        reply_to = LOCALE_CONTACTS[request.locale]
    else:
        reply_to = functional_area.contacts

    try:
        msg = jingo.render_to_string(request, template, data)
    except TemplateNotFound:
        # No template found means no auto-response
        return False

    # FIXME Why ?
    msg = msg.replace('\n', '\r\n')
    headers = {'Reply-To': ','.join(reply_to)}

    email = EmailMessage(subject, msg, from_, to, headers=headers)
    email.send()
