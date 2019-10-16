.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _coding:

=====================
Developing on Bedrock
=====================

Writing URL Patterns
--------------------

URL patterns should be as strict as possible. It should begin with a
`^` and end with `/$` to make sure it only matches what you specifiy.
It also forces a trailing slash. You should also give the URL a name
so that other pages can reference it instead of hardcoding the URL.
Example:

.. code-block:: python

    url(r'^channel/$', channel, name='mozorg.channel')

Bedrock comes with a handy shortcut to automate all of this:

.. code-block:: python

    from bedrock.mozorg.util import page
    page('channel', 'mozorg/channel.html')

You don't even need to create a view. It will serve up the specified
template at the given URL (the first parameter). You can also pass
template data as keyword arguments:

.. code-block:: python

    page('channel', 'mozorg/channel.html',
         latest_version=product_details.firefox_versions['LATEST_FIREFOX_VERSION'])

The variable `latest_version` will be available in the template.

Optimizing images
-----------------

Images can take a long time to load and eat up a lot of bandwidth. Always take care
to optimize images before uploading them to the site.

The script `img.sh` can be used to optimize images locally on the command line:

# Before you run it for the first time you will need to run `yarn` to install dependencies
# Add the image files to git's staging area `git add *`
# Run the script `./bin/img.sh`
# The optimized files will not automatically be staged, so be sure to add them before commiting

The script will:

- optimize JPG and PNG files using `tinypng <https://tinypng.com/>`_ (
    - this step is optional since running compression on the same images over and over degrades them)
    - you will be prompted to add a `TinyPNG API key <https://tinypng.com/developers>`_
- optimize SVG images locally with svgo
- check that SVGs have a viewbox (needed for IE support)
- check that images that end in `-high-res` have low res versions as well

Embedding images
----------------

Images should be included on pages using helper functions.

static()
^^^^^^^^
For a simple image, the `static()` function is used to generate the image URL. For example:

.. code-block:: html

    <img src="{{ static('img/firefox/new/firefox-logo.png') }}" alt="Firefox" />

will output an image:

.. code-block:: html

    <img src="/media/img/firefox/new/firefox-logo.png" alt="Firefox">

high_res_img()
^^^^^^^^^^^^^^
For images that include a high-resolution alternative for displays with a high pixel density, use the `high_res_img()` function:

.. code-block:: python

    high_res_img('img/firefox/new/firefox-logo.png', {'alt': 'Firefox', 'width': '200', 'height': '100'})

The `high_res_img()` function will automatically look for the image in the URL parameter suffixed with `'-high-res'`, e.g. `img/firefox/new/firefox-logo-high-res.png` and switch to it if the display has high pixel density.

`high_res_img()` supports localized images by setting the `'l10n'` parameter to `True`:

.. code-block:: python

    high_res_img('img/firefox/new/firefox-logo.png', {'l10n': True, 'alt': 'Firefox', 'width': '200', 'height': '100'})

When using localization, `high_res_img()` will look for images in the appropriate locale folder. In the above example, for the `de` locale, both standard and high-res versions of the image should be located at `media/img/l10n/de/firefox/new/`.

l10n_img()
^^^^^^^^^^
Images that have translatable text can be handled with `l10n_img()`:

.. code-block:: html

    <img src="{{ l10n_img('firefox/os/have-it-all/messages.jpg') }}" />

The images referenced by `l10n_img()` must exist in `media/img/l10n/`, so for above example, the images could include `media/img/l10n/en-US/firefox/os/have-it-all/messages.jpg` and `media/img/l10n/es-ES/firefox/os/have-it-all/messages.jpg`.

platform_img()
^^^^^^^^^^^^^^
Finally, for outputting an image that differs depending on the platform being used, the `platform_img()` function will automatically display the image for the user's browser:

.. code-block:: python

    platform_img('img/firefox/new/browser.png', {'alt': 'Firefox screenshot'})

`platform_img()` will automatically look for the images `browser-mac.png`, `browser-win.png`, `browser-linux.png`, etc. Platform image also supports hi-res images by adding `'high-res': True` to the list of optional attributes.

`platform_img()` supports localized images by setting the `'l10n'` parameter to `True`:

.. code-block:: python

    platform_img('img/firefox/new/firefox-logo.png', {'l10n': True, 'alt': 'Firefox screenshot'})

When using localization, `platform_img()` will look for images in the appropriate locale folder. In the above example, for the `es-ES` locale, all platform versions of the image should be located at `media/img/l10n/es-ES/firefox/new/`.

Writing Views
-------------

You should rarely need to write a view for mozilla.org. Most pages are
static and you should use the `page` function documented above.

If you need to write a view and the page is translated or translatable
then it should use the `l10n_utils.render()` function to render the
template.

.. code-block:: python

    from lib import l10n_utils

    def my_view(request):
        # do your fancy things
        ctx = {'template_variable': 'awesome data'}
        return l10n_utils.render(request, 'app/template.html', ctx)

Make sure to namespace your templates by putting them in a directory
named after your app, so instead of templates/template.html they would
be in templates/blog/template.html if `blog` was the name of your app.


If you prefer to use Django's Generic View classes we have a convenient
helper for that. You can use it either to create a custom view class of
your own, or use it directly in a `urls.py` file.

.. code-block:: python

    # app/views.py
    from lib.l10n_utils import L10nTemplateView

    class FirefoxRoxView(L10nTemplateView):
        template_name = 'app/firefox-rox.html'

    # app/urls.py
    urlpatterns = [
        # from views.py
        path('firefox/rox/', FirefoxRoxView.as_view()),
        # directly
        path('firefox/sox/', L10nTemplateView.as_view(template_name='app/firefox-sox.html')),
    ]

The `L10nTemplateView` functionality is mostly in a template mixin called `LangFilesMixin` which
you can use with other generic Django view classes if you need one other than `TemplateView`.

Variation Views
^^^^^^^^^^^^^^^

We have a generic view that allows you to easily create and use a/b testing
templates. If you'd like to have either separate templates or just a template
context variable for switching, this will help you out. For example.

.. code-block:: python

    # urls.py

    from django.conf.urls import url

    from bedrock.utils.views import VariationTemplateView

    urlpatterns = [
        url(r'^testing/$',
            VariationTemplateView.as_view(template_name='testing.html',
                                          template_context_variations=['a', 'b']),
            name='testing'),
    ]

This will give you a context variable called `variation` that will either be an empty
string if no param is set, or `a` if `?v=a` is in the URL, or `b` if `?v=b` is in the
URL. No other options will be valid for the `v` query parameter and `variation` will
be empty if any other value is passed in for `v` via the URL. So in your template code
you'd simply do the following:

.. code-block:: jinja

    {% if variation == 'b' %}<p>This is the B variation of our test. Enjoy!</p>{% endif %}

If you'd rather have a fully separate template for your test, you can use the
`template_name_variations` argument to the view instead of `template_context_variations`.

.. code-block:: python

    # urls.py

    from django.conf.urls import url

    from bedrock.utils.views import VariationTemplateView

    urlpatterns = [
        url(r'^testing/$',
            VariationTemplateView.as_view(template_name='testing.html',
                                          template_name_variations=['1', '2']),
            name='testing'),
    ]

This will not provide any extra template context variables, but will instead look for
alternate template names. If the URL is `testing/?v=1`, it will use a template named
`testing-1.html`, if `v=2` it will use `testing-2.html`, and for everything else it will
use the default. It simply puts a dash and the variation value between the template
file name and file extension.

It is theoretically possible to use the template name and template context versions
of this view together, but that would be an odd situation and potentially inappropriate
for this utility.

You can also limit your variations to certain locales. By default the variations will work
for any localization of the page, but if you supply a list of locales to the `variation_locales`
argument to the view then it will only set the variation context variable or alter the template
name (depending on the options explained above) when requested at one of said locales. For example,
the template name example above could be modified to only work for English or German like so

.. code-block:: python

    # urls.py

    from django.conf.urls import url

    from bedrock.utils.views import VariationTemplateView

    urlpatterns = [
        url(r'^testing/$',
            VariationTemplateView.as_view(template_name='testing.html',
                                          template_name_variations=['1', '2'],
                                          variation_locales=['en-US', 'de']),
            name='testing'),
    ]

Any request to the page in for example French would not use the alternate template even if a
valid variation were given in the URL.

.. note::

    If you'd like to add this functionality to an existing Class-Based View, there is
    a mixin that implements this pattern that should work with most views:
    `bedrock.utils.views.VariationMixin`.


Geo Redirect View
^^^^^^^^^^^^^^^^^

We sometimes need to have a special page variation for people visiting from certain
countries. To make this easier we have a redirect view class that will allow you to
define URLs per country as well as a default for everyone else. This redirector URL
must only be a redirector since it must be uncachable by our CDN so that all visitors
will hit the server and see the correct page for their location.

.. code-block:: python

    from bedrock.base.views import GeoRedirectView

    class CanadaIsSpecialView(GeoRedirectView):
        geo_urls = {
            'CA': 'app.canada-is-special',
        }
        default_url = 'app.everyone-else'

In this example people in Canada would go to the URL that Django returns using `reverse()`
(i.e. the name of the URL) and everyone else would go to the `app.everyone-else` URL. You
may also use full URLs instead of URL names if you want to. It will look for strings that
start with "http(s)://" and use it as is. The
`country code <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements>`_
must be 2 characters and upper case. If the patterns for the redirect and the destination(s) have
URL parameters they will be passed to the reverse call for the URL pattern name. So for example
if you're doing this for a Firefox page with a version number in the URL, as long as the view
and destination URLs use the same URL parameter names it will be preserved in the resulting destination URL.
So `/firefox/70.0beta/whatsnew/` would redirect to `/firefox/70.0beta/whatsnew/canada/` for example.
The redirector will also preserve query parameters by default. You can turn that off by
setting the `query_string = False` class variable.

Coding Style Guides
-------------------

* `Mozilla Python Style Guide <http://mozweb.readthedocs.org/en/latest/reference/python-style.html>`_
* `Mozilla HTML Style Guide <http://mozweb.readthedocs.org/en/latest/reference/html-style.html>`_
* `Mozilla JS Style Guide <http://mozweb.readthedocs.org/en/latest/reference/js-style.html>`_
* `Mozilla CSS Style Guide <http://mozweb.readthedocs.org/en/latest/reference/css-style.html>`_

Use the ``.open-sans``, ``.open-sans-light`` and ``.open-sans-extrabold`` mixins
to specify font families to allow using international fonts. See the :ref:
`CSS<l10n>` section in the l10n doc for details.

Use the ``.font-size()`` mixin to generate root-relative font sizes. You can
declare a font size in pixels and the mixin will convert it to an equivalent
``rem`` (root em) unit while also including the pixel value as a fallback for
older browsers that don't support ``rem``. This is preferable to declaring font
sizes in either fixed units (``px``, ``pt``, etc) or element-relative units (``em``, ``%``).
See `this post by Jonathan Snook <http://snook.ca/archives/html_and_css/font-size-with-rem>`_
for more info.

When including CSS blocks, use ``{% block page_css %}`` for page specific inclusion of CSS.
``{% block site_css %}`` should only be touched in rare cases where base styles need to be overwritten.

Configuring your code editor
----------------------------

Bedrock includes an `.editorconfig` file in the root directory that you can
use with your code editor to help maintain consistent coding styles. Please
see `editorconfig.org <http://editorconfig.org/>`_. for a list of supported
editors and available plugins.
