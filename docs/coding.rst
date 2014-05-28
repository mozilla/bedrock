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
Example::

    url(r'^channel/$', channel, name='mozorg.channel')

Bedrock comes with a handy shortcut to automate all of this::

    from bedrock.mozorg.util import page
    page('channel', 'mozorg/channel.html')

You don't even need to create a view. It will serve up the specified
template at the given URL (the first parameter). You can also pass
template data as keyword arguments:

    page('channel', 'mozorg/channel.html',
         latest_version=product_details.firefox_versions['LATEST_FIREFOX_VERSION'])

The variable `latest_version` will be available in the template.

Embedding images
----------------

Images should be included on pages using helper functions.

media()
^^^^^^^
For a simple image, the `media()` function is used to generate the image URL. For example::

    <img src="{{ media('img/firefox/new/firefox-logo.png') }}" alt="Firefox" />

will output an image::

    <img src="/media/img/firefox/new/firefox-logo.png" alt="Firefox">

high_res_img()
^^^^^^^^^^^^^^
For images that include a high-resolution alternative for displays with a high pixel density, use the `high_res_img()` function::

    high_res_img('img/firefox/new/firefox-logo.png', {'alt': 'Firefox', 'width': '200', 'height': '100'})

The `high_res_img()` function will automatically look for the image in the URL parameter suffixed with `'-high-res'`, e.g. `img/firefox/new/firefox-logo-high-res.png` and switch to it if the display has high pixel density.

`high_res_img()` supports localized images by setting the `'l10n'` parameter to `True`::

    high_res_img('img/firefox/new/firefox-logo.png', {'l10n': True, 'alt': 'Firefox', 'width': '200', 'height': '100'})

When using localization, `high_res_img()` will look for images in the appropriate locale folder. In the above example, for the `de` locale, both standard and high-res versions of the image should be located at `media/img/l10n/de/firefox/new/`.

l10n_img()
^^^^^^^^^^
Images that have translatable text can be handled with `l10n_img()`::

    <img src="{{ l10n_img('firefox/os/have-it-all/messages.jpg') }}" />

The images referenced by `l10n_img()` must exist in `media/img/l10n/`, so for above example, the images could include `media/img/l10n/en-US/firefox/os/have-it-all/messages.jpg` and `media/img/l10n/es-ES/firefox/os/have-it-all/messages.jpg`.

platform_img()
^^^^^^^^^^^^^^
Finally, for outputting an image that differs depending on the platform being used, the `platform_img()` function will automatically display the image for the user's browser::

    platform_img('img/firefox/new/browser.png', {'alt': 'Firefox screenshot'})

`platform_img()` will automatically look for the images `browser-mac.png`, `browser-win.png`, `browser-linux.png`, etc. Platform image also supports hi-res images by adding `'data-high-res': true` to the list of optional attributes.

`platform_img()` supports localized images by setting the `'l10n'` parameter to `True`::

    platform_img('img/firefox/new/firefox-logo.png', {'l10n': True, 'alt': 'Firefox screenshot'})

When using localization, `platform_img()` will look for images in the appropriate locale folder. In the above example, for the `es-ES` locale, all platform versions of the image should be located at `media/img/l10n/es-ES/firefox/new/`.

Writing Views
-------------

You should rarely need to write a view for mozilla.org. Most pages are
static and you should use the `page` expression documented above.

If you need to write a view and the page has a newsletter signup form
in the footer (most do), make sure to handle this in your view.
Bedrock comes with a function for doing this automatically::

    from bedrock.mozorg.util import handle_newsletter
    from django.views.decorators.csrf import csrf_exempt

    @csrf_exempt
    def view(request):
        ctx = handle_newsletter(request)
        return l10n_utils.render(request, 'app/template.html', ctx)

You'll notice a few other things in there. You should use the
`l10n_utils.render` function to render templates because it handles
special l10n work for us. Since we're handling the newsletter form
post, you also need the `csrf_exempt` decorator.

Make sure to namespace your templates by putting them in a directory
named after your app, so instead of templates/template.html they would
be in templates/blog/template.html if `blog` was the name of your app.

Python and Django Style
-----------------------

See the `Mozilla Coding Standards
<http://mozweb.readthedocs.org/en/latest/coding.html>`_.

JavaScript Style
----------------

See the `Mozilla JS Style Guide
<http://mozweb.readthedocs.org/en/latest/js-style.html>`_.

CSS Style
---------

See the `Mozilla CSS Style Guide
<http://mozweb.readthedocs.org/en/latest/css-style.html>`_.

Use the ``.open-sans``, ``.open-sans-light`` and ``.open-sans-extrabold`` mixins
to specify font families to allow using international fonts. See the :ref:
`CSS<l10n>` section in the l10n doc for details.

Configuring your code editor
----------------------------

Bedrock includes an `.editorconfig` file in the root directory that you can
use with your code editor to help maintain consistent coding styles. Please
see `editorconfig.org <http://editorconfig.org/>`_. for a list of supported
editors and available plugins.
