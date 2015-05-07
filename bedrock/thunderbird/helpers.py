import jingo

from bedrock.base.urlresolvers import reverse


@jingo.register.function
def thunderbird_url(platform, page, channel=None):
    """
    Return a product-related URL like /thunderbird/all/ or /thunderbird/beta/notes/.

    Examples
    ========

    In Template
    -----------

        {{ thunderbird_url('desktop', 'all', 'beta') }}
        {{ thunderbird_url('desktop', 'sysreq', channel) }}
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
