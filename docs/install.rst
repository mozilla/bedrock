.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _install:

==================
Installing Bedrock
==================

Installation
------------

These instructions assume you have `git` and `pip` installed. If you don't have `pip` installed, you can install it with `easy_install pip`.

Start by getting the source::

    $ git clone --recursive git://github.com/mozilla/bedrock.git
    $ cd bedrock

**(Make sure you use --recursive so that legal-docs are included)**

You need to create a virtual environment for Python libraries. Skip the first instruction if you already have virtualenv installed::

    $ pip install virtualenv                       # installs virtualenv, skip if already have it
    $ virtualenv -p python2.7 venv                 # create a virtual env in the folder `venv`
    $ source venv/bin/activate                     # activate the virtual env
    $ bin/pipstrap.py                              # securely upgrade pip
    $ pip install -r requirements/dev.txt          # installs dependencies

If you are on OSX and some of the compiled dependencies fails to compile, try explicitly setting the arch flags and try again::

    $ export ARCHFLAGS="-arch i386 -arch x86_64"
    $ pip install -r requirements/dev.txt

If you are on Linux, you will need at least the following packages or their equivalent for your distro:

    python-dev libxslt-dev

Now configure the application to run locally by creating your local settings file::

    $ cp bedrock/settings/local.py-dist bedrock/settings/local.py

You shouldn't need to customize anything in there yet.

Sync the database and all of the external data locally. This gets product-details, security-advisories, credits, release notes, etc::

    $ bin/sync_all

Lastly, you need to have `Node.js <https://nodejs.org/>`_ and
`NPM <https://docs.npmjs.com/getting-started/installing-node>`_ installed. The node
dependencies for running the site can be installed with ``npm``::

    $ npm install --production

But if you'd like to run the JS test suite you'll need everything, which you can get by running
``npm install`` from the root directory of the project.

.. note::

    Bedrock uses `npm-lockdown <https://github.com/mozilla/npm-lockdown>`_ to ensure that Node.js
    packages that get installed are the exact ones we meant (similar to peep.py for python). Refer
    to the `lockdown documentation <https://github.com/mozilla/npm-lockdown#adding-new-modules>`_
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

    $ ./manage.py test

.. note::

    If your local tests run fine, but when you submit a pull-request our Jenkins
    (continuous integration service) instance tells you the tests failed, it could
    be due to the difference in settings between what you have in ``settings/local.py``
    and what Jenkins uses: ``settings/jenkins.py``. You can run tests as close to Jenkins
    as possible by doing the following::

        $ JENKINS_HOME=1 ./manage.py test

    This tells Bedrock to use the jenkins settings. This will require you to have a local
    MySQL database server running and configured correctly, but may help you debug. Alternately
    you can move your ``settings/local.py`` to a backup, copy ``settings/jenkins.py`` to
    ``settings/local.py`` and tweak the DB settings yourself to make it work.

Make it run
-----------

To make the server run, make sure you are inside a virtualenv, and then
run the server::

    $ ./manage.py runserver

If you are not inside a virtualenv, you can activate it by doing::

    $ source venv/bin/activate

If you get the error "NoneType is not iterable", you didn't check out the latest product-details. See the above section for that.

Localization
------------

If you want to install localizations, run the following command::

    $ ./manage.py l10n_update

You can read more details about how to localize content :ref:`here<l10n>`.

Waffle
------

`Waffle
<http://waffle.readthedocs.org/en/latest/index.html>`_ is used to configure behavior and/or features of select pages on bedrock.

Currently, Waffle switches are used to enable/disable Optimizely on the following URLs (Waffle switch names follow in parentheses):

* ``/`` (``mozorg-home-optimizely``)
* ``/firefox/desktop/`` (``firefox-desktop-optimizely``)
* ``/firefox/firstrun/`` (``firefox-firstrun-optimizely``)
* ``/firefox/installer-help/`` (``firefox-installer-help-optimizely``)
* ``/firefox/new/`` (``firefox-new-optimizely``)
* ``/firefox/whatsnew/`` (``firefox-whatsnew-optimizely``)
* ``/plugincheck/`` (``plugincheck-optimizely``)

To work with/test these Waffle/Optimizely switches locally, you must add the switches to your local database. For example::

    ./manage.py switch firefox-new-optimizely on --create

You then must set an Optimizely project code in ``settings/local.py``::

    # Optimize.ly project code
    OPTIMIZELY_PROJECT_ID = 12345

.. note::

    You are not required to set up Waffle & Optimizely as detailed above. If not configured, Waffle will treat the switches as set to ``off``.

For quick reference, to toggle a Waffle switch::

    ./manage.py switch firefox-desktop-optimizely off

And to list all Waffle switches::

    ./manage.py switch -l

Notes
-----

A shortcut for activating virtual envs in zsh or bash is `. venv/bin/activate`. The dot is the same as `source`.

There's a project called `virtualenvwrapper <http://www.doughellmann.com/docs/virtualenvwrapper/>`_ that provides a better interface for managing/activating virtual envs, so you can use that if you want.
