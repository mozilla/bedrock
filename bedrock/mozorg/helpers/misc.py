from __future__ import unicode_literals

from os.path import splitext
import random
import urlparse
from os import path

from django.conf import settings
from django.contrib.staticfiles.finders import find as find_static
from django.template.defaultfilters import slugify as django_slugify

import bleach
import jingo
import jinja2
from bedrock.base.urlresolvers import reverse
from bedrock.base.helpers import static


ALL_FX_PLATFORMS = ('windows', 'linux', 'mac', 'android', 'ios')


def _l10n_media_exists(type, locale, url):
    """ checks if a localized media file exists for the locale """
    return find_static(path.join(type, 'l10n', locale, url)) is not None


def add_string_to_image_url(url, addition):
    """Add the platform string to an image url."""
    filename, ext = splitext(url)
    return ''.join([filename, '-', addition, ext])


def convert_to_high_res(url):
    """Convert a file name to the high-resolution version."""
    return add_string_to_image_url(url, 'high-res')


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


def l10n_img_file_name(ctx, url):
    """Return the filename of the l10n image for use by static()"""
    url = url.lstrip('/')
    locale = getattr(ctx['request'], 'locale', None)
    if not locale:
        locale = settings.LANGUAGE_CODE

    # We use the same localized screenshots for all Spanishes
    if locale.startswith('es') and not _l10n_media_exists('img', locale, url):
        locale = 'es-ES'

    if locale != settings.LANGUAGE_CODE:
        if not _l10n_media_exists('img', locale, url):
            locale = settings.LANGUAGE_CODE

    return path.join('img', 'l10n', locale, url)


@jingo.register.function
@jinja2.contextfunction
def l10n_img(ctx, url):
    """Output the url to a localized image.

    Uses the locale from the current request. Checks to see if the localized
    image exists, and falls back to the image for the default locale if not.

    Examples
    ========

    In Template
    -----------

        {{ l10n_img('firefoxos/screenshot.png') }}

    For en-US this would output:

        {{ static('img/l10n/en-US/firefox/screenshot.png') }}

    For fr this would output:

        {{ static('img/l10n/fr/firefox/screenshot.png') }}

    If that file did not exist it would default to the en-US version (if en-US
    was the default language for this install).

    In the Filesystem
    -----------------

    Put files in folders like the following::

        $ROOT/media/img/l10n/en-US/firefoxos/screenshot.png
        $ROOT/media/img/l10n/fr/firefoxos/screenshot.png

    """
    return static(l10n_img_file_name(ctx, url))


@jingo.register.function
@jinja2.contextfunction
def l10n_css(ctx):
    """
    Output the URL to a locale-specific stylesheet if exists.

    Examples
    ========

    In Template
    -----------

        {{ l10n_css() }}

    For a locale that has locale-specific stylesheet, this would output:

        <link rel="stylesheet" media="screen,projection,tv"
              href="{{ STATIC_URL }}css/l10n/{{ LANG }}/intl.css">

    For a locale that doesn't have any locale-specific stylesheet, this would
    output nothing.

    In the Filesystem
    -----------------

    Put files in folders like the following::

        $ROOT/media/css/l10n/en-US/intl.css
        $ROOT/media/css/l10n/fr/intl.css

    """
    locale = getattr(ctx['request'], 'locale', 'en-US')

    if _l10n_media_exists('css', locale, 'intl.css'):
        markup = ('<link rel="stylesheet" media="screen,projection,tv" href='
                  '"%s">' % static(path.join('css', 'l10n', locale, 'intl.css')))
    else:
        markup = ''

    return jinja2.Markup(markup)


@jingo.register.function
def field_with_attrs(bfield, **kwargs):
    """Allows templates to dynamically add html attributes to bound
    fields from django forms"""
    bfield.field.widget.attrs.update(kwargs)
    return bfield


@jingo.register.function
@jinja2.contextfunction
def platform_img(ctx, url, optional_attributes=None):
    optional_attributes = optional_attributes or {}
    img_urls = {}
    platforms = optional_attributes.pop('platforms', ALL_FX_PLATFORMS)
    add_high_res = optional_attributes.pop('high-res', False)
    is_l10n = optional_attributes.pop('l10n', False)

    for platform in platforms:
        img_urls[platform] = add_string_to_image_url(url, platform)
        if add_high_res:
            img_urls[platform + '-high-res'] = convert_to_high_res(img_urls[platform])

    img_attrs = {}
    for platform, image in img_urls.iteritems():
        if is_l10n:
            image = l10n_img_file_name(ctx, image)
        else:
            image = path.join('img', image)

        if find_static(image):
            key = 'data-src-' + platform
            img_attrs[key] = static(image)

    if add_high_res:
        img_attrs['data-high-res'] = 'true'

    img_attrs.update(optional_attributes)
    attrs = ' '.join('%s="%s"' % (attr, val)
                     for attr, val in img_attrs.iteritems())

    # Don't download any image until the javascript sets it based on
    # data-src so we can do platform detection. If no js, show the
    # windows version.
    markup = ('<img class="platform-img js" src="" data-processed="false" {attrs}>'
              '<noscript><img class="platform-img win" src="{win_src}" {attrs}>'
              '</noscript>').format(attrs=attrs, win_src=img_attrs['data-src-windows'])

    return jinja2.Markup(markup)


@jingo.register.function
@jinja2.contextfunction
def high_res_img(ctx, url, optional_attributes=None):
    url_high_res = convert_to_high_res(url)
    if optional_attributes and optional_attributes.pop('l10n', False) is True:
        url = l10n_img(ctx, url)
        url_high_res = l10n_img(ctx, url_high_res)
    else:
        url = static(path.join('img', url))
        url_high_res = static(path.join('img', url_high_res))

    if optional_attributes:
        class_name = optional_attributes.pop('class', '')
        attrs = ' ' + ' '.join('%s="%s"' % (attr, val)
                               for attr, val in optional_attributes.items())
    else:
        class_name = ''
        attrs = ''

    # Don't download any image until the javascript sets it based on
    # data-src so we can do high-dpi detection. If no js, show the
    # normal-res version.
    markup = ('<img class="js {class_name}" src="" data-processed="false" '
              'data-src="{url}" data-high-res="true" '
              'data-high-res-src="{url_high_res}"{attrs}><noscript>'
              '<img class="{class_name}" src="{url}"{attrs}>'
              '</noscript>').format(url=url, url_high_res=url_high_res,
                                    attrs=attrs, class_name=class_name)

    return jinja2.Markup(markup)


@jingo.register.function
def video(*args, **kwargs):
    """
    HTML5 Video tag helper.

    Accepted kwargs:
    prefix, w, h, autoplay, poster, preload, id

    Use like this:
    {{ video('http://example.com/myvid.mp4', 'http://example.com/myvid.webm',
             poster='http://example.com/myvid.jpg',
             w=640, h=360) }}

    You can also use a prefix like:
    {{ video('myvid.mp4', 'myvid.webm', prefix='http://example.com') }}

    The prefix does not apply to the poster attribute.

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
        videos[ext] = (v if 'prefix' not in kwargs else
                       urlparse.urljoin(kwargs['prefix'], v))

    if not videos:
        return ''

    # defaults
    data = {
        'w': 640,
        'h': 360,
        'autoplay': False,
        'preload': False,
        'id': 'htmlPlayer'
    }

    # Flash fallback, if mp4 file on Mozilla Videos CDN.
    data['flash_fallback'] = False
    if 'mp4' in videos:
        mp4_url = urlparse.urlparse(videos['mp4'])
        if mp4_url.netloc.lower() in ('videos.mozilla.org',
                                      'videos.cdn.mozilla.net'):
            data['flash_fallback'] = mp4_url.path

    data.update(**kwargs)
    data.update(filetypes=filetypes, mime=mime, videos=videos)

    return jinja2.Markup(jingo.env.get_template(
        'mozorg/videotag.html').render(data))


@jingo.register.function
@jinja2.contextfunction
def press_blog_url(ctx):
    """Output a link to the press blog taking locales into account.

    Uses the locale from the current request. Checks to see if we have
    a press blog that match this locale, returns the localized press blog
    url or falls back to the US press blog url if not.

    Examples
    ========

    In Template
    -----------

        {{ press_blog_url() }}

    For en-US this would output:

        https://blog.mozilla.org/press/

    For es-ES this would output:

        https://blog.mozilla.org/press-es/

    For es-MX this would output:

        https://blog.mozilla.org/press-latam/

    """
    locale = getattr(ctx['request'], 'locale', 'en-US')
    if locale not in settings.PRESS_BLOGS:
        locale = 'en-US'

    return settings.PRESS_BLOG_ROOT + settings.PRESS_BLOGS[locale]


@jingo.register.function
@jinja2.contextfunction
def donate_url(ctx, source=''):
    """Output a link to the donation page taking locales into account.

    Uses the locale from the current request. Checks to see if we have
    a donation page that match this locale, returns the localized page
    url or falls back to the US page url if not.

    Examples
    ========

    In Template
    -----------

        {{ donate_url() }}

    For en-US this would output:

        https://sendto.mozilla.org/page/contribute/EOYFR2013-tabzilla

    For de this would output:

        https://sendto.mozilla.org/page/contribute/EOYFR2013-webDE

    For fr this would output:

        https://sendto.mozilla.org/page/contribute/EOYFR2013-webFR

    For pt-BR this would output:

        https://sendto.mozilla.org/page/contribute/EOYFR2013-webPTBR

    """
    locale = getattr(ctx['request'], 'locale', 'en-US')
    if locale not in settings.DONATE_LOCALE_LINK:
        if 'default' in settings.DONATE_LOCALE_LINK:
            locale = 'default'
        else:
            locale = 'en-US'

        # The source of the new donation URL is different from the old one,
        # so replace it if needed (Bug 1100548)
        source = source.replace('mozillaorg', 'mozillaorg_default')

    return settings.DONATE_LOCALE_LINK[locale].format(source=source)


@jingo.register.function
@jinja2.contextfunction
def firefox_twitter_url(ctx):
    """Output a link to Twitter taking locales into account.

    Uses the locale from the current request. Checks to see if we have
    a Twitter account that match this locale, returns the localized account
    url or falls back to the US account url if not.

    Examples
    ========

    In Template
    -----------

        {{ firefox_twitter_url() }}

    For en-US this would output:

        https://twitter.com/firefox

    For es-ES this would output:

        https://twitter.com/firefox_es

    For pt-BR this would output:

        https://twitter.com/firefoxbrasil

    """
    locale = getattr(ctx['request'], 'locale', 'en-US')
    if locale not in settings.FIREFOX_TWITTER_ACCOUNTS:
        locale = 'en-US'

    return settings.FIREFOX_TWITTER_ACCOUNTS[locale]


@jingo.register.filter
def absolute_url(url):
    """
    Return a fully qualified URL including a protocol especially for the Open
    Graph Protocol image object.

    Examples
    ========

    In Template
    -----------
    This filter can be used in combination with the static helper like this:

        {{ static('path/to/img')|absolute_url }}

    With a block:

        {% filter absolute_url %}
          {% block page_image %}{{ static('path/to/img') }}{% endblock %}
        {% endfilter %}
    """

    if url.startswith('//'):
        prefix = 'https:'
    elif url.startswith('/'):
        prefix = settings.CANONICAL_URL
    else:
        prefix = ''

    return prefix + url


@jingo.register.function
def releasenotes_url(release):
    prefix = 'aurora' if release.channel == 'Aurora' else 'release'
    if release.product == 'Firefox for Android':
        return reverse('firefox.android.releasenotes', args=(release.version, prefix))
    if release.product == 'Firefox for iOS':
        return reverse('firefox.ios.releasenotes', args=(release.version, prefix))
    else:
        return reverse('firefox.desktop.releasenotes', args=(release.version, prefix))


@jingo.register.filter
def htmlattr(_list, **kwargs):
    """
    Assign an attribute to elements, like jQuery's attr function. The _list
    argument is a BeautifulSoup iterable object. Note that such a code doesn't
    work in a Jinja2 template:

        {% set body.p['id'] = 'great' %}
        {% set body.p['class'] = 'awesome' %}

    Instead, use this htmlattr function like

        {{ body.p|htmlattr(id='great', class='awesome') }}

    """
    for tag in _list:
        for attr, value in kwargs.iteritems():
            tag[attr] = value

    return _list


@jingo.register.filter
def shuffle(_list):
    """Return a shuffled list"""
    random.shuffle(_list)
    return _list


@jingo.register.filter
def slugify(text):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    return django_slugify(text)


@jingo.register.filter
def bleach_tags(text):
    return bleach.clean(text, tags=[], strip=True).replace('&amp;', '&')
