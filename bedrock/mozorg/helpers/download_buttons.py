# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Download buttons. Let's get some terminology straight. Here is a list
of terms and example values for them:

* product: 'firefox' or 'thunderbird'
* version: 7.0, 8.0b3, 9.0a2
* build: 'beta', 'aurora', or None (for latest)
* platform: 'os_windows', 'os_linux', 'os_linux64', or 'os_osx'
* locale: a string in the form of 'en-US'
"""

from django.conf import settings

import jingo
import jinja2

from bedrock.firefox.firefox_details import firefox_details, mobile_details
from lib.l10n_utils import get_locale

nightly_desktop = ('https://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/'
                   'latest-mozilla-aurora')
nightly_android = ('https://ftp.mozilla.org/pub/mozilla.org/mobile/nightly/'
                   'latest-mozilla-aurora-android')

download_urls = {
    'transition': '/firefox/new/?scene=2#download-fx',
    'direct': 'https://download.mozilla.org/',
    'aurora': nightly_desktop,
    'aurora-l10n': nightly_desktop + '-l10n',
    'aurora-android-armv7': nightly_android + (
        '/en-US/fennec-%s.en-US.android-arm.apk'),
    'aurora-android-x86': nightly_android + (
        '-x86/fennec-%s.multi.android-i386.apk'),
}


def latest_version(locale, channel='release'):
    """Return build info for a locale and channel.

    :param locale: locale string of the build
    :param channel: channel of the build: release, beta, or aurora
    :return: dict or None
    """
    all_builds = (firefox_details.firefox_primary_builds,
                  firefox_details.firefox_beta_builds)
    version = firefox_details.latest_version(channel)

    for builds in all_builds:
        if locale in builds and version in builds[locale]:
            _builds = builds[locale][version]
            # Append Linux 64-bit build
            if 'Linux' in _builds:
                _builds['Linux 64'] = _builds['Linux']
            return version, _builds


def make_aurora_link(product, version, platform, locale,
                     force_full_installer=False):
    # Download links are different for localized versions
    src = 'aurora' if locale.lower() == 'en-us' else 'aurora-l10n'

    filenames = {
        'os_windows': 'win32.installer.exe',
        'os_linux': 'linux-i686.tar.bz2',
        'os_linux64': 'linux-x86_64.tar.bz2',
        'os_osx': 'mac.dmg'
    }
    if (not force_full_installer and settings.AURORA_STUB_INSTALLER
            and locale.lower() == 'en-us'):
        filenames['os_windows'] = 'win32.installer-stub.exe'
    filename = filenames[platform]

    return ('%s/%s-%s.%s.%s' %
            (download_urls[src], product, version, locale, filename))


def make_download_link(product, build, version, platform, locale,
                       force_direct=False, force_full_installer=False,
                       force_funnelcake=False, funnelcake_id=None):
    # Aurora has a special download link format
    if build == 'aurora':
        return make_aurora_link(product, version, platform, locale,
                                force_full_installer=force_full_installer)

    # The downloaders expect the platform in a certain format
    platform = {
        'os_windows': 'win',
        'os_linux': 'linux',
        'os_linux64': 'linux64',
        'os_osx': 'osx'
    }[platform]

    # stub installer exceptions
    # TODO: NUKE FROM ORBIT!
    stub_langs = settings.STUB_INSTALLER_LOCALES.get(platform, [])
    if stub_langs and (stub_langs == settings.STUB_INSTALLER_ALL or
                       locale.lower() in stub_langs):
        suffix = 'stub'
        if force_funnelcake or force_full_installer:
            suffix = 'latest'

        version = ('beta-' if build == 'beta' else '') + suffix
    elif not funnelcake_id:
        # Force download via SSL. Stub installers are always downloaded via SSL.
        # Funnelcakes may not be ready for SSL download
        version += '-SSL'

    # append funnelcake id to version if we have one
    if funnelcake_id:
        version = '{vers}-f{fc}'.format(vers=version, fc=funnelcake_id)

    # Check if direct download link has been requested
    # (bypassing the transition page)
    if force_direct:
        # build a direct download link
        tmpl = '?'.join([download_urls['direct'],
                        'product={prod}-{vers}&os={plat}&lang={locale}'])

        return tmpl.format(prod=product, vers=version,
                           plat=platform, locale=locale)
    else:
        # build a link to the transition page
        return download_urls['transition']


@jingo.register.function
@jinja2.contextfunction
def download_firefox(ctx, build='release', small=False, icon=True,
                     mobile=None, dom_id=None, locale=None, simple=False,
                     force_direct=False, force_full_installer=False,
                     force_funnelcake=False):
    """ Output a "download firefox" button.

    :param ctx: context from calling template.
    :param build: name of build: 'release', 'beta' or 'aurora'.
    :param small: Display the small button if True.
    :param icon: Display the Fx icon on the button if True.
    :param mobile: Display the android download button if True, the desktop
            button only if False, and by default (None) show whichever
            is appropriate for the user's system.
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
    :return: The button html.
    """
    alt_build = '' if build == 'release' else build
    platform = 'mobile' if mobile else 'desktop'
    locale = locale or get_locale(ctx['request'])
    funnelcake_id = ctx.get('funnelcake_id', False)
    dom_id = dom_id or 'download-button-%s-%s' % (platform, build)

    l_version = latest_version(locale, build)
    if l_version:
        version, platforms = l_version
    else:
        locale = 'en-US'
        version, platforms = latest_version('en-US', build)

    # Gather data about the build for each platform
    builds = []

    if not mobile:
        for plat_os in ['Windows', 'Linux', 'Linux 64', 'OS X']:
            # Bug 1069545
            # Have to serve OS X 32.0 until Apple whitelists 32.0.2 :/
            # TODO: REMOVE ME WHEN APPLE DOES THEIR JOB
            if plat_os == 'OS X' and version.startswith('32.0.'):
                version = '32.0'

            # Fallback to en-US if this plat_os/version isn't available
            # for the current locale
            _locale = locale
            if plat_os not in platforms:
                _locale = 'en-US'

            # Special case for the Japanese version for Mac
            if plat_os == 'OS X' and _locale == 'ja':
                _locale = 'ja-JP-mac'

            # Normalize the platform os name
            plat_os = 'os_%s' % plat_os.lower().replace(' ', '')
            plat_os_pretty = {
                'os_osx': 'Mac OS X',
                'os_windows': 'Windows',
                'os_linux': 'Linux',
                'os_linux64': 'Linux 64-bit',
            }[plat_os]

            # And generate all the info
            download_link = make_download_link(
                'firefox', build, version, plat_os, _locale,
                force_direct=force_direct,
                force_full_installer=force_full_installer,
                force_funnelcake=force_funnelcake,
                funnelcake_id=funnelcake_id,
            )

            # If download_link_direct is False the data-direct-link attr
            # will not be output, and the JS won't attempt the IE popup.
            if force_direct:
                # no need to run make_download_link again with the same args
                download_link_direct = False
            else:
                download_link_direct = make_download_link(
                    'firefox', build, version, plat_os, _locale,
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
    if mobile is not False:
        android_link = settings.GOOGLE_PLAY_FIREFOX_LINK

        if build == 'beta':
            android_link = android_link.replace('org.mozilla.firefox',
                                                'org.mozilla.firefox_beta')

        if build == 'aurora':
            for arch_pretty in ['ARMv7', 'x86']:
                arch = arch_pretty.lower()
                link = (download_urls['aurora-android-%s' % arch] %
                        mobile_details.latest_version('aurora'))

                builds.append({'os': 'os_android',
                               'os_pretty': 'Android',
                               'os_arch_pretty': 'Android %s' % arch_pretty,
                               'arch': arch,
                               'arch_pretty': arch_pretty,
                               'download_link': link})

        if build != 'aurora':
            builds.append({'os': 'os_android',
                           'os_pretty': 'Android',
                           'download_link': android_link})

    # Get the native name for current locale
    langs = firefox_details.languages
    locale_name = langs[locale]['native'] if locale in langs else locale

    data = {
        'locale_name': locale_name,
        'version': version,
        'product': 'firefox-mobile' if mobile else 'firefox',
        'builds': builds,
        'id': dom_id,
        'small': small,
        'simple': simple,
        'build': alt_build,
        'show_mobile': mobile is not False,
        'show_desktop': mobile is not True,
        'icon': icon,
    }

    html = jingo.render_to_string(ctx['request'],
                                  'mozorg/download_firefox_button.html',
                                  data)
    return jinja2.Markup(html)
