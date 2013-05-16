# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import re

from django.conf import settings
from django.http import (HttpResponsePermanentRedirect,
                         HttpResponseRedirect)
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.context_processors import csrf
from django.views.decorators.vary import vary_on_headers

import basket
from lib import l10n_utils
import requests
from jingo_minify.helpers import BUILD_ID_JS, BUNDLE_HASHES
from funfactory.urlresolvers import reverse


from bedrock.firefox import version_re
from bedrock.firefox.forms import SMSSendForm
from bedrock.mozorg.forms import WebToLeadForm
from bedrock.firefox.platforms import load_devices
from bedrock.firefox.utils import is_current_or_newer
from bedrock.firefox.firefox_details import firefox_details
from lib.l10n_utils.dotlang import _

UA_REGEXP = re.compile(r"Firefox/(%s)" % version_re)

LOCALE_OS_URLS = {
    'en-US': 'http://blog.mozilla.org/press/2013/02/firefox-os-expansion',
    'de': 'http://blog.mozilla.org/press-de/?p=760',
    'it': 'http://blog.mozilla.org/press-it/?p=353',
    'pl': 'http://blog.mozilla.org/press-pl/?p=407',
    'fr': 'http://blog.mozilla.org/press-fr/?p=366',
    'es-ES': 'http://blog.mozilla.org/press-es/?p=340',
    'en-GB': 'http://blog.mozilla.org/press-uk/?p=471'
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
            return l10n_utils.render(req, 'firefox/unsupported-winxp.html')
    return l10n_utils.render(req, 'firefox/unsupported-win2k.html')


def platforms(request):
    file = settings.MEDIA_ROOT + '/devices.csv'
    return l10n_utils.render(request, 'firefox/mobile/platforms.html',
                             {'devices': load_devices(request, file)})


def dnt(request):
    response = l10n_utils.render(request, 'firefox/dnt.html')
    response['Vary'] = 'DNT'
    return response


@vary_on_headers('User-Agent')
def latest_fx_redirect(request, fake_version, template_name):
    """
    Redirect visitors based on their user-agent.

    - Up-to-date Firefox users see the whatsnew page.
    - Other Firefox users go to the update page.
    - Non Firefox users go to the new page.
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if not 'Firefox' in user_agent:
        url = reverse('firefox.new')
        # TODO : Where to redirect bug 757206
        return HttpResponsePermanentRedirect(url)

    user_version = "0"
    match = UA_REGEXP.search(user_agent)
    if match:
        user_version = match.group(1)

    if not is_current_or_newer(user_version):
        url = reverse('firefox.update')
        return HttpResponsePermanentRedirect(url)

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
    return l10n_utils.render(request, template_name,
                             {'locales_with_video': locales_with_video})


def all_downloads(request):
    version = firefox_details.latest_version('release')
    query = request.GET.get('q')
    return l10n_utils.render(request, 'firefox/all.html', {
        'full_builds': firefox_details.get_filtered_full_builds(version, query),
        'test_builds': firefox_details.get_filtered_test_builds(version, query),
        'query': query,
    })


@csrf_protect
def firefox_partners(request):
    # If the current locale isn't in our list, return the en-US value
    locale_os_url = LOCALE_OS_URLS.get(request.locale, LOCALE_OS_URLS['en-US'])

    form = WebToLeadForm()

    template_vars = {
        'locale_os_url': locale_os_url,
        'js_common': JS_COMMON,
        'js_mobile': JS_MOBILE,
        'js_desktop': JS_DESKTOP,
        'form': form,
    }

    template_vars.update(csrf(request))

    return l10n_utils.render(request, 'firefox/partners/index.html', template_vars)


def firstrun_new(request, view, version):
    # only Firefox users should see the firstrun pages
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if not 'Firefox' in user_agent:
        url = reverse('firefox.new')
        return HttpResponsePermanentRedirect(url)

    # only users on the latest version should see the
    # new pages (for GA experiment data purity)
    user_version = "0"
    ua_regexp = r"Firefox/(%s)" % version_re
    match = re.search(ua_regexp, user_agent)
    if match:
        user_version = match.group(1)

    if not is_current_or_newer(user_version):
        url = reverse('firefox.update')
        return HttpResponsePermanentRedirect(url)

    # b only has 1-4 version
    if (view == 'b' and (int(version) < 1 or int(version) > 4)):
        version = '1'

    if (view == 'a'):
        copy = 'a' if (version in '123') else 'b'
    else:
        copy = 'a' if (version in '12') else 'b'

    template_vars = {
        'version': version,
        'copy': copy,
    }

    template = view + '.html'

    return l10n_utils.render(request, 'firefox/firstrun/' + template, template_vars)
