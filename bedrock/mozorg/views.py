# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from commonware.decorators import xframe_allow
from django.conf import settings
from django.shortcuts import render as django_render
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView
from lib import l10n_utils

from bedrock.contentcards.models import get_page_content_cards
from bedrock.mozorg.credits import CreditsFile
from bedrock.mozorg.forums import ForumsFile
from bedrock.pocketfeed.models import PocketArticle
from bedrock.wordpress.views import BlogPostsView

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


class IHView(BlogPostsView):
    template_name = 'mozorg/internet-health/index.html'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'internetcitizen'


def home_view(request):
    locale = l10n_utils.get_locale(request)
    donate_params = settings.DONATE_PARAMS.get(
        locale, settings.DONATE_PARAMS['en-US'])

    # presets are stored as a string but, for the home banner
    # we need it as a list.
    donate_params['preset_list'] = donate_params['presets'].split(',')
    ctx = {
        'donate_params': donate_params,
        'pocket_articles': PocketArticle.objects.all()[:4]
    }

    if locale.startswith('en-'):
        template_name = 'mozorg/home/home-en.html'
        ctx['page_content_cards'] = get_page_content_cards('home-2019', 'en-US')
    elif locale == 'de':
        template_name = 'mozorg/home/home-de.html'
        ctx['page_content_cards'] = get_page_content_cards('home-de', 'de')
    elif locale == 'fr':
        template_name = 'mozorg/home/home-fr.html'
        ctx['page_content_cards'] = get_page_content_cards('home-fr', 'fr')
    else:
        template_name = 'mozorg/home/home.html'

    return l10n_utils.render(request, template_name, ctx)
