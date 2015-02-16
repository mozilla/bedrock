# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Download buttons. Let's get some terminology straight. Here is a list
of terms and example values for them:

* product: 'firefox' or 'thunderbird'
* version: 7.0, 8.0b3, 9.0a2
* channel: 'beta', 'alpha', or None (for latest)
* platform: 'win', 'osx', 'linux' and 64-bit variants
* locale: a string in the form of 'en-US'
"""

import jingo
import jinja2

from bedrock.firefox.firefox_details import firefox_desktop, firefox_android
from lib.l10n_utils import get_locale


def android_builds(channel, builds=None):
    builds = builds or []
    variations = {
        'api-9': 'Gingerbread',
        'api-11': 'Honeycomb+ ARMv7',
        'x86': 'x86',
    }

    if channel == 'alpha':
        for type, arch_pretty in variations.iteritems():
            link = firefox_android.get_download_url('alpha', type)
            builds.append({'os': 'android',
                           'os_pretty': 'Android',
                           'os_arch_pretty': 'Android %s' % arch_pretty,
                           'arch': 'x86' if type == 'x86' else 'armv7 %s' % type,
                           'arch_pretty': arch_pretty,
                           'download_link': link})

    if channel != 'alpha':
        link = firefox_android.get_download_url(channel)
        builds.append({'os': 'android',
                       'os_pretty': 'Android',
                       'download_link': link})

    return builds


@jingo.register.function
@jinja2.contextfunction
def download_firefox(ctx, channel='release', small=False, icon=True,
                     platform='all', dom_id=None, locale=None, simple=False,
                     force_direct=False, force_full_installer=False,
                     force_funnelcake=False, check_old_fx=False):
    """ Output a "download firefox" button.

    :param ctx: context from calling template.
    :param channel: name of channel: 'release', 'beta' or 'alpha'.
    :param small: Display the small button if True.
    :param icon: Display the Fx icon on the button if True.
    :param platform: Target platform: 'desktop', 'android' or 'all'.
    :param dom_id: Use this string as the id attr on the element.
    :param locale: The locale of the download. Default to locale of request.
    :param simple: Display button with text only if True. Will not display
            icon or privacy/what's new/systems & languages links. Can be used
            in conjunction with 'small'.
    :param force_direct: Force the download URL to be direct.
    :param force_full_installer: Force the installer download to not be
            the stub installer (for aurora).
    :param force_funnelcake: Force the download version for en-US Windows to be
            'latest', which bouncer will translate to the funnelcake build.
    :param check_old_fx: Checks to see if the user is on an old version of
            Firefox and, if true, changes the button text from 'Free Download'
            to 'Update your Firefox'. Must be used in conjunction with
            'simple' param being true.
    :return: The button html.
    """
    show_desktop = platform in ['all', 'desktop']
    show_android = platform in ['all', 'android']
    alt_channel = '' if channel == 'release' else channel
    locale = locale or get_locale(ctx['request'])
    funnelcake_id = ctx.get('funnelcake_id', False)
    dom_id = dom_id or 'download-button-%s-%s' % (
        'desktop' if platform == 'all' else platform, channel)

    l_version = firefox_desktop.latest_builds(locale, channel)
    if l_version:
        version, platforms = l_version
    else:
        locale = 'en-US'
        version, platforms = firefox_desktop.latest_builds('en-US', channel)

    # Gather data about the build for each platform
    builds = []

    if show_desktop:
        for plat_os, info in firefox_desktop.platform_info.iteritems():

            # Fallback to en-US if this platform/version isn't available
            # for the current locale
            plat_os_pretty = info['title']
            _locale = locale if plat_os_pretty in platforms else 'en-US'

            # And generate all the info
            download_link = firefox_desktop.get_download_url(
                channel, version, plat_os, _locale,
                force_direct=force_direct,
                force_full_installer=force_full_installer,
                force_funnelcake=force_funnelcake,
                funnelcake_id=funnelcake_id,
            )

            # If download_link_direct is False the data-direct-link attr
            # will not be output, and the JS won't attempt the IE popup.
            if force_direct:
                # no need to run get_download_url again with the same args
                download_link_direct = False
            else:
                download_link_direct = firefox_desktop.get_download_url(
                    channel, version, plat_os, _locale,
                    force_direct=True,
                    force_full_installer=force_full_installer,
                    force_funnelcake=force_funnelcake,
                    funnelcake_id=funnelcake_id,
                )
                if download_link_direct == download_link:
                    download_link_direct = False

            builds.append({'os': plat_os,
                           'os_pretty': plat_os_pretty,
                           'download_link': download_link,
                           'download_link_direct': download_link_direct})
    if show_android:
        builds = android_builds(channel, builds)

    # Get the native name for current locale
    langs = firefox_desktop.languages
    locale_name = langs[locale]['native'] if locale in langs else locale

    data = {
        'locale_name': locale_name,
        'version': version,
        'product': 'firefox-android' if platform == 'android' else 'firefox',
        'builds': builds,
        'id': dom_id,
        'small': small,
        'simple': simple,
        'channel': alt_channel,
        'show_android': show_android,
        'show_desktop': show_desktop,
        'icon': icon,
        'check_old_fx': check_old_fx and simple,
    }

    html = jingo.render_to_string(ctx['request'],
                                  'mozorg/download_firefox_button.html',
                                  data)
    return jinja2.Markup(html)
