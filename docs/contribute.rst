.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _contribute:

=================
How to contribute
=================

Git workflow
------------
When you want to start contributing, you should create a branch from master.
This allows you to work on different project at the same time::

    git checkout master
    git checkout -b topic-branch

To keep your branch up-to-date, assuming the mozilla repository is the remote
called mozilla::

    git fetch mozilla
    git checkout master
    git merge mozilla/master
    git checkout topic-branch
    git rebase master

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
  master.

If you're asked to change your commit message, you can use these commands:

.. code-block:: bash

    git commit --amend
    # -f is doing a force push because you modified the history
    git push -f my-remote topic-branch

Submitting your work
--------------------
In general, you should submit your work with a pull request to master. If you
are working with other people or you want to put your work on a demo server,
then you should be working on a common topic branch.

Once your code has been positively reviewed, it will be deployed shortly after.
So if you want feedback on your code but it's not ready to be deployed, you
should note it in the pull request.

Getting a new Bedrock page online
---------------------------------
On our servers, Bedrock pages are accessible behind the ``/b/`` prefix. So if a
page is accessible at this URL locally::

    http://localhost:8000/foo/bar

then on our servers, it will be accessible at::

    http://www.mozilla.org/b/foo/bar

When you're ready to make a page available to everyone, we need to remove that
/b/ prefix. We handle that with Apache RewriteRule. Apache config files that
are included into the server's config are in the bedrock code base in the
``etc/httpd`` directory. In there you'll find a file for each of the environments.
You'll almost always want to use ``global.conf`` unless you have a great reason
for only wanting the config to stay on one of the non-production environments.

In that file you'll add a RewriteRule that looks like the following:

    .. code-block:: apache

        # bug 123456
        RewriteRule ^/(\w{2,3}(?:-\w{2}(?:-mac)?)?/)?foo/bar(/?)$ /b/$1foo/bar$2 [PT]

This is a lot simpler than it looks. The first large capture is just what's necessary
to catch every possible locale code. After that it's just your new path. Always capture
the trailing slash as we want that to hit django so it will redirect.

.. note::

    It's best if the RewriteRule required for a new page is in the original pull request.
    This allows it to flow through the push process with the code and for it to go live
    as soon as it's on the production server. It's also one less review and pull-request for
    us to manage.

Server architecture
-------------------
**Demos**

- *URLs:* http://www-demo1.allizom.org/ , http://www-demo2.allizom.org/ and
  http://www-demo3.allizom.org/
- *PHP SVN branch:* trunk, updated every 10 minutes
- *Bedrock locale SVN branch:* trunk, updated every 10 minutes
- *Bedrock Git branch:* any branch we want, manually updated

**Dev**

- *URL:* http://www-dev.allizom.org/
- *PHP SVN branch:* trunk, updated every 10 minutes
- *Bedrock locale SVN branch:* trunk, updated every 10 minutes
- *Bedrock Git branch:* master, updated every 10 minutes

**Stage**

- *URL:* http://www.allizom.org/
- *PHP SVN branch:* tags/stage, updated every 10 minutes
- *Bedrock locale SVN branch:* trunk, updated every 10 minutes
- *Bedrock Git branch:* master, updated manually

**Production**

- *URL:* http://www.mozilla.org/
- *PHP SVN branch:* tags/production, updated every 10 minutes
- *Bedrock locale SVN branch:* trunk, updated every 10 minutes
- *Bedrock Git branch:* master, updated manually

We use Chief for the manual deploys. You can check the currently deployed git
commit by checking https://www.mozilla.org/media/revision.txt.

If you want to know more and you have an LDAP account, you can check the
`IT documentation`_.

Pushing to production
---------------------
We're doing pushes as soon as new work is ready to go out.

After doing a push, the "pusher" needs to update the bugs that have been pushed
with a quick message stating that the code was deployed. Chief will send on
#www a URL with all commits that have been deployed.

If you'd like to see the commits that will be deployed before the push run the
following command:

    .. code-block:: bash

        ./bin/open-compare.py

This will discover the currently deployed git hash, and open a compare URL at github
to the latest master. Look at ``open-compare.py -h`` for more options.

.. _Git book: http://git-scm.com/book
.. _how to write good git commit messages: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
.. _IT documentation: https://mana.mozilla.org/wiki/pages/viewpage.action?pageId=1802733
.. _IT bug: https://bugzilla.mozilla.org/enter_bug.cgi?product=mozilla.org&format=itrequest
