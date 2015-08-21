# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jingo
import jinja2

from bedrock.thunderbird.details import thunderbird_desktop
from bedrock.base.urlresolvers import reverse
from lib.l10n_utils import get_locale


@jingo.register.function
@jinja2.contextfunction
def download_thunderbird(ctx, channel='release', small=False,
                         dom_id=None, locale=None, simple=False,
                         force_direct=False):
    """ Output a "Download Thunderbird" button.

    :param ctx: context from calling template.
    :param channel: name of channel: 'release', 'beta' or 'alpha'.
    :param small: Display the small button if True.
    :param dom_id: Use this string as the id attr on the element.
    :param locale: The locale of the download. Default to locale of request.
    :param simple: Display button with text only if True. Will not display
            icon or privacy/what's new/systems & languages links. Can be used
            in conjunction with 'small'. Those links can still be displayed by
            overriding CSS.
    :param force_direct: Force the download URL to be direct.
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
        'small': small,
        'simple': simple,
        'channel': alt_channel,
    }

    html = jingo.render_to_string(ctx['request'],
                                  'thunderbird/includes/download-button.html',
                                  data)
    return jinja2.Markup(html)


@jingo.register.function
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

    return reverse('thunderbird.%s' % page, kwargs=kwargs)
