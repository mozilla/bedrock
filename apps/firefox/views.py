import re

from firefox import version_re
import l10n_utils
from product_details import product_details
from product_details.version_compare import Version
from funfactory.urlresolvers import reverse

from django.conf import settings
from django.http import HttpResponseRedirect
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


def whatsnew_redirect(request, fake_version):
    """
    Redirect visitors based on their user-agent.

    - Up-to-date Firefox users see the whatsnew page.
    - Other Firefox users go to the update page.
    - Non Firefox users go to the new page.
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if not 'Firefox' in user_agent:
        url = reverse('firefox.new')
        return HttpResponseRedirect(url)  # TODO : Where to redirect bug 757206

    user_version = "0"
    ua_regexp = r"Firefox/(%s)" % version_re
    match = re.search(ua_regexp, user_agent)
    if match:
        user_version = match.group(1)

    current_version = product_details.firefox_versions['LATEST_FIREFOX_VERSION']
    if Version(user_version) < Version(current_version):
        url = reverse('firefox.update')
        return HttpResponseRedirect(url)
    else:
        return l10n_utils.render(request, 'firefox/whatsnew.html')
