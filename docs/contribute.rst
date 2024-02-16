.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _contribute:

=================
How to contribute
=================

Before diving into code it might be worth reading through the
:ref:`Developing on Bedrock<coding>` documentation, which contains
useful information and links to our coding guidelines for Python, Django,
JavaScript and CSS.

Git workflow
------------
When you want to start contributing, you should create a branch from main.
This allows you to work on different project at the same time:

.. code-block:: bash

    $ git switch main

.. code-block:: bash

    $ git switch -c topic-branch

To keep your branch up-to-date, assuming the mozilla repository is the remote
called mozilla:

.. code-block:: bash

    $ git switch main

.. code-block:: bash

    $ git pull --ff-only

More on `Why you should use --ff-only`_. To make this the default update your
Git config as described in the article.

.. code-block:: bash

    $ git switch topic-branch

.. code-block:: bash

    $ git rebase main

If you need more Git expertise, a good resource is the `Git book`_.

Once you're done with your changes, you'll need to describe those changes in
the commit message.

Git commit messages
-------------------
Commit messages are important when you need to understand why something was
done.

* First, learn `how to write good git commit messages`_.
* All commit messages must include a bug number. You can put the bug number on
  any line, not only the first one.
* If you use the syntax ``bug xxx``, Github will reference the commit into
  Bugzilla. With ``fix bug xxx``, it will even close the bug once it goes into
  main.

If you're asked to change your commit message, you can use these commands:

.. code-block:: bash

  $ git commit --amend

-f is doing a force push because you modified the history

.. code-block:: bash

  $ git push -f my-remote topic-branch

Submitting your work
--------------------
In general, you should submit your work with a pull request to main. If you
are working with other people or you want to put your work on a demo server,
then you should be working on a common topic branch.

Once your code has been positively reviewed, it will be deployed shortly after.
So if you want feedback on your code but it's not ready to be deployed, you
should note it in the pull request, or use a `Draft PR`_. Also make use of
an appropriate label, such as ``Do Not Merge``.

Squashing your commits
----------------------

Should your pull request contain more than one commit, sometimes we may ask you
to squash them into a single commit before merging. You can do this with `git rebase`.

As an example, let's say your pull request contains two commits. To squash them
into a single commit, you can follow these instructions::

  $ git rebase -i HEAD~2

You will then get an editor with your two commits listed. Change the second
commit from `pick` to `fixup`, then save and close. You should then be able to
verify that you only have one commit now with `git log`.

To push to GitHub again, because you "altered the history" of the repo by merging
the two commits into one, you'll have to `git push -f` instead of just `git push`.


Deploying your code
-------------------

These are the websites that Bedrock is usually deployed to as part of development.

Demo sites
``````````

Bedrock as a platform can run in two modes: Mozorg Mode (for content that will
appear on mozilla.org) and Pocket Mode (for content that will end up on getpocket.com).

To support this, we have two separate sets of URLs we use for demos. To get code up to
one of those URLs, push it to the specified branch on ``github.com/mozilla/bedrock``:

- *Mozorg:*
   - Branch ``mozorg-demo-1`` -> https://www-demo1.allizom.org/
   - Branch ``mozorg-demo-2`` -> https://www-demo2.allizom.org/
   - Branch ``mozorg-demo-3`` -> https://www-demo3.allizom.org/
   - Branch ``mozorg-demo-4`` -> https://www-demo4.allizom.org/
   - Branch ``mozorg-demo-5`` -> https://www-demo5.allizom.org/
   - Branch ``mozorg-demo-6`` -> https://www-demo6.allizom.org/
   - Branch ``mozorg-demo-7`` -> https://www-demo7.allizom.org/
   - Branch ``mozorg-demo-8`` -> https://www-demo8.allizom.org/
   - Branch ``mozorg-demo-9`` -> https://www-demo9.allizom.org/

- *Pocket:*
   - Branch ``pocket-demo-1`` -> https://www-demo1.tekcopteg.com/
   - Branch ``pocket-demo-2`` -> https://www-demo2.tekcopteg.com/
   - Branch ``pocket-demo-3`` -> https://www-demo3.tekcopteg.com/
   - Branch ``pocket-demo-4`` -> https://www-demo4.tekcopteg.com/
   - Branch ``pocket-demo-5`` -> https://www-demo5.tekcopteg.com/

For example, for Mozorg:

.. code-block:: bash

  $ git push -f mozilla my-demo-branch:mozorg-demo-2

Or for Pocket:

.. code-block:: bash

  $ git push -f mozilla my-demo-branch:pocket-demo-1


**Deployment notification and logs**

At the moment, there is no way to view logs for the deployment unless you have
access to Google Cloud Platform.

If you *do* have access, the Cloud Build dashboard shows the latest builds,
and Cloud Run will link off to the relevant logs.

There are Mozilla Slack notifications in ``#www-notify`` that show the
status of demo builds. (Work is ticketed to make those notifications richer in data.)

**Env vars**

Rather than tweak env vars via a web UI, they are set in config files.
Both Mozorg and Pocket mode have specific demo-use-only env var files, which
are only used by our GCP demo setup. They are:

* ``bedrock/gcp/bedrock-demos/cloudrun/mozorg-demo.env.yaml``
* ``bedrock/gcp/bedrock-demos/cloudrun/pocket-demo.env.yaml``

If you need to set/add/remove an env var, you can edit the relevant file on
your feature branch, commit it and push it along with the rest of
the code, as above. There is a small risk of clashes, but these can be best
avoided if you keep up to date with ``bedrock/main`` and can be resolved easily.

**Secret values**

*Remember that the env vars files are public because they are in the Bedrock
codebase, so sensitive values should not be added there, even temporarily.*

If you need to add a secret value, this currently needs to be added at the GCP
level by someone with appropriate permissions to edit and apply the Terraform
configuration, and to edit the trigger YAML spec to pass through the new secret.
Currently Web-SRE and the backend team have appropriate GCP
access and adding a secret is relatively quick. (We can make this easier in
the future if there's sufficient need, of course.)

.. note::

  **Always-on vs auto-sleep demo servers**

  The demo servers are on GCP Cloud Run, and by default they will be turned off if
  there is no traffic for 15 minutes. After this time, the demo app will be woken
  up if it receives a request.

  Normally, a 'cold start' will not be a problem. However, if the branch you are
  demoing does things that alter the database (i.e contains migrations), then you
  may find the restarted demo app crashes because the new migrations have not been
  applied after a cold start.

  The best current way to avoid that happening is:

  * In your branch's demo-env-vars YAML file, set ``LOCAL_DB_UPDATE=True`` so
    that the Dev DB is not pulled down to the demo app
  * Ask one of the backend team to set the Demo app to always be awake by setting
    'Minimum instances' to 1 for the relevant Cloud Run service and restarting
    it. The app will always be on and will not sleep, so won't need a cold start.
    Once you have completed the feature work, please ask the backenders to
    restore the default sleepy behaviour. As an example with ``mozorg-demo-1``:

      * To make it always-on: ``gcloud run services update mozorg-demo-1 --min-instances 1``
      * To revert it to auto-sleeping: ``gcloud run services update mozorg-demo-1 --min-instances 0``

  (We'll try to make this a self-serve thing as soon as we can).

DEPRECATED: Heroku Demo Servers
...............................

Demos are now powered by Google Cloud Platform (GCP), and no longer by Heroku.

However, the `Github Action`_ we used to push code to Heroku may still be enabled.
Pushing a branch to one of the `demo/*` branches of the `mozilla/bedrock` repo
will trigger this. However, note that URLs that historically used to point to
Heroku will be pointed to the new GCP demos services instead, so you will have
to look at Heroku's web UI to see what the URL of the relevant Heroku app is.

.. _Github action: https://github.com/mozilla/bedrock/blob/main/.github/workflows/demo_deploy.yml

To push to launch a demo on Heroku:

.. code-block:: bash

  $ git push -f mozilla my-demo-branch:demo/1


Pushing to production
`````````````````````

We're doing pushes as soon as new work is ready to go out.

Code flows automatically to Dev, amd manually to Stage and to Production. See :ref:`pipeline` for details.

After doing a push, those who are responsible for implementing changes need to update
the bugs that have been pushed with a quick message stating that the code was deployed.

If you'd like to see the commits that will be deployed before the push run the
following command:

.. code-block:: bash

    $ ./bin/open-compare.py

This will discover the currently deployed git hash, and open a compare URL at github
to the latest main. Look at ``open-compare.py -h`` for more options.

We automate pushing to production via tagged commits (see :ref:`pipeline`)

.. _Git book: http://git-scm.com/book
.. _how to write good git commit messages: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
.. _Draft PR: https://github.blog/2019-02-14-introducing-draft-pull-requests/
.. _Why you should use --ff-only: https://blog.sffc.xyz/post/185195398930/why-you-should-use-git-pull-ff-only-git-is-a
