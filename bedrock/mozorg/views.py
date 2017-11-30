# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
from cgi import escape

from django.conf import settings
from django.contrib.staticfiles.finders import find as find_static
from django.core.context_processors import csrf
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render as django_render
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView

from commonware.decorators import xframe_allow

from bedrock.base.templatetags.helpers import static
from bedrock.base.urlresolvers import reverse
from bedrock.mozorg.credits import CreditsFile
from bedrock.mozorg.forms import (WebToLeadForm)
from bedrock.mozorg.forums import ForumsFile
from bedrock.mozorg.models import ContributorActivity, TwitterCache
from bedrock.mozorg.util import HttpResponseJSON
from bedrock.newsletter.forms import NewsletterFooterForm
from bedrock.wordpress.views import BlogPostsView
from lib import l10n_utils
from lib.l10n_utils.dotlang import lang_file_is_active

credits_file = CreditsFile('credits')
forums_file = ForumsFile('forums')

PARTNERSHIPS_EMAIL_SUBJECT = 'New Partnership Inquiry'
PARTNERSHIPS_EMAIL_TO = ['partnerships@mozilla.com']
PARTNERSHIPS_EMAIL_FROM = 'Mozilla.com <noreply@mozilla.com>'
TECH_BLOG_SLUGS = ['hacks', 'cd', 'futurereleases']


def csrf_failure(request, reason=''):
    template_vars = {'reason': reason}
    return l10n_utils.render(request, 'mozorg/csrf-failure.html', template_vars,
                             status=403)


@xframe_allow
def hacks_newsletter(request):
    return l10n_utils.render(request,
                             'mozorg/newsletter/hacks.mozilla.org.html')


@cache_page(60 * 60 * 24 * 7)  # one week
def mozid_data_view(request, source_name):
    try:
        qs = ContributorActivity.objects.group_by_date_and_source(source_name)
    except ContributorActivity.DoesNotExist:
        # not a valid source_name
        raise Http404

    data = [{'wkcommencing': activity['date'].isoformat(),
             'totalactive': activity['total__sum'],
             'new': activity['new__sum']} for activity in qs]

    return HttpResponseJSON(data, cors=True)


@xframe_allow
def contribute_embed(request):
    return l10n_utils.render(request,
                             'mozorg/contribute/contribute-embed.html')


def process_partnership_form(request, template, success_url_name,
                             template_vars=None, form_kwargs=None):
    template_vars = template_vars or {}
    form_kwargs = form_kwargs or {}

    if request.method == 'POST':
        form = WebToLeadForm(data=request.POST, **form_kwargs)

        msg = 'Form invalid'
        stat = 400
        success = False

        if form.is_valid():
            data = form.cleaned_data.copy()

            honeypot = data.pop('office_fax')

            if honeypot:
                msg = 'ok'
                stat = 200
            else:
                # form testing address
                if not data['email'] == 'success@example.com':
                    data['lead_source'] = form_kwargs.get('lead_source',
                                                          'www.mozilla.org/about/partnerships/')

                    subject = PARTNERSHIPS_EMAIL_SUBJECT
                    sender = PARTNERSHIPS_EMAIL_FROM
                    to = PARTNERSHIPS_EMAIL_TO
                    body = render_to_string('mozorg/emails/partnerships.txt', data,
                                            request=request)

                    email = EmailMessage(subject, body, sender, to)
                    email.send()

                msg = 'ok'
                stat = 200
                success = True

        if request.is_ajax():
            form_errors = {fn: [escape(msg) for msg in msgs] for fn, msgs
                           in form.errors.iteritems()}

            return HttpResponseJSON({'msg': msg, 'errors': form_errors}, status=stat)
        # non-AJAX POST
        else:
            # if form is not valid, render template to retain form data/error messages
            if not success:
                template_vars.update(csrf(request))
                template_vars['form'] = form
                template_vars['form_success'] = success

                return l10n_utils.render(request, template, template_vars)
            # if form is valid, redirect to avoid refresh double post possibility
            else:
                return HttpResponseRedirect("%s?success" % (reverse(success_url_name)))
    # no form POST - build form, add CSRF, & render template
    else:
        # without auto_id set, all id's get prefixed with 'id_'
        form = WebToLeadForm(auto_id='%s', **form_kwargs)

        template_vars.update(csrf(request))
        template_vars['form'] = form
        template_vars['form_success'] = True if ('success' in request.GET) else False

        return l10n_utils.render(request, template, template_vars)


@csrf_protect
def partnerships(request):
    return process_partnership_form(request, 'mozorg/partnerships.html', 'mozorg.partnerships')


@xframe_allow
def contribute_studentambassadors_landing(request):
    tweets = TwitterCache.objects.get_tweets_for('mozstudents')
    return l10n_utils.render(request,
                             'mozorg/contribute/studentambassadors/landing.html',
                             {'tweets': tweets})


def holiday_calendars(request, template='mozorg/projects/holiday-calendars.html'):
    """Generate the table of holiday calendars from JSON."""
    calendars = []
    json_file = find_static('caldata/calendars.json')
    with open(json_file) as calendar_data:
        calendars = json.load(calendar_data)

    letters = set()
    for calendar in calendars:
        letters.add(calendar['country'][:1])

    data = {
        'calendars': sorted(calendars, key=lambda k: k['country']),
        'letters': sorted(letters),
        'CALDATA_URL': static('caldata/')
    }

    return l10n_utils.render(request, template, data)


@require_safe
def credits_view(request):
    """Display the names of our contributors."""
    ctx = {'credits': credits_file}
    # not translated
    return django_render(request, 'mozorg/credits.html', ctx)


@require_safe
def forums_view(request):
    """Display our mailing lists and newsgroups."""
    ctx = {'forums': forums_file}
    return l10n_utils.render(request, 'mozorg/about/forums/forums.html', ctx)


class Robots(TemplateView):
    template_name = 'mozorg/robots.txt'
    content_type = 'text/plain'

    def get_context_data(self, **kwargs):
        hostname = self.request.get_host()
        return {'disallow_all': not hostname == 'www.mozilla.org'}


def home(request):
    locale = l10n_utils.get_locale(request)

    donate_params = settings.DONATE_PARAMS.get(
        locale, settings.DONATE_PARAMS['en-US'])

    # presets are stored as a string but, for the home banner
    # we need it as a list.
    donate_params['preset_list'] = donate_params['presets'].split(',')

    if lang_file_is_active('mozorg/home/index-quantum', locale):
        template = 'mozorg/home/home-quantum.html'
    else:
        template = 'mozorg/home/home.html'

    return l10n_utils.render(request, template, {
        'donate_params': donate_params
    })


NAMESPACES = {
    'addons-bl': {
        'namespace': 'http://www.mozilla.org/2006/addons-blocklist',
        'standard': 'Add-ons Blocklist',
        'docs': 'https://wiki.mozilla.org/Extension_Blocklisting:Code_Design',
    },
    'em-rdf': {
        'namespace': 'http://www.mozilla.org/2004/em-rdf',
        'standard': 'Extension Manifest',
        'docs': 'https://developer.mozilla.org/en/Install_Manifests',
    },
    'microsummaries': {
        'namespace': 'http://www.mozilla.org/microsummaries/0.1',
        'standard': 'Microsummaries',
        'docs': 'https://developer.mozilla.org/en/Microsummary_XML_grammar_reference',
    },
    'mozsearch': {
        'namespace': 'http://www.mozilla.org/2006/browser/search/',
        'standard': 'MozSearch plugin format',
        'docs': 'https://developer.mozilla.org/en/Creating_MozSearch_plugins',
    },
    'update': {
        'namespace': 'http://www.mozilla.org/2005/app-update',
        'standard': 'Software Update Service',
        'docs': 'https://wiki.mozilla.org/Software_Update:Testing',
    },
    'xbl': {
        'namespace': 'http://www.mozilla.org/xbl',
        'standard': 'XML Binding Language (XBL)',
        'docs': 'https://developer.mozilla.org/en/XBL',
    },
    'xforms-type': {
        'namespace': 'http://www.mozilla.org/projects/xforms/2005/type',
        'standard': 'XForms mozType extension',
        'docs': 'https://developer.mozilla.org/en/XForms/Custom_Controls',
    },
    'xul': {
        'namespace': 'http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul',
        'standard': 'XML User Interface Language (XUL)',
        'docs': 'https://developer.mozilla.org/en/XUL',
    },
}


def namespaces(request, namespace):
    context = NAMESPACES[namespace]
    context['slug'] = namespace
    template = 'mozorg/namespaces.html'
    return django_render(request, template, context)


def contribute_friends(request):
    newsletter_form = NewsletterFooterForm('firefox-friends', l10n_utils.get_locale(request))

    return l10n_utils.render(request,
                             'mozorg/contribute/friends.html',
                             {'newsletter_form': newsletter_form})


class TechnologyView(BlogPostsView):
    blog_slugs = TECH_BLOG_SLUGS
    blog_posts_limit = 4
    blog_posts_template_variable = 'articles'

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)

        if locale.startswith('en-'):
            template_name = 'mozorg/technology-en.html'
        else:
            template_name = 'mozorg/technology.html'

        return [template_name]


class IHView(BlogPostsView):
    template_name = 'mozorg/internet-health/index.html'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'internetcitizen'


class DeveloperView(BlogPostsView):
    template_name = 'mozorg/developer/index.html'
    blog_slugs = 'hacks'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'


def plugincheck(request):
    locale = l10n_utils.get_locale(request)

    if lang_file_is_active('mozorg/plugincheck-update', locale):
        template = 'mozorg/plugincheck-update.html'
    else:
        template = 'mozorg/plugincheck.html'

    return l10n_utils.render(request, template)
