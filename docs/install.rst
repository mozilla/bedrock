.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _install:

==================
Installing Bedrock
==================

Installation
------------

It's a simple `Playdoh
<http://playdoh.readthedocs.org/en/latest/index.html>`_ instance, which is a Django project.

These instructions assume you have `git` and `pip` installed. If you don't have `pip` installed, you can install it with `easy_install pip`.

Start by getting the source::

    $ git clone --recursive git://github.com/mozilla/bedrock.git
    $ cd bedrock

**(Make sure you use --recursive)**

.. Important::

    Because Bedrock uses submodules, it is important not only to use
    ``--recursive`` on the initial clone, but every time you checkout
    a different branch, to update the submodules with::

        git submodule update --init --recursive

    You might want to create a post-checkout hook to do that every time
    automatically, by putting that command in a file
    ``bedrock/.git/hooks/post-checkout``.

You need to create a virtual environment for Python libraries. Skip the first instruction if you already have virtualenv installed::

    $ pip install virtualenv                     # installs virtualenv, skip if already have it
    $ virtualenv venv                            # create a virtual env in the folder `venv`
    $ source venv/bin/activate                   # activate the virtual env
    $ pip install -r requirements/compiled.txt   # installs compiled dependencies
    $ pip install -r requirements/dev.txt        # installs test dependencies

If you are on OSX and some of the compiled dependencies fails to compile, try explicitly setting the arch flags and try again::

    $ export ARCHFLAGS="-arch i386 -arch x86_64"
    $ pip install -r requirements/compiled.txt

If you are on Linux, you will need at least the following packages or their equivalent for your distro:

    python-dev libmysqlclient-dev libxslt-dev

Now configure the application to run locally by creating your local settings file::

    $ cp bedrock/settings/local.py-dist bedrock/settings/local.py

You shouldn't need to customize anything in there yet.

Sync the database and all of the external data locally. This gets product-details, security-advisories, credits, release notes, etc::

    $ bin/sync_all

Lastly, you need to have `Node.js <https://nodejs.org/>`_ installed. The node dependencies for running the site are in the repository, but if you'd like to run the JS test suite you'll need everything, which you can get by running `npm install` from the root directory of the project.

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

.. _with php:

Run it with the whole site
--------------------------

If you need to run the whole site locally, you'll need to **first** set up the
:ref:`PHP side<php>`, and then **also** set up to serve Bedrock from the
same Apache
server at ``/b/``.  That's because the rewrite rules in the
PHP and Apache config assume they can serve requests from Bedrock by
rewriting them internally to have a ``/b/`` on the front of their URLs.

.. IMPORTANT::

    Before continuing, go get the :ref:`PHP side<php>` working.  Then come
    back here.

One way to add Bedrock to your local site, once you have the
:ref:`PHP side<php>` working, is to use runserver to serve Bedrock at port 8000 as
above, then proxy to it from Apache. The whole virtual server config
might end up looking like this::

    <VirtualHost *:80>
        ServerName mozilla.local
        VirtualDocumentRoot "/path/to/mozilla.com"
        RewriteEngine On
        RewriteOptions Inherit
        ProxyPass /b http://localhost:8000
        ProxyPassReverse /b http://localhost:8000
        ProxyPass /media http://localhost:8000/media
        ProxyPassReverse /media http://localhost:8000/media
        Include /path/to/bedrock/etc/httpd/global.conf
    </VirtualHost>

But you might have better success using a real WSGI setup that is closer to
what the real servers use.  The following configuration is simplified
from what the bedrock staging server uses.

Assumptions:

* A Red Hat or Debian-based Linux distribution. (Other distributions might not
  have Apache HTTP Server installed and configured the same way.)
* Apache HTTP Server with php and mod_wsgi
* Subversion mozilla.com checkout at `/path/to/mozilla/mozilla.com`
* Subversion mozilla.org checkout at `/path/to/mozilla/mozilla.com/org` (ideally
  as an SVN external)
* Bedrock checkout at `/path/to/mozilla/bedrock`

Create a local config files for mozilla.com and mozilla.org::

    $ cp /path/to/mozilla.com/includes/config.inc.php-dist /path/to/mozilla.com/includes/config.inc.php
    $ cp /path/to/mozilla.com/org/includes/config.inc.php-dist /path/to/mozilla.com/org/includes/config.inc.php`

Edit ``/etc/hosts`` and add::

    127.0.0.1   mozilla.local

Apache config - create file ``/etc/apache2/sites-available/mozilla.com``::

    # Main site at /, django-bedrock at /b
    <VirtualHost *:80 *:81>
        ServerName mozilla.local
        ServerAdmin user@example.com
        DocumentRoot "/path/to/mozilla/mozilla.com"
        AddType application/x-httpd-php .php .html
        DirectoryIndex index.php index.html
        RewriteEngine On

        <Directory "/path/to/mozilla.com">
            Options MultiViews FollowSymLinks -Indexes
            AllowOverride All
        </Directory>

        RewriteMap org-urls-410 txt:/path/to/mozilla.com/org-urls-410.txt
        RewriteMap org-urls-301 txt:/path/to/mozilla.com/org-urls-301.txt

        # In the path below, update "python2.6" to whatever version of python2 is provided.
        WSGIDaemonProcess bedrock_local python-path=/path/to/bedrock:/path/to/venv-for-bedrock/lib/python2.6/site-packages
        WSGIProcessGroup bedrock_local
        WSGIScriptAlias /b /path/to/bedrock/wsgi/playdoh.wsgi process-group=bedrock_local application-group=bedrock_local

        Alias /media /path/to/bedrock/media
        <Directory /path/to/bedrock/media>
            AllowOverride FileInfo Indexes
        </Directory>

        Include /path/to/bedrock/etc/httpd/global.conf
    </VirtualHost>

Then enable the new site, build the css and js files, and finally
restart apache:

.. code-block:: bash

    sudo a2ensite mozilla.com
    sudo a2enmod expires headers actions
    python manage.py collectstatic
    sudo service apache2 restart

Troubleshooting
...............

If you get Django error pages reporting I/O errors for .css files, it's because
not all the .css files were compiled before starting Apache and Apache does not
have write permissions in the media directories. Running
`python manage.py collectstatic` should solve it.  Remember to run that
command again anytime the css or less files change.

If you change Python files, either restart Apache or touch playdoh.wsgi, so
that the WSGI processes will be restarted and start running the new code.

If you're working on the rewrite rules in ``bedrock/etc/httpd/*.conf``, be
sure to restart Apache after any change. Apache doesn't re-read those files
after it has started.

Localization
------------

If you want to install localizations, just check out the ``locale`` directory::

    git svn clone https://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale
    # or
    svn checkout https://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale

You can use git or svn to checkout the repo. Make sure that it is named ``locale``. If you already have it checked out as ``locales``, just do::

    ln -s locales locale

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

Upgrading
---------

On May 15th, 2013 we upgraded to a newer version of Playdoh_. This brought with it a lot of structural changes to the code.
Here are the required steps to get up and running again with the latest code::

    # get the code
    git pull origin master
    # update the submodules
    git submodule update --init --recursive
    # move your local settings file
    mv settings/local.py bedrock/settings/local.py
    # remove old empty directories
    rm -rf apps
    rm -rf settings
    rm -rf vendor-local/src/django
    rm -rf vendor-local/src/tower
    rm -rf vendor-local/src/jingo-minify

That should do it. If you're not able to run the tests at that point (``python manage.py test``) then there are a couple more things to try.

1. If you have a line like ``from settings.base import *`` in your ``bedrock/settings/local.py`` file, remove it.
2. If you were setting a logging level in your ``bedrock/settings/local.py`` file, you may now need to explicitly need to import it (``import logging``).

Otherwise please pop into our IRC channel (``#www`` on ``irc.mozilla.org``) and we'll be happy to help.

Notes
-----

A shortcut for activating virtual envs in zsh is `. venv/bin/activate`. The dot is the same as `source`.

There's a project called `virtualenvwrapper <http://www.doughellmann.com/docs/virtualenvwrapper/>`_ that provides a better interface for managing/activating virtual envs, so you can use that if you want.

