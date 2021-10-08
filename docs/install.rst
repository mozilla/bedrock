.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _install:

==================
Installing Bedrock
==================

Installation Methods
====================

There are two primary methods of installing bedrock: Docker and Local. Whichever you choose you'll start by getting the source

.. code-block:: bash

    $ git clone git://github.com/mozilla/bedrock.git

.. code-block:: bash

    $ cd bedrock

After these basic steps you can choose your install method below. Docker is the easiest and recommended way, but local is also possible
and may be preferred by people for various reasons.

You should also install our git pre-commit hooks. Our setup uses the `pre-commit <https://pre-commit.com/>`_
framework. Install the framework using the instructions on their site depending on your platform, then run
``pre-commit install``. After that it will check your Python, JS, and CSS files before you commit to save you
time waiting for the tests to run in our CI before noticing a linting error.

Docker Installation
-------------------

.. note::

    This method assumes you have `Docker installed for your platform <https://www.docker.com/community-edition#/download>`_.
    If not please do that now or skip to the ``Local Installation`` section.

This is the simplest way to get started developing for bedrock. If you're on Linux or Mac (and possibly Windows 10 with the
Linux subsystem) you can run a script that will pull our production and development docker images and start them::

    $ make clean run

.. note::

    You can start the server any other time with::

        $ make run

You should see a number of things happening, but when it's done it will output something saying that the server is running
at `localhost:8000 <http://localhost:8000/>`_. Go to that URL in a browser and you should see the mozilla.org home page.
In this mode the site will refresh itself when you make changes to any template or media file. Simply open your editor of
choice and modify things and you should see those changes reflected in your browser.

.. note::

    It's a good idea to run ``make pull`` from time to time. This will pull down the latest Docker images from our repository
    ensuring that you have the latest dependencies installed among other things. If you see any strange errors after a
    ``git pull`` then ``make pull`` is a good thing to try for a quick fix.

If you don't have or want to use Make you can call the docker and compose commands directly

.. code-block:: bash

    $ docker-compose pull

.. code-block:: bash

    $ [[ ! -f .env ]] && cp .env-dist .env

Then starting it all is simply

.. code-block:: bash

    $ docker-compose up app assets

All of this is handled by the ``Makefile`` script and called by Make if you follow the above directions.
You **DO NOT** need to do both.

These directions pull and use the pre-built images that our deployment process has pushed to the
`Docker Hub <https://hub.docker.com/u/mozorg/>`_. If you need to add or change any dependencies for Python
or Node then you'll need to build new images for local testing. You can do this by updating the requirements
files and/or package.json file then simply running::

    $ make build

**Asset bundles**

If you make a change to ``media/static-bundles.json``, you'll need to restart Docker.

.. note::

    Sometimes stopping Docker doesn't actually kill the images. To be safe, after stopping docker, run
    ``docker ps`` to ensure the containers were actually stopped. If they have not been stopped, you can force
    them by running ``docker-compose kill`` to stop all containers, or ``docker kill <container_name>`` to stop
    a single container, e.g. ``docker kill bedrock_app_1``.

Local Installation
------------------

These instructions assume you have Python 3.6+, pip, and NodeJS installed. If you don't have `pip` installed
(you probably do) you can install it with the instructions in `the pip docs <https://pip.pypa.io/en/stable/installing/>`_.

You need to create a virtual environment for Python libraries:

1. Create a virtual env in the folder `venv` ::

    $ python3 -m venv venv             

2. Activate the virtual env. On Windows, run: venv\Scripts\activate.bat ::    

    $ source venv/bin/activate             

3. Securely upgrade pip ::

    $ pip install --upgrade pip          

4. Installs dependencies ::

    $ pip install -r requirements/dev.txt           


If you are on OSX and some of the compiled dependencies fails to compile, try explicitly setting the arch flags and try again

.. code-block:: bash

    $ export ARCHFLAGS="-arch i386 -arch x86_64"

.. code-block:: bash

    $ pip install -r requirements/dev.txt

If you are on Linux, you will need at least the following packages or their equivalent for your distro::

    $ python3-dev libxslt-dev

Sync the database and all of the external data locally. This gets product-details, security-advisories,
credits, release notes, localizations, legal-docs etc::

    $ bin/bootstrap.sh

Next, you need to have `Node.js <https://nodejs.org/>`_ and `Yarn <https://yarnpkg.com/>`_ installed.
The node dependencies for running the site can be installed with ``yarn``::

    $ yarn

.. note::

    Bedrock uses yarn to ensure that Node.js
    packages that get installed are the exact ones we meant (similar to pip hash checking mode for python). Refer
    to the `yarn documentation <https://yarnpkg.com/en/docs/yarn-workflow>`_
    for adding or upgrading Node.js dependencies.

.. _run-python-tests:

Run the tests
=============

Now that we have everything installed, let's make sure all of our tests pass.
This will be important during development so that you can easily know when
you've broken something with a change.

Docker
------

We manage our local docker environment with docker-compose and Make. All you need to do here is run::

    $ make test

If you don't have Make you can simply run ``docker-compose run test``.

If you'd like to run only a subset of the tests or only one of the test commands you can accomplish
that with a command like the following::

    $ docker-compose run test py.test bedrock/firefox

This example will run only the unit tests for the ``firefox`` app in bedrock. You can substitute
``py.test bedrock/firefox`` with most any shell command you'd like and it will run in the Docker
container and show you the output. You can also just run ``bash`` to get an interactive shell in
the container which you can then use to run any commands you'd like and inspect the file system::

    $ docker-compose run test bash

Local
-----

From the local install instructions above you should still have your virtualenv
activated, so running the tests is as simple as::

    $ py.test lib bedrock

To test a single app, specify the app by name in the command above. e.g.::

    $ py.test bedrock/firefox

.. note::

    If your local tests run fine, but when you submit a pull-request the tests fail in
    `CircleCI <https://circleci.com/gh/mozilla/bedrock>`_, it could be due to the
    difference in settings between what you have in ``.env``
    and what CircleCI uses: ``docker/envfiles/demo.env``. You can run tests as close to Circle
    as possible by moving your ``.env`` file to another name (e.g. ``.env-backup``), then
    copying ``docker/envfiles/demo.env`` to ``.env``, and running tests again.

Make it run
===========

Docker
------

You can simply run the ``make run`` script mentioned above, or use docker-compose directly::

    $ docker-compose up app assets

Local
-----

To make the server run, make sure your virtualenv is activated, and then
run the server::

    $ npm start

If you are not inside a virtualenv, you can activate it by doing::

    $ source venv/bin/activate

Browsersync
-----------

Both the Docker and Local methods of running the site use `Browsersync <https://www.browsersync.io/>`_ to serve
the development static-assets (CSS, JS, etc.) as well as refresh the browser tab for you when you change files. The
refreshing of the page works by injecting a small JS snippet into the page that listens to the browsersync service
and will refresh the page when it receives a signal. It also injects a script that shows a small notification in the
top-right corner of the page to inform you that a refresh is happening and when the page connects to or is disconnected
from the browsersync service. We've not seen issues with this, but since it is modifying the page it is possible that this
could conflict with something on the page itself. Please let us know if you suspect this is happening for you. This
notification can be disabled in the browsersync options in ``webpack.config.js`` by setting ``notify: false`` in the
``BrowserSyncPlugin`` config.

Prod Mode
---------

There are certain things about the site that behave differently when running locally in dev mode using Django's development
server than they do when running in the way it runs in production. Static assets that work fine locally can be a problem
in production if referenced improperly, and the normal error pages won't work unless ``DEBUG=False`` and doing that will
make the site throw errors since the Django server doesn't have access to all of the built static assets. So we have a couple
of extra Docker commands (via make) that you can use to run the site locally in a more prod-like way.

First you should ensure that your ``.env`` file is setup the way you need. This usually means adding ``DEBUG=False``
and ``DEV=False``, though you may want ``DEV=True`` if you want the site to act more like www-dev.allizom.org in that all
feature switches are ``On`` and all locales are active for every page. After that you can run the following:

.. code-block:: bash

    $ make run-prod

This will run the latest bedrock image using your local bedrock files and templates, but not your local static assets. If you
need an updated image just run ``make pull``.

If you need to include the changes you've made to your local static files (images, css, js, etc.) then you have to build the
image first:

.. code-block:: bash

    $ make build-prod run-prod

Documentation
-------------

This is a great place for coders and non-coders alike to contribute! Please note most of the documentation is currently in `reStructuredText <https://bashtage.github.io/sphinx-material/basics.html>`_ but we also support `Markdown <https://www.markdownguide.org/>`_ files.

If you see a typo or similarly small change, you can use the "Edit in GitHub" link to propose a fix through GitHub. Note: you will not see your change directly committed to the master branch. You will commit the change to a separate branch so it can be reviewed by a staff member before merging to master.

If you want to make a bigger change or `find a Documentation issue on the repo <https://github.com/mozilla/bedrock/labels/Documentation>`_, it is best to edit and preview locally before submitting a pull request. You can do this with Docker or Local installations. Run the commands from your root folder. They will build documentation and start a live server to auto-update any changes you make to a documentation file.

Docker: 

.. code-block:: bash

    $ make docs

Local:

.. code-block:: bash

    $ pip install -r requirements/docs.txt

.. code-block:: bash

    $ make livedocs


Localization
============

Localization (or L10n) files were fetched by the `bootstrap.sh` command your ran earlier and are
included in the docker images. If you need to update them or switch to a different repo or branch
after changing settings you can run the following command::

    $ ./manage.py l10n_update

You can read more details about how to localize content :ref:`here <l10n>`.

Feature Flipping (aka Switches)
===============================

Environment variables are used to configure behavior and/or features of select pages on bedrock
via a template helper function called ``switch()``. It will take whatever name you pass to it
(must be only numbers, letters, and dashes), convert it to uppercase, convert dashes to underscores,
and lookup that name in the environment. For example: ``switch('the-dude')`` would look for the
environment variable ``SWITCH_THE_DUDE``. If the value of that variable is any of "on", "true", "1", or
"yes", then it will be considered "on", otherwise it will be "off".

You can also supply a list of locale codes that will be the only ones for which the switch is active.
If the page is viewed in any other locale the switch will always return ``False``, even in ``DEV``
mode. This list can also include a "Locale Group", which is all locales with a common prefix
(e.g. "en-US, en-GB" or "zh-CN, zh-TW"). You specify these with just the prefix. So if you
used ``switch('the-dude', ['en', 'de'])`` in a template, the switch would be active for German and
any English locale the site supports.

You may also use these switches in Python in ``views.py`` files (though not with locale support).
For example::

    from bedrock.base.waffle import switch

    def home_view(request):
        title = 'Staging Home' if switch('staging-site') else 'Prod Home'
        ...

Testing
-------

If the environment variable ``DEV`` is set to a "true" value, then all switches will be considered "on" unless they are
explicitly "off" in the environment. ``DEV`` defaults to "true" in local development and demo servers.

To test switches locally:

#. Set ``DEV=False`` in your ``.env`` file.
#. Enable the switch in your ``.env`` file.
#. Restart your web server.

To configure switches for a demo branch. Follow the `configuration instructions here <http://bedrock.readthedocs.io/en/latest/pipeline.html#configuration>`_.

Traffic Cop
-----------

Currently, these switches are used to enable/disable `Traffic Cop <https://github.com/mozilla/trafficcop/>`_ experiments
on many pages of the site. We only add the Traffic Cop JavaScript snippet to a page when there is an active test. You
can see the current state of these switches and other configuration values in our `configuration
repo <https://mozmeao.github.io/www-config/configs/>`_.

To work with/test these experiment switches locally, you must add the switches to your local environment. For example::

    # to switch on firstrun-copy-experiment you'd add the following to your ``.env`` file
    SWITCH_FIRSTRUN_COPY_EXPERIMENT=on

To do the equivalent in one of the bedrock apps see the `www-config <https://mozmeao.github.io/www-config/>`_ documentation.

Notes
-----

A shortcut for activating virtual envs in zsh or bash is `. venv/bin/activate`. The dot is the same as `source`.

There's a project called `pew <https://pypi.org/project/pew/>`_ that provides a better interface for managing/activating virtual envs, so you can use that if you want.
Also if you need help managing various versions of Python on your system, the `pyenv <https://github.com/pyenv/pyenv>`_ project can help.
