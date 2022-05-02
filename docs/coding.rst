.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _coding:

=====================
Developing on Bedrock
=====================

Managing Dependencies
---------------------

For Python we use ``pip-compile`` from `pip-tools <https://pypi.org/project/pip-tools/>`_ to manage dependencies expressed in
our `requirements files <https://github.com/mozilla/bedrock/tree/main/requirements>`_.
``pip-compile`` is wrapped up in Makefile commands, to ensure we use it consistently.

If you add a new Python dependency (eg to ``requirements/prod.in`` or ``requirements/dev.in``) you can generate a pinned and hash-marked
addition to our requirements files just by running:

.. code-block:: shell

    make compile-requirements

and committing any changes that are made. Please re-build your docker image and test
it with ``make build test`` to be sure the dependency does not cause a regression.

Similarly, if you *upgrade* a pinned dependency in an ``*.in`` file, run
``make compile-requirements`` then rebuild, test and commit the results

To check for stale Python dependencies (basically ``pip list -o`` but in the Docker container):

.. code-block:: shell

    make check-requirements

For Node packages we use `NPM <https://docs.npmjs.com/cli/v8/commands/npm-install>`_, which should already be
installed alongside `Node.js <https://nodejs.org/>`_.

Asset Management and Bundling
-----------------------------

Bedrock uses `Webpack <https://webpack.js.org/>`_ to manage front-end
asset processing and bundling. This includes processing and minifying
JavaScript and SCSS/CSS bundles, as well as managing static assets
such as images, fonts, and other common file types.

When developing on bedrock you can start Webpack by running ``make run``
when using Docker, or ``npm start`` when running bedrock locally.

Once Webpack has finished compiling, a local development server
will be available at `localhost:8000 <http://localhost:8000/>`_. When
Webpack detects changes to a JS/SCSS file, it will automatically
recompile the bundle and then refresh any page running locally in the
browser.

Webpack Configuration
~~~~~~~~~~~~~~~~~~~~~

We have two main Webpack config files in the root directory:

The ``webpack.static.config.js`` file is responsible for copying static
assets, such as images and fonts, from the ``/media/`` directory over to
the ``/assets/`` directory. This is required so Django can serve them
correctly.

The ``webpack.config.js`` file is responsible for processing JS and SCSS
files in the ``/media/`` directory and compiling them into the ``/assets/``
directory. This config file also starts a local development server and
watches for file changes.

We use two separate config files to keep responsibilities clearly defined,
and to make the configs both shorter and easier to follow.

.. note::

    Because of the large number of files used in bedrock, only JS and SCSS
    files managed by ``webpack.config.js`` are watched for changes when in
    development mode. This helps save on memory consumption. The implication
    of this is that files handled by ``webpack.static.config.js``
    are only copied over when Webpack first runs. If you update an image for
    example, then you will need to stop and restart Webpack to pick up the
    change. This is not true for JS and SCSS files, which will be watched
    for change automatically.

Asset Bundling
~~~~~~~~~~~~~~

Asset bundles for both JS and SCSS are defined in ``./media/static-bundles.json``.
This is the file where you can define the bundle names that will get used in page
templates. For example, a CSS bundle can be defined as:

.. code-block:: json

    "css": [
        {
            "files": [
                "css/firefox/new/basic/download.scss"
            ],
            "name": "firefox_new_download"
        }
    ]

Which can then be referenced in a page template using:

.. code-block:: jinja

    {{ css_bundle('firefox_new_download') }}

A JS bundle can be defied as:

.. code-block:: json

    "js": [
        {
            "files": [
                "protocol/js/protocol-modal.js",
                "js/firefox/new/basic/download.js"
            ],
            "name": "firefox_new_download"
        }
    ]

Which can then be referenced in a page template using:

.. code-block:: jinja

    {{ js_bundle('firefox_new_download') }}

Once you define a bundle in ``static-bundles.json``, the ``webpack.config.js``
file will use these as entrypoints for compiling JS and CSS and watching for
changes.

Writing JavaScript
------------------

Bedrock's Webpack configuration supports some different options for writing
JavaScript:

Default Configuration
~~~~~~~~~~~~~~~~~~~~~

Write ``example-script.js`` using ES5 syntax and features. Webpack will bundle
the JS as-is, without any additional pre-processing.

Babel Configuration
~~~~~~~~~~~~~~~~~~~

Write ``example-script.es6.js`` using ES2015+ syntax. Webpack will transpile
the code to ES5 using `Babel <https://babeljs.io/>`_. This is useful when
you want to write modern syntax but still support older browsers.

.. important::

    Whilst Babel will transpile most modern JS syntax to ES5 when suitable
    fallbacks exist, it won't automatically include custom polyfills for
    everything since these can start to greatly increase bundle size. If you
    want to use ``Promise`` or ``async/await`` functions for example, then
    you will need to load polyfills for those. This can be done either at
    the page level, or globally in ``lib.js`` if it's something that multiple
    pages would benefit from. But please pick and choose wisely, and be
    concious of performance.

For pages that are served to Firefox browsers only, such as ``/whatsnew``, it is
also possible to write native ES2015+ syntax and serve that directly in production.
Here there is no need to include the ``.es6.js`` file extension. Instead, you can
simply use ``.js`` instead. The rules that which files you can do this in are defined
in our `ESLint config <https://github.com/mozilla/bedrock/blob/main/.eslintrc.js>`_.

Writing URL Patterns
--------------------

URL patterns should be the entire URL you desire, minus any prefixes from URLs files
importing this one, and including a trailing slash.  You should also give the URL a name
so that other pages can reference it instead of hardcoding the URL. Example:

.. code-block:: python

    path("channel/", channel, name="mozorg.channel")

If you only want to render a template and don't need to do anything else in a custom view,
Bedrock comes with a handy shortcut to automate all of this:

.. code-block:: python

    from bedrock.mozorg.util import page
    page("channel/", "mozorg/channel.html")

You don't need to create a view. It will serve up the specified
template at the given URL (the first parameter. see the
`Django docs <https://docs.djangoproject.com/en/3.2/ref/urls/#django.urls.path>`_ for details).
You can also pass template data as keyword arguments:

.. code-block:: python

    page("channel/", "mozorg/channel.html",
         latest_version=product_details.firefox_versions["LATEST_FIREFOX_VERSION"])

The variable `latest_version` will be available in the template.

Finding Templates by URL
------------------------

General Structure
~~~~~~~~~~~~~~~~~

Bedrock follows the Django app structure and most templates are easy to find by matching URL path segments to folders and files within the correct app.

| URL: ``https://www.mozilla.org/en-US/firefox/features/private-browsing/``
| Template path:  ``bedrock/bedrock/firefox/templates/firefox/features/private-browsing.html``

To get from URL to template path:

- Ignore ``https://www.mozilla.org`` and the locale path segment ``/en-US``. The next path segment is the app name ``/firefox``.
- From the root folder of bedrock, find the app's template folder at ``bedrock/{app}/templates/{app}``
- Match remaining URL path segments (``/features/private-browsing``) to the template folder's structure (``/features/private-browsing.html``)

.. note::

    ``mozorg`` is the app name for the home page and child pages related to Mozilla Corporation (i.e. About, Contact, Diversity).

Whatsnew and Firstrun
~~~~~~~~~~~~~~~~~~~~~

These pages are specific to Firefox browsers, and only appear when a user updates or installs and runs a Firefox browser for the first time.
The URL and template depend on what Firefox browser and version are in use.

.. note::

    There may be extra logic in the app's ``views.py`` file to change the template based on locale or geographic location as well.

Firefox release
^^^^^^^^^^^^^^^

Version number is digits only.

| Whatsnew URL: https://www.mozilla.org/en-US/firefox/99.0/whatsnew/
| Template path:  https://github.com/mozilla/bedrock/tree/main/bedrock/firefox/templates/firefox/whatsnew

| Firstrun URL: https://www.mozilla.org/en-US/firefox/99.0/firstrun/
| Template path:  https://github.com/mozilla/bedrock/blob/main/bedrock/firefox/templates/firefox/firstrun/firstrun.html

Firefox Nightly
^^^^^^^^^^^^^^^

Version number is digits and **a1**.

| Whatsnew URL: https://www.mozilla.org/en-US/firefox/99.0a1/whatsnew/
| Template path:  https://github.com/mozilla/bedrock/blob/main/bedrock/firefox/templates/firefox/nightly/whatsnew.html

| Firstrun URL: https://www.mozilla.org/en-US/firefox/nightly/firstrun/
| Template path:  https://github.com/mozilla/bedrock/tree/main/bedrock/firefox/templates/firefox/nightly

Firefox Developer
^^^^^^^^^^^^^^^^^

Version number is digits and **a2**.

| Whatsnew URL: https://www.mozilla.org/en-US/firefox/99.0a2/whatsnew/
| Template path:  https://github.com/mozilla/bedrock/blob/main/bedrock/firefox/templates/firefox/developer/whatsnew.html

| Firstrun URL: https://www.mozilla.org/en-US/firefox/99.0a2/firstrun/
| Template path:  https://github.com/mozilla/bedrock/blob/main/bedrock/firefox/templates/firefox/developer/firstrun.html


Release Notes
~~~~~~~~~~~~~

Release note templates live here: https://github.com/mozilla/bedrock/tree/main/bedrock/firefox/templates/firefox/releases

.. note::

    Release note content is pulled in from an external data source.

- Firefox release: https://www.mozilla.org/en-US/firefox/99.0.1/releasenotes/
- Firefox Developer and Beta: https://www.mozilla.org/en-US/firefox/100.0beta/releasenotes/
- Firefox Nightly: https://www.mozilla.org/en-US/firefox/101.0a1/releasenotes/
- Firefox Android: https://www.mozilla.org/en-US/firefox/android/99.0/releasenotes/
- Firefox iOS: https://www.mozilla.org/en-US/firefox/ios/99.0/releasenotes/


Optimizing Images
-----------------

Images can take a long time to load and eat up a lot of bandwidth. Always take care
to optimize images before uploading them to the site.

The script `img.sh` can be used to optimize images locally on the command line:

#. Before you run it for the first time you will need to run `npm install` to install dependencies
#. Add the image files to git's staging area `git add *`
#. Run the script `./bin/img.sh`
#. The optimized files will not automatically be staged, so be sure to add them before commiting

The script will:

- optimize JPG and PNG files using `tinypng <https://tinypng.com/>`_ (
    - this step is optional since running compression on the same images over and over degrades them)
    - you will be prompted to add a `TinyPNG API key <https://tinypng.com/developers>`_
- optimize SVG images locally with svgo
- check that SVGs have a viewbox (needed for IE support)
- check that images that end in `-high-res` have low res versions as well

Embedding Images
----------------

Images should be included on pages using helper functions.

static()
~~~~~~~~

For a simple image, the `static()` function is used to generate the image URL. For example:

.. code-block:: html

    <img src="{{ static('img/firefox/new/firefox-logo.png') }}" alt="Firefox" />

will output an image:

.. code-block:: html

    <img src="/media/img/firefox/new/firefox-logo.png" alt="Firefox">

high_res_img()
~~~~~~~~~~~~~~

For images that include a high-resolution alternative for displays with a high pixel density, use the `high_res_img()` function:

.. code-block:: python

    high_res_img("img/firefox/new/firefox-logo.png", {"alt": "Firefox", "width": "200", "height": "100"})

The `high_res_img()` function will automatically look for the image in the URL parameter suffixed with `'-high-res'`, e.g. `img/firefox/new/firefox-logo-high-res.png` and switch to it if the display has high pixel density.

`high_res_img()` supports localized images by setting the `'l10n'` parameter to `True`:

.. code-block:: python

    high_res_img("img/firefox/new/firefox-logo.png", {"l10n": True, "alt": "Firefox", "width": "200", "height": "100"})

When using localization, `high_res_img()` will look for images in the appropriate locale folder. In the above example, for the `de` locale, both standard and high-res versions of the image should be located at `media/img/l10n/de/firefox/new/`.

l10n_img()
~~~~~~~~~~

Images that have translatable text can be handled with `l10n_img()`:

.. code-block:: html

    <img src="{{ l10n_img('firefox/os/have-it-all/messages.jpg') }}" />

The images referenced by `l10n_img()` must exist in `media/img/l10n/`, so for above example, the images could include `media/img/l10n/en-US/firefox/os/have-it-all/messages.jpg` and `media/img/l10n/es-ES/firefox/os/have-it-all/messages.jpg`.

platform_img()
~~~~~~~~~~~~~~

Finally, for outputting an image that differs depending on the platform being used, the `platform_img()` function will automatically display the image for the user's browser:

.. code-block:: python

    platform_img("img/firefox/new/browser.png", {"alt": "Firefox screenshot"})

`platform_img()` will automatically look for the images `browser-mac.png`, `browser-win.png`, `browser-linux.png`, etc. Platform image also supports hi-res images by adding `'high-res': True` to the list of optional attributes.

`platform_img()` supports localized images by setting the `'l10n'` parameter to `True`:

.. code-block:: python

    platform_img("img/firefox/new/firefox-logo.png", {"l10n": True, "alt": "Firefox screenshot"})

When using localization, `platform_img()` will look for images in the appropriate locale folder. In the above example, for the `es-ES` locale, all platform versions of the image should be located at `media/img/l10n/es-ES/firefox/new/`.

qrcode()
~~~~~~~~

This is a helper function that will output SVG data for a QR Code at the spot in the template
where it is called. It caches the results to the ``data/qrcode_cache`` directory, so it only
generates the SVG data one time per data and box_size combination.

.. code-block:: python

    qrcode("https://accounts.firefox.com", 30)

The first argument is the data you'd like to encode in the QR Code (usually a URL), and the second
is the "box size". It's a parameter that tells the generator how large to set the height and width
parameters on the XML SVG tag, the units of which are "mm". This can be overriden with CSS so you
may not need to use it at all. The ``box_size`` parameter is optional.

image()
~~~~~~~

We also have an image macro, which is mainly used to encapsulate the conditional logic needed for `Protocol macros <https://bedrock.readthedocs.io/en/latest/coding.html#working-with-protocol>`_ containing images. You can also import the macro directly into a template.

.. code-block:: jinja

    {% from 'macros.html' import image with context %}

    {{ image(
        url='example.jpg',
        alt='example alt',
        class='example class',
        width='64',
        height='64',
        loading='lazy',
        include_highres=True,
        include_l10n=True
    ) }}

Only ``url`` is required. By default, alt text will be an empty string, loading will be determined by the browser, and highres/l10n images will not be included. For ``include_l10n=True`` to work, you must import the macro `with context`.

Using Large Assets
------------------

We don't want to (and if large enough GitHub won't let us) commit large files to the bedrock repo.
Files such as large PDFs or very-high-res JPG files (e.g. leadership team photos), or videos are not
well-tracked in git and will make every checkout after they're added slower and this diffs less useful.
So we have another domain at which we upload these files: assets.mozilla.net

This domain is simply an AWS S3 bucket with a CloudFront :abbr:`CDN (Content Delivery Network)` in front of it. It is highly available
and fast. We've made adding files to this domain very simple using `git-lfs <https://git-lfs.github.com/>`_.
You simply install git-lfs, clone our `assets.mozilla.net repo <https://github.com/mozmeao/assets.mozilla.net>`_,
and then add and commit files under the ``assets`` directory there as usual. Open a pull request, and once it's merged
it will be automatically uploaded to the S3 bucket and be available on the domain.

For example, if you add a file to the repo under ``assets/pdf/the-dude-abides.pdf``, it will be available
as https://assets.mozilla.net/pdf/the-dude-abides.pdf. Once that is done you can link to that URL from bedrock
as you would any other URL.

Writing Migrations
------------------

Bedrock uses Django's built-in Migrations framework for its database migrations, and has no custom
database routing, etc. So, no big surprises here – write things as you regularly would.

*However*, as with any complex system, care needs to be taken with schema changes that
drop or rename database columns. Due to the way the rollout process works (ask for
details directly from the team), an absent column can cause some of the rollout to
enter a crashloop.

To avoid this, split your changes across releases, such as below.

For column renames:

* Release 1: Add your new column
* Release 2: Amend the codebase to use it instead of the old column
* Release 3: Clean up - drop the old, deprecated column, which should not be referenced in code at this point.

For column drops:

* Release 1: Update all code that uses the relevant column, so that nothing interacts with it any more.
* Release 2: Clean up - drop the old, deprecated column.

With both paths, check for any custom schema or data migrations that might reference the deprecated column.

Writing Views
-------------

You should rarely need to write a view for mozilla.org. Most pages are
static and you should use the `page` function documented above.

If you need to write a view and the page is translated or translatable
then it should use the `l10n_utils.render()` function to render the
template.

.. code-block:: python

    from lib import l10n_utils

    from django.views.decorators.http import require_safe


    @require_safe
    def my_view(request):
        # do your fancy things
        ctx = {"template_variable": "awesome data"}
        return l10n_utils.render(request, "app/template.html", ctx)

Make sure to namespace your templates by putting them in a directory
named after your app, so instead of templates/template.html they would
be in templates/blog/template.html if `blog` was the name of your app.

The `require_safe` ensures that only `GET` or `HEAD` requests will make it
through to your view.

If you prefer to use Django's Generic View classes we have a convenient
helper for that. You can use it either to create a custom view class of
your own, or use it directly in a `urls.py` file.

.. code-block:: python

    # app/views.py
    from lib.l10n_utils import L10nTemplateView

    class FirefoxRoxView(L10nTemplateView):
        template_name = "app/firefox-rox.html"

    # app/urls.py
    urlpatterns = [
        # from views.py
        path("firefox/rox/", FirefoxRoxView.as_view()),
        # directly
        path("firefox/sox/", L10nTemplateView.as_view(template_name="app/firefox-sox.html")),
    ]

The `L10nTemplateView` functionality is mostly in a template mixin called `LangFilesMixin` which
you can use with other generic Django view classes if you need one other than `TemplateView`. 
The `L10nTemplateView` already ensures that only `GET` or `HEAD` requests will be served.

Variation Views
~~~~~~~~~~~~~~~

We have a generic view that allows you to easily create and use a/b testing
templates. If you'd like to have either separate templates or just a template
context variable for switching, this will help you out. For example.

.. code-block:: python

    # urls.py

    from django.urls import path

    from bedrock.utils.views import VariationTemplateView

    urlpatterns = [
        path("testing/",
             VariationTemplateView.as_view(template_name="testing.html",
                                           template_context_variations=["a", "b"]),
             name="testing"),
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

    from django.urls import path

    from bedrock.utils.views import VariationTemplateView

    urlpatterns = [
        path("testing/",
             VariationTemplateView.as_view(template_name="testing.html",
                                           template_name_variations=["1", "2"]),
             name="testing"),
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

    from django.urls import path

    from bedrock.utils.views import VariationTemplateView

    urlpatterns = [
        path("testing/",
             VariationTemplateView.as_view(template_name="testing.html",
                                           template_name_variations=["1", "2"],
                                           variation_locales=["en-US", "de"]),
             name="testing"),
    ]

Any request to the page in for example French would not use the alternate template even if a
valid variation were given in the URL.

.. note::

    If you'd like to add this functionality to an existing Class-Based View, there is
    a mixin that implements this pattern that should work with most views:
    `bedrock.utils.views.VariationMixin`.

Geo Template View
~~~~~~~~~~~~~~~~~

Now that we have our :abbr:`CDN (Content Delivery Network)` configured properly, we can also just swap out templates
per request country. This is very similar to the above, but it will simply use
the proper template for the country from which the request originated.

.. code-block:: python

    from bedrock.base.views import GeoTemplateView

    class CanadaIsSpecialView(GeoTemplateView):
        geo_template_names = {
            "CA": "mozorg/canada-is-special.html",
        }
        template_name = "mozorg/everywhere-else-is-also-good.html"

For testing purposes while you're developing or on any deployment that is not
accessed via the production domain (www.mozilla.org) you can append your URL
with a ``geo`` query param (e.g. ``/firefox/?geo=DE``) and that will take
precedence over the country from the request header.

Other Geo Stuff
~~~~~~~~~~~~~~~

There are a couple of other tools at your disposal if you need to change things
depending on the location of the user. You can use the
``bedrock.base.geo.get_country_from_request`` function in a view and it will
return the country code for the request (either from the :abbr:`CDN (Content Delivery Network)` or the query param,
just like above).

.. code-block:: python

    from bedrock.base.geo import get_country_from_request

    def dude_view(request):
        country = get_country_from_request(request)
        if country == "US":
            # do a thing for the US
        else:
            # do the default thing

The other convenience available is that the country code, either from the :abbr:`CDN (Content Delivery Network)`
or the query param, is avilable in any template in the ``country_code`` variable.
This allows you to change anything about how the template renders based on the
location of the user.

.. code-block:: jinja

    {% if country_code == "US" %}
        <h1>GO MURICA!</h1>
    {% else %}
        <h1>Yay World!</h1>
    {% endif %}

Coding Style
------------

Bedrock uses the following open source tools to follow coding styles and conventions,
as well as applying automatic code formatting:

* `black <https://black.readthedocs.io/>`_ for Python code formatting.
* `flake8 <https://flake8.pycqa.org/>`_ for Python style and code quality rules.
* `isort <https://pycqa.github.io/isort/>`_ for Python import ordering consistency.
* `Prettier <https://prettier.io/>`_ for JavaScript code formatting.
* `ESLint <https://eslint.org/>`_ for JavaScript code quality rules.
* `Stylelint <https://stylelint.io/>`_ for Sass/CSS style and code quality rules.

For front-end HTML & CSS conventions, bedrock uses Mozilla's Protocol design system for
building components. You can read the `Protocol documentation site <https://protocol.mozilla.org/>`_
for more information.

Mozilla also has some more general coding styleguides available, although some of
these are now rather outdated:

* `Mozilla Python Style Guide <http://mozweb.readthedocs.org/en/latest/reference/python-style.html>`_
* `Mozilla HTML Style Guide <http://mozweb.readthedocs.org/en/latest/reference/html-style.html>`_
* `Mozilla JS Style Guide <http://mozweb.readthedocs.org/en/latest/reference/js-style.html>`_
* `Mozilla CSS Style Guide <http://mozweb.readthedocs.org/en/latest/reference/css-style.html>`_


Test coverage
-------------

When the Python tests are run, a coverage report is generated, showing which lines of the
codebase have tests that execute them, and which do not. You can view this report in your
browser at ``file:///path/to/your/checkout/of/bedrock/python_coverage/index.html``.

When adding code, please aim to provide solid test coverage, using the coverage report as
a guide. This doesn't necessarily mean every single line needs a test, and 100% coverage
doesn't mean 0% defects.


Configuring your Code Editor
----------------------------

Bedrock includes an `.editorconfig` file in the root directory that you can
use with your code editor to help maintain consistent coding styles. Please
see `editorconfig.org <http://editorconfig.org/>`_. for a list of supported
editors and available plugins.

Working with Protocol Design System
-----------------------------------

Bedrock uses the `Protocol Design System <https://protocol.mozilla.org/>`_ to quickly produce consistent, stable components. There are different methods -- depending on the component -- to import a Protocol component into our codebase.

One method involves two steps:

1. Adding the `correct markup <#styles-and-components>`_ or importing the `appropriate macro <#macros>`_ to the page's HTML file.
2. Importing the necessary Protocol styles to a page's SCSS file.

The other method is to `import CSS bundles <#import-css-bundles>`_ onto the HTML file. However, this only works for certain components, which are listed below in the respective section.


Styles and Components
~~~~~~~~~~~~~~~~~~~~~
The base templates in Bedrock have global styles from Protocol that apply to every page. When we need to extend these styles on a page-specific basis, we set up Protocol in a page-specific SCSS file.

For example, on a Firefox product page, we might want to use Firefox logos or wordmarks that do not exist on every page.

To do this, we add Protocol ``mzp-`` classes to the HTML:

.. code-block:: html

    // bedrock/bedrock/firefox/templates/firefox/{specific-page}.html

    <div class="mzp-c-wordmark mzp-t-wordmark-md mzp-t-product-firefox">
        Firefox Browser
    </div>

Then we need to include those Protocol styles in the page's SCSS file:

.. code-block:: css

    /* bedrock/media/css/firefox/{specific-page}.scss */

    /* if we need to use protocol images, we need to set the $image-path variable */
    $image-path: '/media/protocol/img';
    /* mozilla is the default theme, so if we want a different one, we need to set the $brand-theme variable */
    $brand-theme: 'firefox';

    /* the lib import is always essential: it provides access to tokens, functions, mixins, and theming */
    @import '~@mozilla-protocol/core/protocol/css/includes/lib';
    /* then you add whatever specific protocol styling you need */
    @import '~@mozilla-protocol/core/protocol/css/components/logos/wordmark';
    @import '~@mozilla-protocol/core/protocol/css/components/logos/wordmark-product-firefox';

.. note::
    If you create a new SCSS file for a page, you will have to include it in that page's CSS bundle by updating
    `static-bundles.json <#asset-bundling>`_ file.


Macros
~~~~~~

The team has created several `Jinja macros <https://jinja.palletsprojects.com/en/3.1.x/templates/?=macros#macros>`_ out of Protocol components to simplify the usage of components housing larger blocks of code (i.e. Billboard). The code housing the custom macros can be found in our `protocol macros file <https://github.com/mozilla/bedrock/blob/main/bedrock/base/templates/macros-protocol.html>`_. These Jinja macros include parameters that are simple to define and customize based on how the component should look like on a given page.

To use these macros in files, we simply import a macro to the page's HTML code and call it with the desired arguments, instead of manually adding Protocol markup. We can import multiple macros in a comma-separated fashion, ending the import with ``with context``:

.. code-block:: html

    // bedrock/bedrock/firefox/templates/firefox/{specific-page}.html

    {% from "macros-protocol.html" import billboard with context %}

    {{ billboard(
        title='This is Firefox.',
        ga_title='This is Firefox',
        desc='Firefox is an awesome web browser.',
        link_cta='Click here to install',
        link_url=url('firefox.new')
      )}}

Because not all component styles are global, we still have to import the page-specific Protocol styles in SCSS:

.. code-block:: css

    /* bedrock/media/css/firefox/{specific-page}.scss */

    $brand-theme: 'firefox';

    @import '~@mozilla-protocol/core/protocol/css/includes/lib';
    @import '~@mozilla-protocol/core/protocol/css/components/billboard';


Import CSS Bundles
~~~~~~~~~~~~~~~~~~
We created pre-built CSS bundles to be used for some components due to their frequency of use. This method only requires an import into the HTML template. Since it’s a separate CSS bundle, we don’t need to import that component in the respective page CSS.
The CSS bundle import only works for the following components:

* Split
* Card
* Picto
* Callout
* Article
* Newsletter form
* Emphasis box

Include a CSS bundle in the template's ``page_css`` block along with any other page-specific bundles, like so:

.. code-block:: html

    {% block page_css %}
        {{ css_bundle('protocol-split') }}
        {{ css_bundle('protocol-card') }}
        {{ css_bundle('page-specific-bundle') }}
    {% endblock %}


Imports and Parameters
~~~~~~~~~~~~~~~~~~~~~~

You can find import examples and parameter definitions for the available Protocol macros below.

.. note::
    You can use Protocol without macros. They are not dependent on each other but they work well together. 10/10 would recommend!

Picto
^^^^^

**HTML import**

.. code-block:: html

    {% block page_css %}
        {{ css_bundle('protocol-picto') }}
    {% endblock %}

**Macro parameters**

- title
    String indicating heading text (usually a translation id wrapped in ftl function)

    Default: None

    Example: ``title=ftl('misinformation-why-trust-firefox')``

- heading_level
    Number indicating heading level for title text. Should be based on semantic meaning, not presentational styling.

    Default: 3

    Example: ``heading_level=2``

- body
    A boolean attribute. If true, it will show the contents of the card, if false, it will hide the contents.

    Default: False

    Example: ``body=True``

- image_url
    image location to be used. Start it off with ‘img/…’.

    Default: ''

    Example: ``image_url='img/icons/mountain-purple.svg'``

- base_el
    The element the content of the picto will be read as in HTML. For example, if the Picto macro is wrapped in a ul tag, the base_el would be an li tag.

    Default: div

    Example: ``base_el='li'``

- class
    String adding class(es) to the base el tag.

    Default: None

    Example: ``class='trust'``

- image_width
    Number indicating width of image.

    Default: 64

    Example: ``image_width='153px'``

- include_highres_image
    Boolean that determines whether the image can also appear in high res.

    Default: False

    Example: ``include_highres_image=True``

- l10n_image
    Boolean to indicate if image has translatable text.

    Default: False

    Example: ``l10n_image=True``


- loading
    String to provide value for image loading attribute. This will use browser default ("eager") if not set. Lazy loading defers fetching of images to a browser decision based on user scroll and connection.

    Default: None

    Example: ``loading='lazy'``



Call out
^^^^^^^^

**HTML import**

.. code-block:: html

    {% block page_css %}
        {{ css_bundle('protocol-call-out') }}
    {% endblock %}

**Macro parameters**

- title
    **Required**. String indicating heading text (usually a translation id wrapped in ftl function).

    Default: N/A

    Example: ``title=ftl('firefox-privacy-hub-read-the-privacy-notice-for')``

- desc
    String indicating paragraph text (usually a translation id wrapped in ftl function).

    Default: None

    Example: ``desc=ftl('firefox-channel-test-beta-versions-of-firefox-ios')``

- class
    String adding class(es) to the section tag.

    Default: None

    Example: ``class='mzp-t-firefox ' + product_class``

- include_cta
    Boolean indicating whether or not to include the body of the macro call (usually a mix of text and html).

    Default: None

    Example: ``include_cta=True``

- heading_level
    Number indicating heading level for title text. Should be based on semantic meaning, not presentational styling.

    Default: 2

    Example: ``heading_level=1``


Split
^^^^^

**HTML import**

.. code-block:: html

    {% block page_css %}
        {{ css_bundle('protocol-split') }}
    {% endblock %}

**Macro parameters**

- block_id
    String providing id to the section tag (usually if it needs to be used as an in-page link).

    Default: None

    Example: ``id='nextgen``

- base_el
    String for block HTML tag not required.

    Default: section

    Example: ``base_el='aside'``

- block_class
    String providing class(es) to the section tag.

    Default: None

    Example: ``block_class='mzp-l-split-reversed mzp-l-split-center-on-sm-md``

- theme_class
    String providing theme class(es) to a container div tag inside the section.

    Default: None

    Example: ``theme_class='mzp-t-dark'``

- body_class
    String providing class(es) to the body (text content) div inside the section.

    Default: None

    Example: ``Not currently in use``

- image_url
    Path to image location.

    Default: None

    Example: ``image_url=’img/firefox/accounts/trailhead/value-respect.jpg’``

- media_class
    String providing class(es) to the media div inside the section.

    Default: None

    Example: ``media_class='mzp-l-split-h-center'``

- include_highres_image
    Boolean that determines whether the image can also appear in high res.

    Default: False

    Example: ``include_highres_image=True``

- l10n_image
    Boolean to indicate if image has translatable text.

    Default: False

    Example: ``l10n_image=True``

- image_alt
    String providing alt text to the image.

    Default: ''

    Example: ``Not currently in use``

- media_after
    Boolean to determine if image appears before or after text when stacked on mobile size screens.

    Default: False

    Example: ``media_after=True``

- media_include
    Path to video media.

    Default: None

    Example: ``media_include='firefox/facebookcontainer/includes/video.html'``

- loading
    String to provide value for image loading attribute. This will use browser default ("eager") if not set. Lazy loading defers fetching of images to a browser decision based on user scroll and connection.

    Default: None

    Example: ``loading='lazy'``


Billboard
^^^^^^^^^

**HTML import**

.. code-block:: html

   {% from "macros-protocol.html" import billboard with context %}

**CSS import**

.. code-block:: css

   @import '~@mozilla-protocol/core/protocol/css/components/billboard';

**Macro parameters**

- title
    **Required**. String indicating heading text (usually a translation id wrapped in ftl function).

    Default: N/A

    Example: ``title=ftl('about-the-mozilla-manifesto')``

- ga_title
    **Required**. String providing value for data-link-name attribute on cta.

    Default: N/A

    Example: ``ga_title='The Mozilla Manifesto'``

- desc
    **Required**.String indicating paragraph text (usually a translation id wrapped in ftl function).

    Default: N/A

    Example: ``desc=ftl('about-the-principles-we-wrote-in')``

- link_cta
    **Required**. String indicating link text (usually a translation id wrapped in an ftl function).

    Default: N/A

    Example: ``link_cta=ftl('about-read-the-manifesto')``

- link_url
    **Required**. String or url helper function provides href value for cta link.

    Default: N/A

    Example: ``link_url=url('mozorg.about.manifesto')``

- image_url
    **Required**. Path to image location.

    Default: N/A

    Example: ``image_url='img/home/2018/billboard-healthy-internet.png'``

- include_highres_image
    Boolean that determines whether the image can also appear in high res.

    Default: False

    Example: ``include_highres_image=True``

- reverse
    Uses default layout: mzp-l-billboard-rightReverse will switch to billboard (text) left.

    Default: False

    Example: ``reverse=True``

- heading_level
    Number indicating heading level for title text. Should be based on semantic meaning, not presentational styling.

    Default: 2

    Example: ``heading_level=1``

- loading
    String to provide value for image loading attribute. This will use browser default ("eager") if not set. Lazy loading defers fetching of images to a browser decision based on user scroll and connection.

    Default: None

    Example: ``loading='lazy'``


Feature Card
^^^^^^^^^^^^

**HTML import**

.. code-block:: html

   {% from "macros-protocol.html" import feature_card with context %}

**CSS import**

.. code-block:: css

   @import '~@mozilla-protocol/core/protocol/css/components/feature-card';

**Macro parameters**

- title
    String indicating heading text (usually a translation id wrapped in ftl function).

    Default: None

    Example: ``title=ftl('firefox-home-firefox-browser')``

- ga_title
    String used as an identifying name on a link for google analytics. Only used if link_url and link_cta are provided as well.

    Default: None

    Example: ``ga_title='Firefox Windows'``

- image_url
    Path to image location.

    Default: N/A

    Example: ``image_url=’img/firefox/accounts/trailhead/value-respect.jpg’``

- class
    String adding class(es) to the section tag.

    Default: None

    Example: ``class=’mzp-l-card-feature-left-half t-mozvpn’``

- link_url
    String or url helper function provides href value for cta link. Only used if link_cta is provided as well.

    Default: None

    Example: ``link_url=url('firefox.privacy.index')``

- link_cta
    String indicating link text (usually a translation id wrapped in an ftl function). Only used if link_url is provided as well.

    Default: None

    Example: ``link_cta=ftl('ui-learn-more')``

- include_highres_image
    Boolean that determines whether the image can also appear in high res.

    Default: False

    Example: ``include_highres_image=True``

- l10n_image
    Boolean to indicate if image has translatable text.

    Default: False

    Example: ``l10n_image=True``

- aspect_ratio
    aspect_ratio 	String with an mzp class name indicating desired aspect ratio (adds class to section tag).

    Default: False

    Example: ``aspect_ratio='mzp-has-aspect-3-2'``

- heading_level
    Number indicating heading level for title text. Should be based on semantic meaning, not presentational styling.

    Default: 2

    Example: ``heading_level=3``

- media_after
    Boolean to determine if image appears before or after text when stacked on mobile size screens.

    Default: False

    Example: ``media_after=True``

- loading
    String to provide value for image loading attribute. This will use browser default ("eager") if not set. Lazy loading defers fetching of images to a browser decision based on user scroll and connection.

    Default: None

    Example: ``loading='lazy'``


Card
^^^^

**HTML import**

.. code-block:: html

    {% block page_css %}
        {{ css_bundle('protocol-split') }}
    {% endblock %}

**Macro parameters**

- youtube_id
    String indicating the Youtube ID found at the end of a Youtube video URL. Used when we are embedding a video to the card rather than an image.

    Default: N/A

    Example: ``youtube_id='aHpCLDQ_2ns'``

- title
    **Required**. String indicating heading text (usually a translation id wrapped in ftl function).

    Default: N/A

    Example: ``title=ftl('about-the-mozilla-manifesto')``

- ga_title
    **Required**. String providing value for data-link-name attribute on cta.

    Default: N/A

    Example: ``ga_title='The Mozilla Manifesto'``

- desc
    **Required**. String indicating paragraph text (usually a translation id wrapped in ftl function).

    Default: N/A

    Example: ``desc=ftl('about-the-principles-we-wrote-in')``

- aspect_ratio
    String indicating size/aspect ratio of the card (make sure to have it even if it’s in a defined Card Layout.

    Default: N/A

    Example: ``aspect_ratio=’mzp-has-aspect-16-9’``

- link_url
    **Required**. String or url helper function provides href value for cta link.

    Default: N/A

    Example: ``link_url=url('mozorg.about.manifesto')``

- image_url
    **Required**. Path to image location.

    Default: N/A

    Example: ``image_url='img/home/2018/billboard-healthy-internet.png'``

- include_highres_image
    **Required**. Boolean that determines whether the image can also appear in high res.

    Default: N/A

    Example: ``include_highres_image=True``

- l10n_image
    Boolean to indicate if image has translatable text.

    Default: False

    Example: ``l10n_image=True``

- heading_level
    Number indicating heading level for title text. Should be based on semantic meaning, not presentational styling.

    Default: 3

    Example: ``heading_level=2``

- attributes
    A generic parameter to add any extra attributes to the component, such as data or aria attributes. Note that the quotes will pass through unescaped.

    Default: N/A

    Example: ``attributes='aria-role="menuitem"'``
