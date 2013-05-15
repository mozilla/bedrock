# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Download buttons. Let's get some terminology straight. Here is a list
of terms and example values for them:

* product: 'firefox' or 'thunderbird'
* version: 7.0, 8.0b3, 9.0a2
* build: 'beta', 'aurora', or None (for latest)
* platform: 'os_windows', 'os_linux', or 'os_osx'
* locale: a string in the form of 'en-US'
"""

from distutils.version import StrictVersion

from django.conf import settings

import jingo
import jinja2
from product_details import product_details


download_urls = {
    'transition': '/{locale}/products/download.html',
    'direct': 'https://download.mozilla.org/',
    'aurora': 'https://ftp.mozilla.org/pub/mozilla.org/firefox/'
              'nightly/latest-mozilla-aurora',
    'aurora-l10n': 'https://ftp.mozilla.org/pub/mozilla.org/firefox/'
                   'nightly/latest-mozilla-aurora-l10n',
    'aurora-mobile': 'https://ftp.mozilla.org/pub/mozilla.org/mobile/'
                     'nightly/latest-mozilla-aurora-android/en-US/'
                     'fennec-%s.en-US.android-arm.apk' %
                     product_details.mobile_details['alpha_version'],
}


def _latest_pre_version(locale, version):
    builds = product_details.firefox_primary_builds
    vers = product_details.firefox_versions[version]

    if locale in builds and vers in builds[locale]:
        return vers, builds[locale][vers]


def latest_aurora_version(locale):
    return _latest_pre_version(locale, 'FIREFOX_AURORA')


def latest_beta_version(locale):
    return _latest_pre_version(locale, 'LATEST_FIREFOX_DEVEL_VERSION')


def latest_version(locale):
    fx_versions = product_details.firefox_versions
    beta_vers = fx_versions['FIREFOX_AURORA']
    aurora_vers = fx_versions['LATEST_FIREFOX_DEVEL_VERSION']
    esr_vers = fx_versions['FIREFOX_ESR']

    def _check_builds(builds):
        if locale in builds and isinstance(builds[locale], dict):
            greatest = None

            for version, info in builds[locale].items():
                match = (version != beta_vers and
                         version != aurora_vers and
                         version != esr_vers and
                         info)
                if match:
                    if not greatest:
                        greatest = version
                    elif StrictVersion(version) > StrictVersion(greatest):
                            greatest = version

            if greatest:
                return greatest, builds[locale][greatest]
            return None

    return (_check_builds(product_details.firefox_primary_builds) or
            _check_builds(product_details.firefox_beta_builds))


def make_aurora_link(product, version, platform, locale,
                     force_full_installer=False):
    # Download links are different for localized versions
    src = 'aurora' if locale.lower() == 'en-us' else 'aurora-l10n'

    filenames = {
        'os_windows': 'win32.installer.exe',
        'os_linux': 'linux-i686.tar.bz2',
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
                       force_funnelcake=False, force_stub_installer=False):
    # Aurora has a special download link format
    if build == 'aurora':
        return make_aurora_link(product, version, platform, locale,
                                force_full_installer=force_full_installer)

    # The downloaders expect the platform in a certain format
    platform = {
        'os_windows': 'win',
        'os_linux': 'linux',
        'os_osx': 'osx'
    }[platform]

    # en-US windows exceptions
    # TODO: NUKE FROM ORBIT!
    if force_funnelcake or force_full_installer or force_stub_installer:
        if locale.lower() == 'en-us' and platform == 'win':
            suffix = 'latest'
            if force_stub_installer:
                suffix = 'stub'

            version = ('beta-' if build == 'beta' else '') + suffix

    # Figure out the base url. certain locales have a transitional
    # thankyou-style page (most do)
    src = 'direct'
    if locale in settings.LOCALES_WITH_TRANSITION and not force_direct:
        src = 'transition'

    tmpl = '?'.join([download_urls[src], 'product={prod}-{vers}&os={plat}'
                                         '&lang={locale}'])

    return tmpl.format(prod=product, vers=version,
                       plat=platform, locale=locale)


@jingo.register.function
@jinja2.contextfunction
def download_firefox(ctx, build='release', small=False, icon=True,
                     mobile=None, dom_id=None, locale=None,
                     force_direct=False, force_full_installer=False,
                     force_funnelcake=False, force_stub_installer=False):
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
    :param force_direct: Force the download URL to be direct.
    :param force_full_installer: Force the installer download to not be
            the stub installer (for aurora).
    :param force_funnelcake: Force the download version for en-US Windows to be
            'latest', which bouncer will translate to the funnelcake build.
    :param force_stub_installer: Force the download link for en-US windows to
            be for the stub installer (for release and beta).
    :return: The button html.
    """
    alt_build = '' if build == 'release' else build
    platform = 'mobile' if mobile else 'desktop'
    locale = locale or ctx['request'].locale
    dom_id = dom_id or 'download-button-%s-%s' % (platform, build)

    def latest(locale):
        if build == 'aurora':
            return latest_aurora_version(locale)
        elif build == 'beta':
            return latest_beta_version(locale)
        else:
            return latest_version(locale)

    version, platforms = latest(locale) or latest('en-US')

    # Gather data about the build for each platform
    builds = []

    if not mobile:
        for plat_os in ['Windows', 'Linux', 'OS X']:
            # Fallback to en-US if this plat_os/version isn't available
            # for the current locale
            _locale = locale
            if plat_os not in platforms:
                _locale = 'en-US'

            # Normalize the platform os name
            plat_os = 'os_%s' % plat_os.lower().replace(' ', '')
            plat_os_pretty = {
                'os_osx': 'Mac OS X',
                'os_windows': 'Windows',
                'os_linux': 'Linux'
            }[plat_os]

            # And generate all the info
            download_link = make_download_link(
                'firefox', build, version, plat_os,
                _locale, force_direct, force_full_installer, force_funnelcake,
                force_stub_installer)

            # If download_link_direct is False the data-direct-link attr
            # will not be output, and the JS won't attempt the IE popup.
            if force_direct:
                # no need to run make_download_link again with the same args
                download_link_direct = False
            else:
                download_link_direct = make_download_link(
                    'firefox', build, version, plat_os,
                    _locale, True, force_full_installer, force_funnelcake,
                    force_stub_installer)
                if download_link_direct == download_link:
                    download_link_direct = False

            builds.append({'os': plat_os,
                           'os_pretty': plat_os_pretty,
                           'download_link': download_link,
                           'download_link_direct': download_link_direct})
    if mobile is not False:
        if build == 'aurora':
            android_link = download_urls['aurora-mobile']
        elif build == 'beta':
            android_link = ('https://market.android.com/details?'
                            'id=org.mozilla.firefox_beta')
        else:
            android_link = ('https://market.android.com/details?'
                            'id=org.mozilla.firefox')

        builds.append({'os': 'os_android',
                       'os_pretty': 'Android',
                       'download_link': android_link})

    # Get the native name for current locale
    langs = product_details.languages
    locale_name = langs[locale]['native'] if locale in langs else locale

    data = {
        'locale_name': locale_name,
        'version': version,
        'product': 'firefox-mobile' if mobile else 'firefox',
        'builds': builds,
        'id': dom_id,
        'small': small,
        'build': alt_build,
        'show_mobile': mobile is not False,
        'show_desktop': mobile is not True,
        'icon': icon,
    }

    html = jingo.render_to_string(ctx['request'],
                                  'mozorg/download_firefox_button.html',
                                  data)
    return jinja2.Markup(html)
