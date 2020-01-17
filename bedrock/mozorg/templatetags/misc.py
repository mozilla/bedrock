# coding: utf-8

import random
import re
from os import path
from os.path import splitext
import urllib.parse

from django.conf import settings
from django.contrib.staticfiles.finders import find as find_static
from django.template.defaultfilters import slugify as django_slugify
from django.template.defaulttags import CsrfTokenNode
from django.template.loader import render_to_string
from django.utils import six
from django.utils.http import urlquote
from django.utils.translation import ugettext as _
try:
    from django.utils.encoding import smart_unicode as smart_text
except ImportError:
    from django.utils.encoding import smart_text

import bleach
import jinja2
from django_jinja import library

from bedrock.base.templatetags.helpers import static
from bedrock.firefox.firefox_details import firefox_ios


ALL_FX_PLATFORMS = ('windows', 'linux', 'mac', 'android', 'ios')


def _strip_img_prefix(url):
    return re.sub(r'^/?img/', '', url)


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


@library.global_function
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
    url = _strip_img_prefix(url)
    return static(l10n_img_file_name(ctx, url))


@library.global_function
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


@library.global_function
def field_with_attrs(bfield, **kwargs):
    """Allows templates to dynamically add html attributes to bound
    fields from django forms"""
    bfield.field.widget.attrs.update(kwargs)
    return bfield


@library.global_function
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
    for platform, image in img_urls.items():
        if is_l10n:
            image = l10n_img_file_name(ctx, _strip_img_prefix(image))

        if find_static(image):
            key = 'data-src-' + platform
            img_attrs[key] = static(image)

    if add_high_res:
        img_attrs['data-high-res'] = 'true'

    img_attrs.update(optional_attributes)
    attrs = ' '.join('%s="%s"' % (attr, val)
                     for attr, val in img_attrs.items())

    # Don't download any image until the javascript sets it based on
    # data-src so we can do platform detection. If no js, show the
    # windows version.
    markup = ('<img class="platform-img js" src="" data-processed="false" {attrs}>'
              '<noscript><img class="platform-img win" src="{win_src}" {attrs}>'
              '</noscript>').format(attrs=attrs, win_src=img_attrs['data-src-windows'])

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def high_res_img(ctx, url, optional_attributes=None):
    if optional_attributes and optional_attributes.pop('l10n', False) is True:
        url = _strip_img_prefix(url)
        url_high_res = convert_to_high_res(url)
        url = l10n_img(ctx, url)
        url_high_res = l10n_img(ctx, url_high_res)
    else:
        url_high_res = convert_to_high_res(url)
        url = static(url)
        url_high_res = static(url_high_res)

    if optional_attributes:
        class_name = optional_attributes.pop('class', '')
        attrs = ' ' + ' '.join('%s="%s"' % (attr, val)
                               for attr, val in optional_attributes.items())
    else:
        class_name = ''
        attrs = ''

    # Use native srcset attribute for high res images
    markup = ('<img class="{class_name}" src="{url}" '
              'srcset="{url_high_res} 1.5x"'
              '{attrs}>').format(url=url, url_high_res=url_high_res,
                                 attrs=attrs, class_name=class_name)

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def lazy_img(ctx, image_url, placeholder_url, include_highres_image=False,
             optional_attributes=None, highres_image_url=None):
    placeholder = static(placeholder_url)

    external_img = re.match(r'^https?://', image_url, flags=re.I)

    if include_highres_image and not external_img:
        image_high_res = static(convert_to_high_res(image_url))
        srcset = f'data-srcset="{image_high_res} 2x"'
    else:
        srcset = ''

    # image could be external
    if not external_img:
        image_url = static(image_url)

    if highres_image_url:
        srcset = f'data-srcset="{highres_image_url} 2x"'

    if optional_attributes:
        class_name = optional_attributes.pop('class', 'lazy-image')
        alt_text = optional_attributes.pop('alt', '')
        attrs = ' '.join('%s="%s"' % (attr, val)
                         for attr, val in optional_attributes.items())
    else:
        class_name = 'lazy-image'
        alt_text = ''
        attrs = ''

    markup = (f'<div class="lazy-image-container">'
              f'<img class="{class_name}" src="{placeholder}" data-src="{image_url}" {srcset} alt="{alt_text}" {attrs}>'
              f'<noscript>'
              f'<img class="{class_name}" src="{image_url}" {srcset} alt="{alt_text}" {attrs}>'
              f'</noscript>'
              f'</div>')

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def video(ctx, *args, **kwargs):
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
                       urllib.parse.urljoin(kwargs['prefix'], v))

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

    data.update(**kwargs)
    data.update(filetypes=filetypes, mime=mime, videos=videos)

    return jinja2.Markup(render_to_string('mozorg/videotag.html', data, request=ctx['request']))


@library.global_function
@jinja2.contextfunction
def press_blog_url(ctx):
    """Output a link to the press blog taking locales into account.

    Uses the locale from the current request. Checks to see if we have
    a press blog that matches this locale, returns the localized press blog
    url or falls back to the US press blog url if not.

    Examples
    ========

    In Template
    -----------

        {{ press_blog_url() }}

    For en-US this would output:

        https://blog.mozilla.org/press/

    For en-GB this would output:

        https://blog.mozilla.org/press-uk/

    For de this would output:

        https://blog.mozilla.org/press-de/

    """
    locale = getattr(ctx['request'], 'locale', 'en-US')
    if locale not in settings.PRESS_BLOGS:
        locale = 'en-US'

    return settings.PRESS_BLOG_ROOT + settings.PRESS_BLOGS[locale]


@library.global_function
@jinja2.contextfunction
def donate_url(ctx, source=''):
    """Output a donation link to the donation page formatted using settings.DONATE_PARAMS

    Examples
    ========

    In Template
    -----------

        {{ donate_url() }}

    For en-US this would output:

        https://donate.mozilla.org/en-US/?presets=100,50,25,15&amount=50&utm_source=mozilla.org&utm_medium=referral&utm_content=footer&currency=usd

    For de this would output:

        https://donate.mozilla.org/de/?presets=100,50,25,15&amount=50&utm_source=mozilla.org&utm_medium=referral&utm_content=footer&currency=eur

    For a locale not defined in settings.DONATE this would output:

        https://donate.mozilla.org/ca/?presets=100,50,25,15&amount=50&utm_source=mozilla.org&utm_medium=referral&utm_content=footer&currency=usd

    """
    locale = getattr(ctx['request'], 'locale', 'en-US')

    donate_url_params = settings.DONATE_PARAMS.get(
        locale, settings.DONATE_PARAMS['en-US'])

    return settings.DONATE_LINK.format(
        locale=locale, presets=donate_url_params['presets'],
        default=donate_url_params['default'], source=source,
        currency=donate_url_params['currency'])


@library.global_function
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


@library.filter
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


@library.global_function
@jinja2.contextfunction
def firefox_ios_url(ctx, ct_param=None):
    """
    Output a link to the Firefox for iOS download page on the Apple App Store
    taking locales into account.

    Use the locale from the current request. Check if the locale matches one of
    the Store's supported countries, return the localized page's URL or fall
    back to the default (English) page if not.

    The optional ct_param is a campaign value for the app analytics.

    Examples
    ========

    In Template
    -----------

        {{ firefox_ios_url() }}

    For en-US this would output:

        https://itunes.apple.com/us/app/firefox-private-safe-browser/id989804926

    For es-ES this would output:

        https://itunes.apple.com/es/app/firefox-private-safe-browser/id989804926

    For ja this would output:

        https://itunes.apple.com/jp/app/firefox-private-safe-browser/id989804926

    """
    locale = getattr(ctx['request'], 'locale', 'en-US')
    link = firefox_ios.get_download_url('release', locale)

    if ct_param:
        return link + '?ct=' + ct_param

    return link


@library.filter
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
        for attr, value in kwargs.items():
            tag[attr] = value

    return _list


@library.filter
def shuffle(_list):
    """Return a shuffled list"""
    random.shuffle(_list)
    return _list


@library.filter
def slugify(text):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    return django_slugify(text)


@library.filter
def bleach_tags(text):
    return bleach.clean(text, tags=[], strip=True).replace('&amp;', '&')


# from jingo


@library.global_function
@jinja2.contextfunction
def csrf(context):
    """Equivalent of Django's ``{% crsf_token %}``."""
    return jinja2.Markup(CsrfTokenNode().render(context))


@library.filter
def f(s, *args, **kwargs):
    """
    Uses ``str.format`` for string interpolation.

    **Note**: Always converts to s to text type before interpolation.

    >>> {{ "{0} arguments and {x} arguments"|f('positional', x='keyword') }}
    "positional arguments and keyword arguments"
    """
    s = six.text_type(s)
    return s.format(*args, **kwargs)


@library.filter
def datetime(t, fmt=None):
    """Call ``datetime.strftime`` with the given format string."""
    if fmt is None:
        fmt = _(u'%B %e, %Y')
    if not six.PY3:
        # The datetime.strftime function strictly does not
        # support Unicode in Python 2 but is Unicode only in 3.x.
        fmt = fmt.encode('utf-8')
    return smart_text(t.strftime(fmt)) if t else ''


@library.filter
def ifeq(a, b, text):
    """Return ``text`` if ``a == b``."""
    return jinja2.Markup(text if a == b else '')


def _get_adjust_link(adjust_url, app_store_url, google_play_url, redirect, locale, adgroup, creative=None):
    link = adjust_url
    params = 'campaign=www.mozilla.org&adgroup=' + adgroup
    redirect_url = None

    # Get the appropriate app store URL to use as a fallback redirect.
    if redirect == 'ios':
        countries = settings.APPLE_APPSTORE_COUNTRY_MAP
        if locale in countries:
            redirect_url = app_store_url.format(country=countries[locale])
        else:
            redirect_url = app_store_url.replace('/{country}/', '/')
    elif redirect == 'android':
        redirect_url = google_play_url

    # Optional creative parameter.
    if creative:
        params += '&creative=' + creative

    if redirect_url:
        link += '?redirect=' + urlquote(redirect_url, safe='') + '&' + params
    else:
        link += '?' + params

    return link


@library.global_function
@jinja2.contextfunction
def firefox_adjust_url(ctx, redirect, adgroup, creative=None):
    """
    Return an adjust.com link for Firefox on mobile.

    Examples
    ========

    In Template
    -----------

        {{ firefox_adjust_url('ios', 'accounts-page') }}
    """
    adjust_url = settings.ADJUST_FIREFOX_URL
    app_store_url = settings.APPLE_APPSTORE_FIREFOX_LINK
    play_store_url = settings.GOOGLE_PLAY_FIREFOX_LINK
    locale = getattr(ctx['request'], 'locale', 'en-US')

    return _get_adjust_link(adjust_url, app_store_url, play_store_url, redirect, locale, adgroup, creative)


@library.global_function
@jinja2.contextfunction
def focus_adjust_url(ctx, redirect, adgroup, creative=None):
    """
    Return an adjust.com link for Focus/Klar on mobile.

    Examples
    ========

    In Template
    -----------

        {{ focus_adjust_url('ios', 'fights-for-you-page') }}
    """
    klar_locales = ['de']
    adjust_url = settings.ADJUST_FOCUS_URL
    app_store_url = settings.APPLE_APPSTORE_FOCUS_LINK
    play_store_url = settings.GOOGLE_PLAY_FOCUS_LINK
    locale = getattr(ctx['request'], 'locale', 'en-US')

    if locale in klar_locales:
        adjust_url = settings.ADJUST_KLAR_URL
        app_store_url = settings.APPLE_APPSTORE_KLAR_LINK
        play_store_url = settings.GOOGLE_PLAY_KLAR_LINK

    return _get_adjust_link(adjust_url, app_store_url, play_store_url, redirect, locale, adgroup, creative)


@library.global_function
@jinja2.contextfunction
def pocket_adjust_url(ctx, redirect, adgroup, creative=None):
    """
    Return an adjust.com link for Pocket on mobile.

    Examples
    ========

    In Template
    -----------

        {{ pocket_adjust_url('ios', 'accounts-page') }}
    """
    adjust_url = settings.ADJUST_POCKET_URL
    app_store_url = settings.APPLE_APPSTORE_POCKET_LINK
    play_store_url = settings.GOOGLE_PLAY_POCKET_LINK
    locale = getattr(ctx['request'], 'locale', 'en-US')

    return _get_adjust_link(adjust_url, app_store_url, play_store_url, redirect, locale, adgroup, creative)


@library.global_function
@jinja2.contextfunction
def lockwise_adjust_url(ctx, redirect, adgroup, creative=None):
    """
    Return an adjust.com link for Lockwise on mobile.

    Examples
    ========

    In Template
    -----------

        {{ lockwise_adjust_url('ios', 'accounts-page') }}
    """
    adjust_url = settings.ADJUST_LOCKWISE_URL
    app_store_url = settings.APPLE_APPSTORE_LOCKWISE_LINK
    play_store_url = settings.GOOGLE_PLAY_LOCKWISE_LINK
    locale = getattr(ctx['request'], 'locale', 'en-US')

    return _get_adjust_link(adjust_url, app_store_url, play_store_url, redirect, locale, adgroup, creative)


def _fxa_product_button(product_url, entrypoint, button_text, class_name=None, is_button_class=True,
                        optional_parameters=None, optional_attributes=None):
    href = f'{product_url}?entrypoint={entrypoint}&form_type=button&utm_source={entrypoint}&utm_medium=refferal'
    css_class = 'js-fxa-cta-link js-fxa-product-button'
    attrs = ''

    if optional_parameters:
        params = '&'.join('%s=%s' % (param, val) for param, val in optional_parameters.items())
        href += f'&{params}'

    if optional_attributes:
        attrs += ' '.join('%s="%s"' % (attr, val) for attr, val in optional_attributes.items())

    if is_button_class:
        css_class += ' mzp-c-button mzp-t-product'

    if class_name:
        css_class += f' {class_name}'

    markup = (f'<a href="{href}" data-action="{settings.FXA_ENDPOINT}" class="{css_class}" {attrs}>'
              f'{button_text}'
              f'</a>')

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def pocket_fxa_button(ctx, entrypoint, button_text, class_name=None, is_button_class=True, optional_parameters=None, optional_attributes=None):
    """
    Render a getpocket.com link with required params for FxA authentication.

    Examples
    ========

    In Template
    -----------

        {{ pocket_fxa_button(entrypoint='mozilla.org-firefox-pocket', button_text='Try Pocket Now') }}
    """
    product_url = 'https://getpocket.com/ff_signup'
    return _fxa_product_button(product_url, entrypoint, button_text, class_name, is_button_class, optional_parameters, optional_attributes)


@library.global_function
@jinja2.contextfunction
def monitor_fxa_button(ctx, entrypoint, button_text, class_name=None, is_button_class=True, optional_parameters=None, optional_attributes=None):
    """
    Render a monitor.firefox.com link with required params for FxA authentication.

    Examples
    ========

    In Template
    -----------

        {{ monitor_fxa_button(entrypoint='mozilla.org-firefox-accounts', button_text='Sign In to Monitor') }}
    """
    product_url = 'https://monitor.firefox.com/oauth/init'
    return _fxa_product_button(product_url, entrypoint, button_text, class_name, is_button_class, optional_parameters, optional_attributes)
