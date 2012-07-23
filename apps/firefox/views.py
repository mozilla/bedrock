import re
from time import time

from django.conf import settings
from django.views.decorators.vary import vary_on_headers
from django.http import HttpResponsePermanentRedirect

from django_statsd.clients import statsd
from funfactory.urlresolvers import reverse
from product_details import product_details
from product_details.version_compare import Version

from firefox import version_re
import l10n_utils
from platforms import load_devices


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
def whatsnew_redirect(request, fake_version):
    """
    Redirect visitors based on their user-agent.

    - Up-to-date Firefox users see the whatsnew page.
    - Other Firefox users go to the update page.
    - Non Firefox users go to the new page.
    """
    start = time()
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if not 'Firefox' in user_agent:
        url = reverse('firefox.new')
        response = HttpResponsePermanentRedirect(url)
        dt = int((time() - start) * 1000)
        statsd.timing('whatsnew.not_firefox', dt)
        return response

    user_version = "0"
    ua_regexp = r"Firefox/(%s)" % version_re
    match = re.search(ua_regexp, user_agent)
    if match:
        user_version = match.group(1)

    current_version = product_details.firefox_versions['LATEST_FIREFOX_VERSION']
    if Version(user_version) < Version(current_version):
        url = reverse('firefox.update')
        response = HttpResponsePermanentRedirect(url)
        dt = int((time() - start) * 1000)
        statsd.timing('whatsnew.old_firefox', dt)
        return response

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
    response = l10n_utils.render(request, 'firefox/whatsnew.html',
                                 {'locales_with_video': locales_with_video})
    dt = int((time() - start) * 1000)
    statsd.timing('whatsnew.uptodate_firefox', dt)
    return response
