# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import re

from django.conf import settings
from django.http import (HttpResponsePermanentRedirect,
                         HttpResponseRedirect)
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.vary import vary_on_headers
from django.views.generic.base import TemplateView

import basket
from lib import l10n_utils
from jingo_minify.helpers import BUILD_ID_JS, BUNDLE_HASHES
from funfactory.urlresolvers import reverse


from bedrock.firefox import version_re
from bedrock.firefox.forms import SMSSendForm
from bedrock.mozorg.context_processors import funnelcake_param
from bedrock.mozorg.views import process_partnership_form
from bedrock.firefox.utils import is_current_or_newer
from bedrock.firefox.firefox_details import firefox_details, mobile_details
from lib.l10n_utils.dotlang import _

UA_REGEXP = re.compile(r"Firefox/(%s)" % version_re)

LOCALE_OS_URLS = {
    'en-US': 'https://blog.mozilla.org/press/2013/02/firefox-os-expansion',
    'de': 'https://blog.mozilla.org/press-de/?p=760',
    'it': 'https://blog.mozilla.org/press-it/?p=353',
    'pl': 'https://blog.mozilla.org/press-pl/?p=407',
    'fr': 'https://blog.mozilla.org/press-fr/?p=366',
    'es-ES': 'https://blog.mozilla.org/press-es/?p=340',
    'en-GB': 'https://blog.mozilla.org/press-uk/?p=471'
}

LOCALE_OS_RELEASE_URLS = {
    'de': 'https://blog.mozilla.org/press-de/2013/07/01/'
          'mozilla-und-partner-machen-sich-bereit-fur-den-ersten-firefox-os-launch/',
    'en-GB': 'https://blog.mozilla.org/press-uk/2013/07/01/'
             'mozilla-and-partners-prepare-to-launch-first-firefox-os-smartphones/',
    'en-US': 'https://blog.mozilla.org/blog/2013/07/01/'
             'mozilla-and-partners-prepare-to-launch-first-firefox-os-smartphones',
    'es-ES': 'https://blog.mozilla.org/press-es/?p=482',
    'fr': 'https://blog.mozilla.org/press-fr/2013/07/01/'
          'mozilla-et-ses-partenaires-preparent-le-lancement-des-premiers-smartphones-sous-firefox-os/',
    'it': 'https://blog.mozilla.org/press-it/2013/07/01/'
          'mozilla-e-i-suoi-partner-si-preparano-al-lancio-dei-primi-smartphone-con-firefox-os/',
    'pl': 'https://blog.mozilla.org/press-pl/2013/07/01/'
          'mozilla-wraz-z-partnerami-przygotowuje-sie-do-wprowadzenia-na-rynek-pierwszych-smartfonow-z-firefox-os/',
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


def all_downloads(request):
    version = get_latest_version()
    query = request.GET.get('q')
    return l10n_utils.render(request, 'firefox/all.html', {
        'full_builds': firefox_details.get_filtered_full_builds(version, query),
        'test_builds': firefox_details.get_filtered_test_builds(version, query),
        'query': query,
    })


@csrf_protect
def firefox_partners(request):
    # If the current locale isn't in our list, return the en-US value
    # MWC announcement
    locale_os_url = LOCALE_OS_URLS.get(request.locale, LOCALE_OS_URLS['en-US'])
    # Firefox OS 1.0 release
    locale_os_release_url = LOCALE_OS_RELEASE_URLS.get(request.locale, LOCALE_OS_RELEASE_URLS['en-US'])

    template_vars = {
        'locale_os_url': locale_os_url,
        'locale_os_release_url': locale_os_release_url,
        'locale_os_release_active': LOCALE_OS_RELEASE_URLS,
        'js_common': JS_COMMON,
        'js_mobile': JS_MOBILE,
        'js_desktop': JS_DESKTOP,
    }

    form_kwargs = {'interest_set': 'fx'}

    return process_partnership_form(request, 'firefox/partners/index.html', 'firefox.partners.index', template_vars, form_kwargs)


def releases_index(request):
    releases = {}
    major_releases = firefox_details.firefox_history_major_releases
    minor_releases = firefox_details.firefox_history_stability_releases

    for release in major_releases:
        releases[float(re.findall(r'^\d+\.\d+', release)[0])] = {
            'major': release,
            'minor': sorted(filter(lambda x: re.findall(r'^' + re.escape(release), x),
                                   minor_releases),
                            key=lambda x: int(re.findall(r'\d+$', x)[0]))
        }

    return l10n_utils.render(request, 'firefox/releases/index.html',
                             {'releases': sorted(releases.items(), reverse=True)})


def latest_notes(request, product, channel='release'):
    version = get_latest_version(product, channel)
    path = [
        product,
        re.sub(r'b\d+$', 'beta', version) if channel == 'beta' else version,
        'auroranotes' if channel == 'aurora' else 'releasenotes'
    ]
    locale = getattr(request, 'locale', None)
    if locale:
        path.insert(0, locale)
    return HttpResponseRedirect('/' + '/'.join(path) + '/')


def latest_sysreq(request):
    path = [
        'firefox',
        get_latest_version(),
        'system-requirements'
    ]
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
    funnelcake_campaign = '25'

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        fc_ctx = funnelcake_param(self.request)

        if (locale == 'en-US' and
                fc_ctx.get('funnelcake_id', 0) == self.funnelcake_campaign):

            template = 'firefox/firstrun-a.html'
        else:
            template = 'firefox/firstrun.html'

        return template


class WhatsnewView(LatestFxView):
    # Locales targeted for FxOS
    fxos_locales = ['pl']

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

    def get_context_data(self, **kwargs):
        ctx = super(WhatsnewView, self).get_context_data(**kwargs)

        locale = l10n_utils.get_locale(self.request)

        if (locale not in self.fxos_locales):
            ctx['locales_with_video'] = self.locales_with_video

        return ctx

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        if locale in self.fxos_locales:
            template = 'firefox/whatsnew-fxos.html'
        else:
            template = 'firefox/whatsnew.html'
        return template
