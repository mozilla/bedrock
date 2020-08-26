from django.conf import settings

import jinja2
from django.template.loader import render_to_string
from django_jinja import library

from bedrock.firefox.firefox_details import firefox_desktop, firefox_android, firefox_ios
from bedrock.base.urlresolvers import reverse
from lib.l10n_utils import get_locale


def desktop_builds(channel, builds=None, locale=None, force_direct=False,
                   force_full_installer=False, force_funnelcake=False,
                   funnelcake_id=False, locale_in_transition=False, classified=False):
    builds = builds or []

    l_version = firefox_desktop.latest_builds(locale, channel)

    # Developer Edition is now based on the Beta channel, so the build list
    # should be generated from the Beta locales.
    if channel == 'alpha':
        l_version = firefox_desktop.latest_builds(locale, 'beta')

    if l_version:
        version, platforms = l_version
    else:
        locale = 'en-US'
        version, platforms = firefox_desktop.latest_builds('en-US', channel)

    for plat_os, plat_os_pretty in firefox_desktop.platforms(channel, classified):

        os_pretty = plat_os_pretty

        # Firefox Nightly: The Windows stub installer is now universal,
        # automatically detecting a 32-bit and 64-bit desktop, so the
        # win64-specific entry can be skipped.
        if channel == 'nightly':
            if plat_os == 'win':
                continue
            if plat_os == 'win64':
                plat_os = 'win'
                os_pretty = 'Windows 32/64-bit'

        # And generate all the info
        download_link = firefox_desktop.get_download_url(
            channel, version, plat_os, locale,
            force_direct=force_direct,
            force_full_installer=force_full_installer,
            force_funnelcake=force_funnelcake,
            funnelcake_id=funnelcake_id,
            locale_in_transition=locale_in_transition,
        )

        # If download_link_direct is False the data-direct-link attr
        # will not be output, and the JS won't attempt the IE popup.
        if force_direct:
            # no need to run get_download_url again with the same args
            download_link_direct = False
        else:
            download_link_direct = firefox_desktop.get_download_url(
                channel, version, plat_os, locale,
                force_direct=True,
                force_full_installer=force_full_installer,
                force_funnelcake=force_funnelcake,
                funnelcake_id=funnelcake_id,
            )
            if download_link_direct == download_link:
                download_link_direct = False

        builds.append({'os': plat_os,
                       'os_pretty': os_pretty,
                       'download_link': download_link,
                       'download_link_direct': download_link_direct})

    return builds


def android_builds(channel, builds=None):
    builds = builds or []
    link = firefox_android.get_download_url(channel.lower())
    builds.append({'os': 'android',
                   'os_pretty': 'Android',
                   'download_link': link})

    return builds


def ios_builds(channel, builds=None):
    builds = builds or []
    link = firefox_ios.get_download_url(channel)
    builds.append({'os': 'ios',
                   'os_pretty': 'iOS',
                   'download_link': link})

    return builds


@library.global_function
@jinja2.contextfunction
def download_firefox(ctx, channel='release', platform='all',
                     dom_id=None, locale=None, force_direct=False,
                     force_full_installer=False, force_funnelcake=False,
                     alt_copy=None, button_class='mzp-t-xl',
                     locale_in_transition=False, download_location=None):
    """ Output a "download firefox" button.

    :param ctx: context from calling template.
    :param channel: name of channel: 'release', 'beta', 'alpha', or 'nightly'.
    :param platform: Target platform: 'desktop', 'android', 'ios', or 'all'.
    :param dom_id: Use this string as the id attr on the element.
    :param locale: The locale of the download. Default to locale of request.
    :param force_direct: Force the download URL to be direct.
    :param force_full_installer: Force the installer download to not be
            the stub installer (for aurora).
    :param force_funnelcake: Force the download version for en-US Windows to be
            'latest', which bouncer will translate to the funnelcake build.
    :param alt_copy: Specifies alternate copy to use for download buttons.
    :param button_class: Classes to add to the download button, contains size mzp-t-xl by default
    :param locale_in_transition: Include the page locale in transitional download link.
    :param download_location: Specify the location of download button for
            GA reporting: 'primary cta', 'nav', 'sub nav', or 'other'.
    """
    show_desktop = platform in ['all', 'desktop']
    show_android = platform in ['all', 'android']
    show_ios = platform in ['all', 'ios']
    alt_channel = '' if channel == 'release' else channel
    locale = locale or get_locale(ctx['request'])
    funnelcake_id = ctx.get('funnelcake_id', False)
    dom_id = dom_id or 'download-button-%s-%s' % (
        'desktop' if platform == 'all' else platform, channel)

    # Gather data about the build for each platform
    builds = []

    if show_desktop:
        version = firefox_desktop.latest_version(channel)
        builds = desktop_builds(channel, builds, locale, force_direct,
                                force_full_installer, force_funnelcake,
                                funnelcake_id, locale_in_transition)

    if show_android:
        version = firefox_android.latest_version(channel)
        builds = android_builds(channel, builds)

    if show_ios:
        version = firefox_ios.latest_version(channel)
        builds.append({'os': 'ios',
                       'os_pretty': 'iOS',
                       'download_link': firefox_ios.get_download_url()})

    # Get the native name for current locale
    langs = firefox_desktop.languages
    locale_name = langs[locale]['native'] if locale in langs else locale

    data = {
        'locale_name': locale_name,
        'version': version,
        'product': 'firefox-%s' % platform,
        'builds': builds,
        'id': dom_id,
        'channel': alt_channel,
        'show_desktop': show_desktop,
        'show_android': show_android,
        'show_ios': show_ios,
        'alt_copy': alt_copy,
        'button_class': button_class,
        'download_location': download_location,
        'fluent_l10n': ctx['fluent_l10n']
    }

    html = render_to_string('firefox/includes/download-button.html', data,
                            request=ctx['request'])
    return jinja2.Markup(html)


@library.global_function
@jinja2.contextfunction
def download_firefox_thanks(ctx, dom_id=None, locale=None, alt_copy=None, button_class=None,
                            locale_in_transition=False, download_location=None):
    """ Output a simple "download firefox" button that only points to /download/thanks/

    :param ctx: context from calling template.
    :param dom_id: Use this string as the id attr on the element.
    :param locale: The locale of the download. Default to locale of request.
    :param alt_copy: Specifies alternate copy to use for download buttons.
    :param button_class: Classes to add to the download button, contains size mzp-t-xl by default
    :param locale_in_transition: Include the page locale in transitional download link.
    :param download_location: Specify the location of download button for
            GA reporting: 'primary cta', 'nav', 'sub nav', or 'other'.
    """

    channel = 'release'
    locale = locale or get_locale(ctx['request'])
    funnelcake_id = ctx.get('funnelcake_id', False)
    dom_id = dom_id or 'download-button-thanks'
    transition_url = '/firefox/download/thanks/'
    version = firefox_desktop.latest_version(channel)

    if funnelcake_id:
        # include funnelcake in /download/thanks/ URL
        transition_url += '?f=%s' % funnelcake_id

    if locale_in_transition:
        transition_url = '/%s%s' % (locale, transition_url)

    download_link_direct = firefox_desktop.get_download_url(
        channel, version, 'win', locale,
        force_direct=True,
        force_full_installer=False,
        force_funnelcake=False,
        funnelcake_id=funnelcake_id,
    )

    data = {
        'id': dom_id,
        'transition_url': transition_url,
        'download_link_direct': download_link_direct,
        'alt_copy': alt_copy,
        'button_class': button_class,
        'download_location': download_location,
        'fluent_l10n': ctx['fluent_l10n']
    }

    html = render_to_string('firefox/includes/download-button-thanks.html', data,
                            request=ctx['request'])
    return jinja2.Markup(html)


@library.global_function
@jinja2.contextfunction
def download_firefox_desktop_list(ctx, channel='release', dom_id=None, locale=None,
                                  force_full_installer=False):
    """
    Return a HTML list of platform download links for Firefox desktop

    :param channel: name of channel: 'release', 'beta',  'alpha' or 'nightly'.
    :param dom_id: Use this string as the id attr on the element.
    :param locale: The locale of the download. Default to locale of request.
    :param force_full_installer: Force the installer download to not be
            the stub installer (for aurora).

    """
    dom_id = dom_id or 'download-platform-list-%s' % (channel)
    locale = locale or get_locale(ctx['request'])

    # Make sure funnelcake_id is not passed as builds are often Windows only.
    builds = desktop_builds(channel, None, locale, True, force_full_installer,
                            False, False, False, True)

    recommended_builds = []
    traditional_builds = []

    for plat in builds:
        # Add 32-bit label for Windows and Linux builds.
        if channel != 'nightly':
            if plat['os'] == 'win':
                plat['os_pretty'] = 'Windows 32-bit'

        if plat['os'] == 'linux':
            plat['os_pretty'] = 'Linux 32-bit'

        if (plat['os'] in firefox_desktop.platform_classification['recommended'] or
                channel == 'nightly' and plat['os'] == 'win'):
            recommended_builds.append(plat)
        else:
            traditional_builds.append(plat)

    data = {
        'id': dom_id,
        'builds': {
            'recommended': recommended_builds,
            'traditional': traditional_builds,
        },
    }

    html = render_to_string('firefox/includes/download-list.html', data,
                            request=ctx['request'])
    return jinja2.Markup(html)


@library.global_function
def firefox_url(platform, page, channel=None):
    """
    Return a product-related URL like /firefox/all/ or /mobile/beta/notes/.

    Examples
    ========

    In Template
    -----------

        {{ firefox_url('desktop', 'all', 'organizations') }}
        {{ firefox_url('desktop', 'sysreq', channel) }}
        {{ firefox_url('android', 'notes') }}
    """

    kwargs = {}
    anchor = None

    # Tweak the channel name for the naming URL pattern in urls.py
    if channel == 'release':
        channel = None
    if channel == 'alpha':
        if platform == 'desktop':
            channel = 'developer'
        if platform == 'android':
            channel = 'aurora'
    if channel == 'esr':
        channel = 'organizations'

    # There is now only one /all page URL - issue 8096
    if page == 'all':
        if platform == 'desktop':
            if channel == 'beta':
                anchor = 'product-desktop-beta'
            elif channel == 'developer':
                anchor = 'product-desktop-developer'
            elif channel == 'nightly':
                anchor = 'product-desktop-nightly'
            elif channel == 'organizations':
                anchor = 'product-desktop-esr'
            else:
                anchor = 'product-desktop-release'
        elif platform == 'android':
            if channel == 'beta':
                anchor = 'product-android-beta'
            elif channel == 'nightly':
                anchor = 'product-android-nightly'
            else:
                anchor = 'product-android-release'
    else:
        if channel:
            kwargs['channel'] = channel
        if platform != 'desktop':
            kwargs['platform'] = platform

    # Firefox for Android and iOS have the system requirements page on SUMO
    if platform in ['android', 'ios'] and page == 'sysreq':
        return settings.FIREFOX_MOBILE_SYSREQ_URL

    anchor = '#' + anchor if anchor else ''
    return reverse(f'firefox.{page}', kwargs=kwargs) + anchor
