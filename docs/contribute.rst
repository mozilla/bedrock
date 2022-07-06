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

    $ git checkout main

.. code-block:: bash

    $ git checkout -b topic-branch

To keep your branch up-to-date, assuming the mozilla repository is the remote
called mozilla:

.. code-block:: bash

    $ git fetch mozilla

.. code-block:: bash

    $ git checkout main

.. code-block:: bash

    $ git merge mozilla/main

.. code-block:: bash

    $ git checkout topic-branch

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


Server architecture
-------------------
**Demos**

- *URLs:*
   - http://www-demo1.allizom.org/
   - http://www-demo2.allizom.org/
   - http://www-demo3.allizom.org/
   - http://www-demo4.allizom.org/
   - http://www-demo5.allizom.org/
- *Bedrock locales:* dev repo
- *Bedrock Git branch:* ``demo/1``, ``demo/2``, etc.

These demos can be deployed by pushing a branch to one of the `demo/*` branches
of the `mozilla/bedrock` repo. The `Github action`_ will then deploy the
demo to Heroku.

.. _Github action: https://github.com/mozilla/bedrock/blob/main/.github/workflows/demo_deploy.yml

.. code-block:: bash

  $ git push -f mozilla my-demo-branch:demo/1

**On-demand demos**

- *URLs:* Demo instances can also be spun up on-demand by pushing a branch to the mozilla
  bedrock repo that matches a specific naming convention (the branch name must start with
  ``demo/``). Jenkins will then automate spinning up a demo instance based on that
  branch. For example, pushing a branch named ``demo/feature`` would create a demo
  instance with the following URL: ``https://bedrock-demo-feature.oregon-b.moz.works/``
- *Bedrock locales:* dev repo
- *Bedrock Git branch:* any branch named starting with ``demo/``

.. Note::

    Deployed demo instances are not yet automatically cleaned up when branches are deleted,
    so to avoid lots of instances piling up it is currently recommended to try and limit
    a single demo instance per developer, reusing a branch such as `demo/<your_username>`.

**Dev**

- *URL:* http://www-dev.allizom.org/
- *Bedrock locales:* dev repo
- *Bedrock Git branch:* main, deployed on git push

**Stage**

- *URL:* http://www.allizom.org/
- *Bedrock locales:* prod repo
- *Bedrock Git branch:* prod, deployed on git push with date-tag

**Production**

- *URL:* http://www.mozilla.org/
- *Bedrock locales:* prod repo
- *Bedrock Git branch:* prod, deployed on git push with date-tag

You can check the currently deployed git commit by checking https://www.mozilla.org/revision.txt.

Pushing to production
---------------------
We're doing pushes as soon as new work is ready to go out.

After doing a push, those who are responsible for implementing changes need to update
the bugs that have been pushed with a quick message stating that the code was deployed.

If you'd like to see the commits that will be deployed before the push run the
following command:

.. code-block:: bash

    $ ./bin/open-compare.py

This will discover the currently deployed git hash, and open a compare URL at github
to the latest main. Look at ``open-compare.py -h`` for more options.

We automate pushing to production via tagged commits (see :ref:`tagged-commit`)

.. _Git book: http://git-scm.com/book
.. _how to write good git commit messages: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
.. _Draft PR: https://github.blog/2019-02-14-introducing-draft-pull-requests/
