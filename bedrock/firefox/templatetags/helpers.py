from collections import OrderedDict

from django.conf import settings

import jinja2
from django.template.loader import render_to_string
from django_jinja import library

from bedrock.firefox.firefox_details import firefox_desktop, firefox_android, firefox_ios
from bedrock.base.urlresolvers import reverse
from lib.l10n_utils import get_locale


def desktop_builds(channel, builds=None, locale=None, force_direct=False,
                   force_full_installer=False, force_funnelcake=False,
                   funnelcake_id=False, locale_in_transition=False):
    builds = builds or []

    l_version = firefox_desktop.latest_builds(locale, channel)
    if l_version:
        version, platforms = l_version
    else:
        locale = 'en-US'
        version, platforms = firefox_desktop.latest_builds('en-US', channel)

    for plat_os, plat_os_pretty in firefox_desktop.platform_labels.iteritems():
        os_pretty = plat_os_pretty

        # Firefox Nightly: The Windows stub installer is now universal,
        # automatically detecting a 32-bit and 64-bit desktop, so the
        # win64-specific entry can be skipped.
        if channel == 'nightly':
            if plat_os == 'win':
                os_pretty = 'Windows 32/64-bit'
            if plat_os == 'win64':
                continue

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
    channel = channel.lower()
    builds = builds or []
    variations = OrderedDict([
        ('api-15', 'Ice Cream Sandwich+'),
        ('x86', 'x86'),
    ])

    if channel == 'aurora':
        channel = 'alpha'

    if channel == 'nightly':
        for type, arch_pretty in variations.iteritems():
            link = firefox_android.get_download_url(channel, type)
            builds.append({'os': 'android',
                           'os_pretty': 'Android',
                           'os_arch_pretty': 'Android %s' % arch_pretty,
                           'arch': 'x86' if type == 'x86' else 'armv7up %s' % type,
                           'arch_pretty': arch_pretty,
                           'download_link': link})
    else:
        link = firefox_android.get_download_url(channel)
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
                     alt_copy=None, button_color='button-green',
                     locale_in_transition=False):
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
    :param button_color: color of download button. Default to 'button-green'.
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
        'button_color': button_color,
    }

    html = render_to_string('firefox/includes/download-button.html', data,
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
    builds = desktop_builds(channel, None, locale, True,
                            force_full_installer, False, False)

    for plat in builds:
        # Add 32-bit label for Windows and Linux builds.
        if channel != 'nightly':
            if plat['os'] == 'win' or plat['os'] == 'winsha1':
                plat['os_pretty'] = 'Windows 32-bit'

        if plat['os'] == 'linux':
            plat['os_pretty'] = 'Linux 32-bit'

    data = {
        'id': dom_id,
        'builds': builds
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

    if channel:
        kwargs['channel'] = channel
    if platform != 'desktop':
        kwargs['platform'] = platform

    # Firefox for Android and iOS have the system requirements page on SUMO
    if platform in ['android', 'ios'] and page == 'sysreq':
        return settings.FIREFOX_MOBILE_SYSREQ_URL

    return reverse('firefox.%s' % page, kwargs=kwargs)
