==================
Docker Development
==================

First, install `Docker https://docs.docker.com/installation/`_ and `Compose https://docs.docker.com/compose/install/`_. Then clone bedrock locally with::

    $ git clone --recursive git://github.com/mozilla/bedrock.git
    $ cd bedrock

**(Make sure you use --recursive so that legal-docs are included)**

To work with locales other than en-US, you will also need to clone the locales from their subversion repository::

    $ git svn clone https://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale
    # or
    $ svn checkout https://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale

OS X
----

Launch a dev server container in a boot2docker VM::

    $ bin/b2d-dev

Open a browser window to the dev server you just launched::

    $ bin/b2d-open

To run a bash shell inside a b2d container::

    $ bin/b2d-bash

If a b2d container has already been lauched it will ``exec`` the process inside the running container. Otherwise it will launch a new container to run bash. Once you're interacting with a bash shell inside the container you can use other commands such as ``./manage.py test`` and ``./manage.py shell_plus`` as described elsewhere in the documentation.

If you want to use grunt to compile less to css with live reloading in the browser,
set ``USE_GRUNT_LIVERELOAD`` to ``True`` in ``bedrock/settings/local.py``,
and use the following to launch ``grunt`` in a container::

    $ bin/b2d-grunt

If you make or pull a change to the dependencies, such as in ``requirements/dev.txt`` or ``package.json``, you will need to rebuild your local dev image::

    $ bin/b2d-build
  
Linux
-----

Build the dev docker image::

    $ docker-compose build dev

If you make or pull a change to the dependencies, such as in ``requirements/dev.txt`` or ``package.json``, you will need to rebuild your local dev image with the command above.

Create a local settings file::

    $ cp bedrock/settings/local.py-dist bedrock/settings/local.py

Run the ``bin/sync_all`` script inside a dev docker container::

    $ docker-compose run dev bin/sync_all

Launch the development server::

    $ docker-compose up dev

Then visit http://localhost:8000 in your browser.

To run a bash shell in a new container::

    $ docker-compose run dev bash

To run a bash shell in an already running container (after running ``docker-compose up dev`` in a separate shell)::

    $ docker exec -it bedrock_dev_1 bash

Once running a bash shell inside a container, you can use commands like ``./manage.py test`` and ``./manage.py shell_plus`` as described elsewhere in the docs. You can also ``run`` or ``exec`` other commands directly, without the intermediate bash shell if you prefer. For example, to run backend tests in a new container::

    $ docker-compose run dev ./manage.py tests

If you want to use grunt to compile less to css with live reloading in the browser,
set ``USE_GRUNT_LIVERELOAD`` to ``True`` in ``bedrock/settings/local.py``,
and run the following::

    $ docker-compose run dev bin/grunter

Frontend tests are not yet working in the docker environment. This will be addressed in the near future.
