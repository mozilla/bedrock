.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _install:

==================
Installing Bedrock
==================

Installation
------------

These instructions assume you have `git` and `pip` installed. If you don't have `pip` installed
(you probably do) you can install it with the instructions in `the pip docs <https://pip.pypa.io/en/stable/installing/>`_.

Start by getting the source::

    $ git clone git://github.com/mozilla/bedrock.git
    $ cd bedrock

You need to create a virtual environment for Python libraries. Skip the first instruction if you already have virtualenv installed::

    $ pip install virtualenv                       # installs virtualenv, skip if already have it
    $ virtualenv -p python2.7 venv                 # create a virtual env in the folder `venv`
    $ source venv/bin/activate                     # activate the virtual env. On Windows, run: venv\Scripts\activate.bat
    $ pip install -U pip                           # securely upgrade pip
    $ pip install -r requirements/test.txt         # installs dependencies

If you are on OSX and some of the compiled dependencies fails to compile, try explicitly setting the arch flags and try again::

    $ export ARCHFLAGS="-arch i386 -arch x86_64"
    $ pip install -r requirements/test.txt

If you are on Linux, you will need at least the following packages or their equivalent for your distro::

    $ python-dev libxslt-dev

Now configure the application to run locally by creating your local settings environment file::

    $ cp .env-dist .env

You shouldn't need to customize anything in there yet.

Sync the database and all of the external data locally. This gets product-details, security-advisories,
credits, release notes, localizations, legal-docs etc::

    $ bin/bootstrap.sh

Lastly, you need to have `Node.js <https://nodejs.org/>`_ and
`Yarn <https://yarnpkg.com/>`_ installed. The node
dependencies for running the site can be installed with ``yarn``::

    $ yarn

You may also need to install the `Gulp <http://gulpjs.com/>`_ cli globally::

    $ npm install -g gulp-cli

.. note::

    Bedrock uses yarn to ensure that Node.js
    packages that get installed are the exact ones we meant (similar to pip hash checking mode for python). Refer
    to the `yarn documentation <https://yarnpkg.com/en/docs/yarn-workflow>`_
    for adding or upgrading Node.js dependencies.

.. _run-python-tests:

Run the tests
-------------

.. Important::

    We're working on fixing this, but for now you need the localization files for the tests to pass.
    See the `Localization`_ section below for instructions on checking those out.

Now that we have everything installed, let's make sure all of our tests pass.
This will be important during development so that you can easily know when
you've broken something with a change. You should still have your virtualenv
activated, so running the tests is as simple as::

    $ py.test lib bedrock

To test a single app, specify the app by name in the command above. e.g.::

    $ py.test lib bedrock/firefox

.. note::

    If your local tests run fine, but when you submit a pull-request the tests fail in
    `CircleCI <https://circleci.com/gh/mozilla/bedrock>`_, it could be due to the
    difference in settings between what you have in ``.env``
    and what CircleCI uses: ``docker/envfiles/demo.env``. You can run tests as close to Circle
    as possible by moving your ``.env`` file to another name (e.g. ``.env-backup``), then
    copying ``docker/envfiles/demo.env`` to ``.env``, and running tests again.

Make it run
-----------

To make the server run, make sure you are inside a virtualenv, and then
run the server::

    $ ./manage.py runserver

If you are not inside a virtualenv, you can activate it by doing::

    $ source venv/bin/activate

If you get the error "NoneType is not iterable", you didn't check out the latest product-details. See the above section for that.

Next, in a new terminal tab run gulp to watch for local file changes::

    $ gulp

This will automatically copy over CSS, JavaScript and image files to the /static directory as and when they change, which is needed for Django Pipeline to serve the assets as pages are requested.

If you have problems with gulp, or you for some reason don't want to use it you can set::

    PIPELINE_COLLECTOR_ENABLED=True

in your ``.env`` file or otherwise set it in your environment and it will collect media for you as you make changes. The reason that this is not the preferred method is that it is much slower than using gulp.

Localization
------------

Localization (or L10n) files were fetched by the `bootstrap.sh` command your ran earlier.
If you need to update them or switch to a different repo or branch after changing settings
you can run the following command::

    $ ./manage.py l10n_update

You can read more details about how to localize content :ref:`here<l10n>`.

Feature Flipping
----------------

Environment variables are used to configure behavior and/or features of select pages on bedrock
via a template helper function called ``switch()``. It will take whatever name you pass to it
(must be only numbers, letters, and dashes), convert it to uppercase, convert dashes to underscores,
and lookup that name in the environment. For example: ``switch('the-dude')`` would look for the
environment variable ``SWITCH_THE_DUDE``. If the value of that variable is any of "on", "true", "1", or
"yes", then it will be considered "on", otherwise it will be "off". If the environment variable ``DEV``
is set to one of those "true" values, then all switches will be considered "on" unless they are
explicitly "off" in the environment.

You can also supply a list of locale codes that will be the only ones for which the switch is active.
If the page is viewed in any other locale the switch will always return ``False``, even in ``DEV``
mode. This list can also include a "Locale Group", which is all locales with a common prefix
(e.g. "en-US, en-GB, en-ZA" or "zh-CN, zh-TW"). You specify these with just the prefix. So if you
used ``switch('the-dude', ['en', 'de'])`` in a template, the switch would be active for German and
any English locale the site supports.

You may also use these switches in Python in ``views.py`` files (though not with locale support).
For example::

    from bedrock.base.waffle import switch

    def home_view(request):
        title = 'Staging Home' if switch('staging-site') else 'Prod Home'
        ...

Currently, these switches are used to enable/disable Optimizely on many pages of the site. We only add
the Optimizely JavaScript snippet to a page when there is an active test to minimize the security risk
of the service. We maintain a `page on the Mozilla wiki detailing our use of Optimizely
<https://wiki.mozilla.org/Mozilla.org/Optimizely>`_ and these switches. You can see the current state of
these switches and other configuration values in our `configuration repo <https://mozmeao.github.io/www-config/configs/>`_.

To work with/test these Optimizely switches locally, you must add the switches to your local environment. For example::

    # to switch on firefox-new-optimizely you'd add the following to your ``.env`` file
    SWITCH_FIREFOX_NEW_OPTIMIZELY=on

You then must set an Optimizely project code in ``.env``::

    # Optimize.ly project code
    OPTIMIZELY_PROJECT_ID=12345

.. note::

    You are not required to set up Optimizely as detailed above. If not configured,
    bedrock will treat the switches as set to ``off``.

To do the equivalent in one of the bedrock apps deployed with `Deis <http://deis.io/>`_, use `deis config <http://docs.deis.io/en/latest/using_deis/config-application/>`_. To continue the example above with a Deis app named ``bedrock-demo-switch``::

    deis config:set SWITCH_FIREFOX_NEW_OPTIMIZELY=on -a bedrock-demo-switch

.. note::

    We have multiple Deis clusters with independent configurations, and recommend using the `DEIS_PROFILE <http://docs.deis.io/en/latest/using_deis/install-client/#multiple-profile-support>`_ environment variable to switch between clusters.



Notes
-----

A shortcut for activating virtual envs in zsh or bash is `. venv/bin/activate`. The dot is the same as `source`.

There's a project called `virtualenvwrapper <http://www.doughellmann.com/docs/virtualenvwrapper/>`_ that provides a better interface for managing/activating virtual envs, so you can use that if you want.
Also if you need help managing various versions of Python on your system, the `pyenv <https://github.com/pyenv/pyenv>`_ project can help.
