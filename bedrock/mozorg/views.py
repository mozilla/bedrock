# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from django.contrib.staticfiles.finders import find as find_static
from django.http import Http404
from django.shortcuts import render as django_render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView

from commonware.decorators import xframe_allow

from bedrock.base.templatetags.helpers import static
from bedrock.mozorg.credits import CreditsFile
from bedrock.mozorg.forums import ForumsFile
from bedrock.mozorg.models import ContributorActivity, TwitterCache
from bedrock.mozorg.util import HttpResponseJSON
from bedrock.newsletter.forms import NewsletterFooterForm
from bedrock.wordpress.views import BlogPostsView
from lib import l10n_utils

credits_file = CreditsFile('credits')
forums_file = ForumsFile('forums')

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
