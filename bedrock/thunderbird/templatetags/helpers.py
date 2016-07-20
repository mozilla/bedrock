# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jinja2
from django.template.loader import render_to_string
from django_jinja import library

from bedrock.thunderbird.details import thunderbird_desktop
from bedrock.base.urlresolvers import reverse
from lib.l10n_utils import get_locale


@library.global_function
@jinja2.contextfunction
def download_thunderbird(ctx, channel='release', dom_id=None,
                         locale=None, force_direct=False,
                         alt_copy=None, button_color='green'):
    """ Output a "Download Thunderbird" button.

    :param ctx: context from calling template.
    :param channel: name of channel: 'release', 'beta' or 'alpha'.
    :param dom_id: Use this string as the id attr on the element.
    :param locale: The locale of the download. Default to locale of request.
    :param force_direct: Force the download URL to be direct.
    :param alt_copy: Specifies alternate copy to use for download buttons.
    :param button_color: color of download button. Default to 'green'.
    :return: The button html.
    """
    alt_channel = '' if channel == 'release' else channel
    locale = locale or get_locale(ctx['request'])
    dom_id = dom_id or 'download-button-desktop-%s' % channel

    l_version = thunderbird_desktop.latest_builds(locale, channel)
    if l_version:
        version, platforms = l_version
    else:
        locale = 'en-US'
        version, platforms = thunderbird_desktop.latest_builds('en-US', channel)

    # Gather data about the build for each platform
    builds = []

    for plat_os, plat_os_pretty in thunderbird_desktop.platform_labels.iteritems():
        # Fallback to en-US if this plat_os/version isn't available
        # for the current locale
        _locale = locale if plat_os_pretty in platforms else 'en-US'

        # And generate all the info
        download_link = thunderbird_desktop.get_download_url(
            channel, version, plat_os, _locale,
            force_direct=force_direct,
        )

        # If download_link_direct is False the data-direct-link attr
        # will not be output, and the JS won't attempt the IE popup.
        if force_direct:
            # no need to run get_download_url again with the same args
            download_link_direct = False
        else:
            download_link_direct = thunderbird_desktop.get_download_url(
                channel, version, plat_os, _locale,
                force_direct=True,
            )
            if download_link_direct == download_link:
                download_link_direct = False

        builds.append({'os': plat_os,
                       'os_pretty': plat_os_pretty,
                       'download_link': download_link,
                       'download_link_direct': download_link_direct})

    # Get the native name for current locale
    langs = thunderbird_desktop.languages
    locale_name = langs[locale]['native'] if locale in langs else locale

    data = {
        'locale_name': locale_name,
        'version': version,
        'product': 'thunderbird',
        'builds': builds,
        'id': dom_id,
        'channel': alt_channel,
        'alt_copy': alt_copy,
        'button_color': button_color,
    }

    html = render_to_string('thunderbird/includes/download-button.html', data,
                            request=ctx['request'])
    return jinja2.Markup(html)


@library.global_function
def thunderbird_url(page, channel=None):
    """
    Return a product-related URL like /thunderbird/all/ or /thunderbird/beta/notes/.

    Examples
    ========

    In Template
    -----------

        {{ thunderbird_url('all', 'beta') }}
        {{ thunderbird_url('sysreq', channel) }}
    """

    kwargs = {}

    # Tweak the channel name for the naming URL pattern in urls.py
    if channel == 'release':
        channel = None
    if channel == 'alpha':
        channel = 'earlybird'

    if channel:
        kwargs['channel'] = channel

    return reverse('thunderbird.latest.%s' % page, kwargs=kwargs)
