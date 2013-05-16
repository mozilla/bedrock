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

These instructions assume you have `git` and `pip` installed. If you don't have `pip` install, you can install it with `easy_install pip`.

Start by getting the source::

    $ git clone --recursive git://github.com/mozilla/bedrock.git
    $ cd bedrock

**(Make sure you use --recursive)**

You need to create a virtual environment for Python libraries. Skip the first instruction if you already have virtualenv installed::

    $ pip install virtualenv                     # installs virtualenv, skip if already have it
    $ virtualenv venv                            # create a virtual env in the folder `venv`
    $ source venv/bin/activate                   # activate the virtual env
    $ pip install -r requirements/compiled.txt   # installs compiled dependencies

If you are on OSX and some of the compiled dependencies fails to compile, try explicitly setting the arch flags and try again::

    $ export ARCHFLAGS="-arch i386 -arch x86_64"
    $ pip install -r requirements/compiled.txt

Now configure the application to run locally by creating your local settings file::

    $ cp bedrock/settings/local.py-dist bedrock/settings/local.py

You shouldn't need customize anything in there yet.

Check out the latest product-details::

    $ ./manage.py update_product_details

Lastly, you need to install `node` and the `less` package. Soon you won't need this for local development but currently it compiles the LESS CSS code on the server-side::

    $ npm -g install less

You don't have to use npm to install less; feel free to install it however you want.

Add the path to the LESS compiler in you `local.py` config file in the `settings` folder. It is most likely `/usr/local/bin/lessc`, so add the following line::

    LESS_BIN = '/usr/local/bin/lessc'

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

If you want to install localizations, just check out the ``locale`` directory::

    git svn clone https://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale
    # or
    svn checkout https://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale

You can use git or svn to checkout the repo. Make sure that it is named ``locale``. If you already have it checked out as ``locales``, just do::

    ln -s locales locale

You can read more details about how to localize content :ref:`here<l10n>`.

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

