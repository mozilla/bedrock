# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import re

from django.conf import settings
from django.http import (
    Http404, HttpResponsePermanentRedirect, HttpResponseRedirect)
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.vary import vary_on_headers
from django.views.generic.base import TemplateView

import basket
from funfactory.urlresolvers import reverse
from jingo_minify.helpers import BUILD_ID_JS, BUNDLE_HASHES
from lib import l10n_utils
from rna.models import Release

from bedrock.firefox import version_re
from bedrock.firefox.forms import SMSSendForm
from bedrock.mozorg.views import process_partnership_form
from bedrock.mozorg.helpers.misc import releasenotes_url
from bedrock.firefox.utils import is_current_or_newer
from bedrock.firefox.firefox_details import firefox_details, mobile_details
from lib.l10n_utils.dotlang import _


UA_REGEXP = re.compile(r"Firefox/(%s)" % version_re)

LANG_FILES = ['firefox/partners/index']

LOCALE_FXOS_HEADLINES = {
    'de': {
        'title': u"Firefox OS ist richtungsweisend für die Zukunft des "
            "mobilen Marktes",
        'url': 'http://blog.mozilla.org/press-de/2014/02/23/'
            'firefox-os-ist-richtungsweisend-fur-die-zukunft-des-mobilen-marktes',
    },
    'en-GB': {
        'title': u'Firefox OS Unleashes the Future of Mobile',
        'url': 'http://blog.mozilla.org/press-uk/2014/02/23/'
            'firefox-os-unleashes-the-future-of-mobile'
    },
    'en-US': {
        'title': _('Firefox OS Unleashes the Future of Mobile'),
        'url': 'https://blog.mozilla.org/press/2014/02/firefox-os-future-2/',
    },
    'es-AR': {
        'title': u'Firefox OS te desvela el futuro de lo móvil',
        'url': 'http://blog.mozilla.org/press-latam/2014/02/23/'
            'firefox-os-te-desvela-el-futuro-de-lo-movil/',
    },
    'es-CL': {
        'title': u'Firefox OS te desvela el futuro de lo móvil',
        'url': 'http://blog.mozilla.org/press-latam/2014/02/23/'
            'firefox-os-te-desvela-el-futuro-de-lo-movil/',
    },
    'es-ES': {
        'title': u'Firefox OS te desvela el futuro de lo móvil',
        'url': 'https://blog.mozilla.org/press/2014/02/firefox-os-future-2/',
    },
    'es-MX': {
        'title': u'Firefox OS te desvela el futuro de lo móvil',
        'url': 'http://blog.mozilla.org/press-latam/2014/02/23/'
            'firefox-os-te-desvela-el-futuro-de-lo-movil/',
    },
    'fr': {
        'title': u'Firefox OS chamboule le futur du mobile',
        'url': 'http://blog.mozilla.org/press-fr/2014/02/23/'
            'firefox-os-chamboule-le-futur-du-mobile',
    },
    'it': {
        'title': u'Firefox OS svela il futuro del mobile',
        'url': 'http://blog.mozilla.org/press-it/2014/02/23/'
            'firefox-os-svela-il-futuro-del-mobile',
    },
    'pl': {
        'title': u'Firefox OS uwalnia przyszłość technologii mobilnej',
        'url': 'http://blog.mozilla.org/press-pl/2014/02/23/'
            'firefox-os-uwalnia-przyszlosc-technologii-mobilnej',
    },
    'pt-BR': {
        'title': u'Firefox OS apresenta o futuro dos dispositivos móveis',
        'url': 'https://blog.mozilla.org/press-br/2014/02/23/'
            'firefox-os-apresenta-o-futuro-dos-dispositivos-moveis/',
    },
}

INSTALLER_CHANNElS = [
    'release',
    'beta',
    'aurora',
    #'nightly',  # soon
]


def get_js_bundle_files(bundle):
    """
    Return a JSON string of the list of file names for lazy loaded
    javascript.
    """
    # mostly stolen from jingo_minify.helpers.js
    if settings.DEBUG:
        items = settings.MINIFY_BUNDLES['js'][bundle]
    else:
        build_id = BUILD_ID_JS
        bundle_full = "js:%s" % bundle
        if bundle_full in BUNDLE_HASHES:
            build_id = BUNDLE_HASHES[bundle_full]
        items = ("js/%s-min.js?build=%s" % (bundle, build_id,),)
    return json.dumps([settings.MEDIA_URL + i for i in items])


JS_COMMON = get_js_bundle_files('partners_common')
JS_MOBILE = get_js_bundle_files('partners_mobile')
JS_DESKTOP = get_js_bundle_files('partners_desktop')


def get_latest_version(product='firefox', channel='release'):
    if channel == 'organizations':
        channel = 'esr'

    if product == 'mobile':
        return mobile_details.latest_version(channel)
    else:
        return firefox_details.latest_version(channel)


def installer_help(request):
    installer_lang = request.GET.get('installer_lang', None)
    installer_channel = request.GET.get('channel', None)
    context = {
        'installer_lang': None,
        'installer_channel': None,
    }

    if installer_lang and installer_lang in firefox_details.languages:
        context['installer_lang'] = installer_lang

    if installer_channel and installer_channel in INSTALLER_CHANNElS:
        context['installer_channel'] = installer_channel

    return l10n_utils.render(request, 'firefox/installer-help.html', context)


@csrf_exempt
def sms_send(request):
    form = SMSSendForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            basket.send_sms(form.cleaned_data['number'],
                            'SMS_Android',
                            form.cleaned_data['optin'])
        except basket.BasketException:
            msg = form.error_class(
                [_('An error occurred in our system. '
                   'Please try again later.')]
            )
            form.errors['__all__'] = msg
        else:
            return HttpResponseRedirect(
                reverse('firefox.mobile.sms-thankyou'))
    return l10n_utils.render(request, 'firefox/mobile/sms-send.html',
                             {'sms_form': form})


def windows_billboards(req):
    major_version = req.GET.get('majorVersion')
    minor_version = req.GET.get('minorVersion')

    if major_version and minor_version:
        major_version = float(major_version)
        minor_version = float(minor_version)
        if major_version == 5 and minor_version == 1:
            return l10n_utils.render(req, 'firefox/unsupported/winxp.html')
    return l10n_utils.render(req, 'firefox/unsupported/win2k.html')


def fx_home_redirect(request):
    return HttpResponseRedirect(reverse('firefox.fx'))


def dnt(request):
    response = l10n_utils.render(request, 'firefox/dnt.html')
    response['Vary'] = 'DNT'
    return response


def all_downloads(request, channel):
    if channel is None:
        channel = 'release'

    if channel == 'organizations':
        channel = 'esr'

    version = get_latest_version('firefox', channel)
    query = request.GET.get('q')

    channel_names = {
        'release': _('Firefox'),
        'beta': _('Firefox Beta'),
        'aurora': _('Firefox Aurora'),
        'esr': _('Firefox Extended Support Release'),
    }

    return l10n_utils.render(request, 'firefox/all.html', {
        'full_builds': firefox_details.get_filtered_full_builds(version, query),
        'test_builds': firefox_details.get_filtered_test_builds(version, query),
        'query': query,
        'channel': channel,
        'channel_name': channel_names[channel],
    })


@csrf_protect
def firefox_partners(request):
    # If the current locale isn't in our list, return the en-US value
    press_locale = request.locale if (request.locale in LOCALE_FXOS_HEADLINES) else 'en-US'

    template_vars = {
        'locale_headline_url': LOCALE_FXOS_HEADLINES[press_locale]['url'],
        'locale_headline_title': LOCALE_FXOS_HEADLINES[press_locale]['title'],
        'js_common': JS_COMMON,
        'js_mobile': JS_MOBILE,
        'js_desktop': JS_DESKTOP,
    }

    form_kwargs = {'interest_set': 'fx', 'lead_source': 'www.mozilla.org/firefox/partners/'}

    return process_partnership_form(request, 'firefox/partners/index.html', 'firefox.partners.index', template_vars, form_kwargs)


def releases_index(request):
    releases = {}
    major_releases = firefox_details.firefox_history_major_releases
    minor_releases = firefox_details.firefox_history_stability_releases

    for release in major_releases:
        major_verion = float(re.findall(r'^\d+\.\d+', release)[0])
        # The version numbering scheme of Firefox changes sometimes. The second
        # number has not been used since Firefox 4, then reintroduced with
        # Firefox ESR 24 (Bug 870540). On this index page, 24.1.x should be
        # fallen under 24.0. This patter is a tricky part.
        major_pattern = r'^' + re.escape(('%s' if major_verion < 4 else '%g') % round(major_verion, 1))
        releases[major_verion] = {
            'major': release,
            'minor': sorted(filter(lambda x: re.findall(major_pattern, x),
                                   minor_releases),
                            key=lambda x: int(re.findall(r'\d+$', x)[0]))
        }

    return l10n_utils.render(request, 'firefox/releases/index.html',
                             {'releases': sorted(releases.items(), reverse=True)})


def latest_notes(request, product='firefox', channel='release'):
    version = get_latest_version(product, channel)

    if channel == 'beta':
        version = re.sub(r'b\d+$', 'beta', version)
    if channel == 'organizations':
        version = re.sub(r'esr$', '', version)

    dir = 'auroranotes' if channel == 'aurora' else 'releasenotes'
    path = [product, version, dir]
    locale = getattr(request, 'locale', None)
    if locale:
        path.insert(0, locale)
    return HttpResponseRedirect('/' + '/'.join(path) + '/')


def latest_sysreq(request, channel='release'):
    version = get_latest_version('firefox', channel)

    if channel == 'beta':
        version = re.sub(r'b\d+$', 'beta', version)
    if channel == 'organizations':
        version = re.sub(r'^(\d+).+', r'\1.0', version)

    path = ['firefox', version, 'system-requirements']
    locale = getattr(request, 'locale', None)
    if locale:
        path.insert(0, locale)
    return HttpResponseRedirect('/' + '/'.join(path) + '/')


class LatestFxView(TemplateView):
    """
    Base class to be extended by views that require visitor to be
    using latest version of Firefox. Classes extending this class must
    implement either `get_template_names` function or provide
    `template_name` class attribute.
    """

    @vary_on_headers('User-Agent')
    def dispatch(self, *args, **kwargs):
        return super(LatestFxView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # required for newsletter form post that is handled in newsletter/helpers.py
        return self.get(request, *args, **kwargs)

    def redirect_to(self):
        """
        Redirect visitors based on their user-agent.

        - Up-to-date Firefox users pass through.
        - Other Firefox users go to the new page.
        - Non Firefox users go to the new page.
        """
        query = self.request.META.get('QUERY_STRING')
        query = '?' + query if query else ''

        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        if not 'Firefox' in user_agent:
            return reverse('firefox.new') + query
            # TODO : Where to redirect bug 757206

        user_version = '0'
        match = UA_REGEXP.search(user_agent)
        if match:
            user_version = match.group(1)

        if not is_current_or_newer(user_version):
            return reverse('firefox.new') + query

        return None

    def render_to_response(self, context, **response_kwargs):
        redirect_url = self.redirect_to()

        if redirect_url is not None:
            return HttpResponsePermanentRedirect(redirect_url)
        else:
            return l10n_utils.render(self.request,
                                     self.get_template_names(),
                                     context,
                                     **response_kwargs)


class FirstrunView(LatestFxView):

    def get(self, request, *args, **kwargs):
        version = kwargs.get('fx_version')
        if version == '29.0' and not settings.DEV and not request.is_secure():
            uri = 'https://{host}{path}'.format(
                host=request.get_host(),
                path=request.get_full_path(),
            )
            return HttpResponsePermanentRedirect(uri)
        return super(FirstrunView, self).get(request, *args, **kwargs)

    def get_template_names(self):
        version = self.kwargs.get('fx_version')
        locale = l10n_utils.get_locale(self.request)

        if version == '29.0' and locale == 'en-US':
            template = 'firefox/australis/firstrun-tour.html'
        else:
            template = 'firefox/firstrun.html'

        # return a list to conform with original intention
        return [template]


class WhatsnewView(LatestFxView):
    # Locales targeted for FxOS
    fxos_locales = []

    locales_with_video = {
        'en-US': 'american',
        'en-GB': 'british',
        'de': 'german_final',
        'it': 'italian_final',
        'ja': 'japanese_final',
        'es-AR': 'spanish_final',
        'es-CL': 'spanish_final',
        'es-ES': 'spanish_final',
        'es-MX': 'spanish_final',
    }

    def get(self, request, *args, **kwargs):
        version = kwargs.get('fx_version')
        if version == '29.0' and not settings.DEV and not request.is_secure():
            uri = 'https://{host}{path}'.format(
                host=request.get_host(),
                path=request.get_full_path(),
            )
            return HttpResponsePermanentRedirect(uri)
        return super(WhatsnewView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(WhatsnewView, self).get_context_data(**kwargs)

        locale = l10n_utils.get_locale(self.request)

        if locale not in self.fxos_locales:
            ctx['locales_with_video'] = self.locales_with_video

        return ctx

    def get_template_names(self):
        version = self.kwargs.get('fx_version')
        locale = l10n_utils.get_locale(self.request)

        if version == '29.0a1':
            template = 'firefox/whatsnew-nightly-29.html'
        elif version == '29.0':
            template = 'firefox/australis/whatsnew-tour-a.html'
        elif locale in self.fxos_locales:
            template = 'firefox/whatsnew-fxos.html'
        else:
            template = 'firefox/whatsnew.html'

        # return a list to conform with original intention
        return [template]


class WhatsnewViewGATest(LatestFxView):

    template_name = 'firefox/australis/whatsnew-tour-b.html'

    def get(self, request, *args, **kwargs):
        if not settings.DEV and not request.is_secure():
            uri = 'https://{host}{path}'.format(
                host=request.get_host(),
                path=request.get_full_path(),
            )
            return HttpResponsePermanentRedirect(uri)
        return super(WhatsnewViewGATest, self).get(request, *args, **kwargs)


class TourView(LatestFxView):
    template_name = 'firefox/australis/firstrun-tour.html'

    def get(self, request, *args, **kwargs):
        if not settings.DEV and not request.is_secure():
            uri = 'https://{host}{path}'.format(
                host=request.get_host(),
                path=request.get_full_path(),
            )
            return HttpResponsePermanentRedirect(uri)
        return super(TourView, self).get(request, *args, **kwargs)


def release_notes_template(channel, product):
    if product == 'Firefox OS':
        return 'firefox/releases/os-notes.html'
    prefix = dict((c, c.lower()) for c in Release.CHANNELS)
    return 'firefox/releases/%s-notes.html' % prefix.get(channel, 'release')


def equivalent_release_url(release):
    equivalent_release = (release.equivalent_android_release() or
                          release.equivalent_desktop_release())
    if equivalent_release:
        return releasenotes_url(equivalent_release)


def get_release_or_404(version, product):
    release = get_object_or_404(Release, version=version, product=product)
    if not release.is_public and not settings.DEV:
        raise Http404
    return release


def release_notes(request, fx_version, product='Firefox'):
    if product == 'Firefox OS' and fx_version in (
            '1.0.1', '1.1', '1.2', '1.3'):
        return l10n_utils.render(
            request, 'firefox/os/notes-%s.html' % fx_version)

    try:
        release = get_release_or_404(fx_version, product)
    except Http404:
        release = get_release_or_404(fx_version + 'beta', product)
        return HttpResponseRedirect(releasenotes_url(release))

    new_features, known_issues = release.notes()
    return l10n_utils.render(
        request, release_notes_template(release.channel, product), {
            'version': fx_version,
            'major_version': fx_version.split('.', 1)[0],
            'release': release,
            'equivalent_release_url': equivalent_release_url(release),
            'new_features': new_features,
            'known_issues': known_issues})


def system_requirements(request, fx_version, product='Firefox'):
    release = get_release_or_404(fx_version, product)
    return l10n_utils.render(
        request, 'firefox/releases/system_requirements.html',
        {'release': release, 'version': fx_version})
