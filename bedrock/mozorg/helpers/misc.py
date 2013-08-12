import urlparse
from os import path

from django.conf import settings

import jingo
import jinja2
from funfactory.settings_base import path as base_path
from funfactory.urlresolvers import reverse


L10N_IMG_PATH = base_path('media', 'img', 'l10n')


@jingo.register.function
@jinja2.contextfunction
def php_url(ctx, url):
    """Process a URL on the PHP site and prefix the locale to it."""
    locale = getattr(ctx['request'], 'locale', None)

    # Do this only if we have a locale and the URL is absolute
    if locale and url[0] == '/':
        return path.join('/', locale, url.lstrip('/'))
    return url


@jingo.register.function
def url(viewname, *args, **kwargs):
    """Helper for Django's ``reverse`` in templates."""
    url = reverse(viewname, args=args, kwargs=kwargs)
    # If this instance is a mix of Python and PHP, it can be set to
    # force the /b/ URL so that linking across pages work
    # TURNED OFF FOR NOW. The dev site seems to be doing this already
    # somehow. Looking into it. Issue #22
    if getattr(settings, 'FORCE_SLASH_B', False) and False:
        return path.join('/b/', url.lstrip('/'))
    return url


@jingo.register.function
@jinja2.contextfunction
def secure_url(ctx, viewname=None):
    """Retrieve a full secure URL especially for form submissions"""
    _path = url(viewname) if viewname else None
    _url = ctx['request'].build_absolute_uri(_path)

    # only force https if current page was requested via SSL
    # otherwise, CSRF/AJAX errors will occur (submitting to https from http)
    if ctx['request'].is_secure():
        return _url.replace('http://', 'https://')
    return _url


@jingo.register.function
def media(url):
    return path.join(settings.MEDIA_URL, url.lstrip('/'))


@jingo.register.function
@jinja2.contextfunction
def img_l10n(ctx, url):
    """Output the url to a localized image.

    Uses the locale from the current request. Checks to see if the localized
    image exists, and falls back to the image for the default locale if not.

    Examples
    ========

    In Template
    -----------

        {{ img_l10n('firefoxos/screenshot.png') }}

    For en-US this would output:

        {{ MEDIA_URL }}img/l10n/en-US/firefox/screenshot.png

    For fr this would output:

        {{ MEDIA_URL }}img/l10n/fr/firefox/screenshot.png

    If that file did not exist it would default to the en-US version (if en-US
    was the default language for this install).

    In the Filesystem
    -----------------

    Put files in folders like the following::

        $ROOT/media/img/l10n/en-US/firefoxos/screenshot.png
        $ROOT/media/img/l10n/fr/firefoxos/screenshot.png

    """
    url = url.lstrip('/')
    locale = getattr(ctx['request'], 'locale', None)
    if not locale:
        locale = settings.LANGUAGE_CODE

    if locale != settings.LANGUAGE_CODE:
        if not path.exists(path.join(L10N_IMG_PATH, locale, url)):
            locale = settings.LANGUAGE_CODE

    return path.join(settings.MEDIA_URL, 'img', 'l10n', locale, url)


@jingo.register.function
def field_with_attrs(bfield, **kwargs):
    """Allows templates to dynamically add html attributes to bound
    fields from django forms"""
    bfield.field.widget.attrs.update(kwargs)
    return bfield


@jingo.register.function
def platform_img(url, optional_attributes = {}, prepend_media_url = True):
    attrs = ' '.join(('%s="%s"' % (attr, val)
                      for attr, val in optional_attributes.items()))

    if prepend_media_url:
        url = path.join(settings.MEDIA_URL, url.lstrip('/'))

    # Don't download any image until the javascript sets it based on
    # data-src so we can to platform detection. If no js, show the
    # windows version.
    markup = ('<img class="platform-img js" src="" data-src="%s" %s>'
              '<noscript><img class="platform-img win" src="%s" %s></noscript>'
              % (url, attrs, url, attrs))

    return jinja2.Markup(markup)


@jingo.register.function
def video(*args, **kwargs):
    """
    HTML5 Video tag helper.

    Accepted kwargs:
    prefix, w, h, autoplay

    Use like this:
    {{ video('http://example.com/myvid.mp4', http://example.com/myvid.webm',
             w=640, h=360) }}

    You can also use a prefix like:
    {{ video('myvid.mp4', 'myvid.webm', prefix='http://example.com') }}

    Finally, MIME type detection happens by file extension. Supported: webm,
    mp4, ogv. If you want anything else, patches welcome.
    """

    filetypes = ('webm', 'ogv', 'mp4')
    mime = {'webm': 'video/webm',
            'ogv': 'video/ogg; codecs="theora, vorbis"',
            'mp4': 'video/mp4'}

    videos = {}
    for v in args:
        try:
            ext = v.rsplit('.', 1)[1].lower()
        except IndexError:
            # TODO: Perhaps we don't want to swallow this quietly in the future
            continue
        if ext not in filetypes:
            continue
        videos[ext] = (v if not 'prefix' in kwargs else
                       urlparse.urljoin(kwargs['prefix'], v))

    if not videos:
        return ''

    # defaults
    data = {
        'w': 640,
        'h': 360,
        'autoplay': False,
    }

    # Flash fallback, if mp4 file on Mozilla Videos CDN.
    data['flash_fallback'] = False
    if 'mp4' in videos:
        mp4_url = urlparse.urlparse(videos['mp4'])
        if mp4_url.netloc.lower() in ('videos.mozilla.org',
                                      'videos-cdn.mozilla.net'):
            data['flash_fallback'] = mp4_url.path

    data.update(**kwargs)
    data.update(filetypes=filetypes, mime=mime, videos=videos)

    return jinja2.Markup(jingo.env.get_template(
        'mozorg/videotag.html').render(data))
