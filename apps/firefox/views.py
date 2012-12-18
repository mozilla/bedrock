# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.vary import vary_on_headers

import basket
from product_details import product_details
from product_details.version_compare import Version
from funfactory.urlresolvers import reverse

import l10n_utils
from firefox import version_re
from firefox.forms import SMSSendForm
from firefox.platforms import load_devices
from l10n_utils.dotlang import _


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
    ua_regexp = r"Firefox/(%s)" % version_re
    match = re.search(ua_regexp, user_agent)
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


def is_current_or_newer(user_version):
    """
    Return true if the version (X.Y only) is for the latest Firefox or newer.
    """
    latest = Version(product_details.firefox_versions['LATEST_FIREFOX_VERSION'])
    user = Version(user_version)

    # similar to the way comparison is done in the Version class,
    # but only using the major and minor versions.
    latest_int = int('%d%02d' % (latest.major, latest.minor1))
    user_int = int('%d%02d' % (user.major or 0, user.minor1 or 0))
    return user_int >= latest_int
