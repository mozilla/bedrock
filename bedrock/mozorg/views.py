# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render as django_render
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView

from commonware.decorators import xframe_allow

from bedrock.base.waffle import switch
from bedrock.contentcards.models import get_page_content_cards
from bedrock.mozorg.credits import CreditsFile
from bedrock.mozorg.forums import ForumsFile
from bedrock.mozorg.models import ContributorActivity
from bedrock.mozorg.util import (
    fxa_concert_rsvp,
    get_fxa_oauth_token,
    get_fxa_profile_email,
    HttpResponseJSON
)
from bedrock.pocketfeed.models import PocketArticle
from bedrock.wordpress.views import BlogPostsView
from lib import l10n_utils
from lib.l10n_utils.dotlang import lang_file_is_active

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


def about_view(request):
    locale = l10n_utils.get_locale(request)
    variant = request.GET.get('v', None)
    allowed_variants = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    # ensure variant matches pre-defined value
    if variant not in allowed_variants:
        variant = None

    if lang_file_is_active('mozorg/about-2019', locale):
        if variant == 'a':
            template_name = 'mozorg/perf-exp/control.html'
        elif variant in allowed_variants:
            template_name = 'mozorg/perf-exp/variation.html'
        else:
            template_name = 'mozorg/about-2019.html'
    else:
        template_name = 'mozorg/about.html'

    return l10n_utils.render(request, template_name, {'variant': variant})


def moss_view(request):
    locale = l10n_utils.get_locale(request)

    if lang_file_is_active('mozorg/moss/index-092018', locale):
        template_name = 'mozorg/moss/index-092018.html'
    else:
        template_name = 'mozorg/moss/index.html'

    return l10n_utils.render(request, template_name)


@never_cache
def oauth_fxa(request):
    """
    Acts as an OAuth relier for Firefox Accounts. Currently specifically tuned to handle
    the OAuth flow for the Firefox Concert Series (Q4 2018).

    If additional OAuth flows are required in the future, please refactor this method.
    """
    if not switch('firefox_concert_series'):
        return HttpResponseRedirect(reverse('mozorg.home'))

    # expected state should be in user's cookies
    stateExpected = request.COOKIES.get('fxaOauthState', None)

    # provided state passed back from FxA - these state values should match
    stateProvided = request.GET.get('state', None)

    # code must be present - is in redirect querystring from FxA
    code = request.GET.get('code', None)

    error = False
    cookie_age = 86400  # 1 day

    # ensure all the data we need is present and valid
    if not (stateExpected and stateProvided and code):
        error = True
    elif stateExpected != stateProvided:
        error = True
    else:
        token = get_fxa_oauth_token(code)

        if not token:
            error = True
        else:
            email = get_fxa_profile_email(token)

            if not email:
                error = True
            else:
                # add email to mailing list

                # check for Firefox
                include_re = re.compile(r'\bFirefox\b', flags=re.I)
                exclude_re = re.compile(r'\b(Camino|Iceweasel|SeaMonkey)\b', flags=re.I)

                value = request.META.get('HTTP_USER_AGENT', '')
                isFx = bool(include_re.search(value) and not exclude_re.search(value))

                # add user to mailing list for future concert updates
                rsvp_ok = fxa_concert_rsvp(email, isFx)

                if not rsvp_ok:
                    error = True

    if error:
        # send user to a custom error page
        response = HttpResponseRedirect(reverse('mozorg.oauth.fxa-error'))
    else:
        # send user back to the concerts page
        response = HttpResponseRedirect(reverse('firefox.concerts'))
        response.set_cookie('fxaOauthVerified', True, max_age=cookie_age, httponly=False)

    return response


def oauth_fxa_error(request):
    if switch('firefox_concert_series'):
        return l10n_utils.render(request, 'mozorg/oauth/fxa-error.html')
    else:
        return HttpResponseRedirect(reverse('mozorg.home'))
