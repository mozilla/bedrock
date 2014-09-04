.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _install:

==================
Quickstart
==================

You can develop and test bedrock without installing anything locally by using
Cloud9_, which provides a complete development environment via your browser,
including unlimited free public workspaces [#]_, which is great for open source
projects. Each workspace includes root_ access to an Ubuntu_ Docker_ container,
which you can install bedrock and all its depdencies into with the following
steps:

1. Fork `bedrock <https://github.com/mozilla/bedrock/>`_ on github
2. Sign up or sign in to Cloud9_ with your github account [#]_
3. Create a new workspace from your fork using the "Clone from URL"
   option with a URL in the format ``git@github.com:mozilla/bedrock.git`` but 
   with your username instead of ``mozilla``
4. Once your workspace is ready, click the "Start Editing" button
5. In the bash shell, run the command ``bin/install-c9``

Once the ``install-c9`` script completes, you can use the ``bin/runserver-c9``
script to launch the django development server, which will be accessible on a
public URL similar to ``http://bedrock-c9-username.c9.io``


.. _Cloud9: https://c9.io
.. _root: https://help.ubuntu.com/community/RootSudo
.. _Ubuntu: http://www.ubuntu.com/
.. _Docker: https://www.docker.com/
.. [#] Public means everything in the workspace is world readable; you can also
       grant write access to specific cloud9 users and collaboratively edit code
       in your workspace in real time.
.. [#] Github account integration is optional; if you do not wish to give cloud9
       access to push to any repo your github account has access, you may wish
       to use a `deploy key 
       <https://developer.github.com/guides/managing-deploy-keys/#deploy-keys>`_
       or a `machine user account
       <https://developer.github.com/guides/managing-deploy-keys/#machine-users>`_.