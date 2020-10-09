# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render as django_render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView

from lib import l10n_utils
from lib.l10n_utils import L10nTemplateView, get_locale
from lib.l10n_utils.fluent import ftl_file_is_active

from bedrock.contentful.api import contentful
from bedrock.contentful.models import ContentfulEntry
from bedrock.mozorg.credits import CreditsFile
from bedrock.mozorg.forums import ForumsFile
from bedrock.pocketfeed.models import PocketArticle

from commonware.decorators import xframe_allow

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


class ContributeView(L10nTemplateView):
    ftl_files_map = {
        'mozorg/contribute/contribute-2020.html': ['mozorg/contribute']
    }

    def get_template_names(self):
        if ftl_file_is_active('mozorg/contribute'):
            template_name = 'mozorg/contribute/contribute-2020.html'
        else:
            template_name = 'mozorg/contribute/index.html'

        return [template_name]


class HomePageView(L10nTemplateView):
    def get_lang(self):
        locale = get_locale(self.request)
        if '-' in locale:
            return locale.split('-')[0]

        return locale

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lang = self.get_lang()
        page_data = ContentfulEntry.objects.get_homepage(lang)
        if page_data:
            ctx['card_layouts'] = page_data['layouts']

        ctx['pocket_articles'] = PocketArticle.objects.all()[:4]
        return ctx

    def get_template_names(self):
        return [
            f'mozorg/home/home-{self.get_lang()}.html',
            'mozorg/home/home.html'
        ]


@method_decorator(never_cache, name='dispatch')
class HomePagePreviewView(L10nTemplateView):
    locales_map = {
        'en': 'en-US',
    }
    card_data_lang = 'en'

    def get_preview_locale(self):
        return self.locales_map.get(self.card_data_lang, self.card_data_lang)

    def get_preview_url(self, page_id):
        return f'/{self.get_preview_locale()}/homepage-preview/{page_id}/'

    def get_template_names(self):
        return [
            f'mozorg/home/home-{self.card_data_lang}.html',
            'mozorg/home/home-en.html',
        ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_data = contentful.get_home_page_data(ctx['content_id'])
        ctx['card_layouts'] = page_data['layouts']
        self.card_data_lang = page_data['lang'].lower()
        return ctx

    def render_to_response(self, context, **response_kwargs):
        locale = get_locale(self.request)
        if not locale.startswith(self.card_data_lang):
            return HttpResponsePermanentRedirect(self.get_preview_url(context['content_id']))

        return super().render_to_response(context, **response_kwargs)
