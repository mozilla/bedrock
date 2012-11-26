.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _php:

============================================
 Installing and Learning About the PHP Site
============================================

The previous version of mozilla.org was written in PHP. The PHP
codebase still serves some of the mozilla.org pages because we haven't
migrated everything over. A request runs through the following stack:

* If the page exists in Bedrock, serve from Bedrock
* If the page exists in the PHP site, serve from PHP
* Else, serve a 404 page

History
=======

The PHP site has a long history and as a result, is a little quirky.
If you are looking to work on the site and/or set it up locally, this
page will be helpful to you.

mozilla.org, mozilla.com, and thunderbird used to be completely
separate sites with different PHP codebases. In 2011 these sites were
merged into one site.

The merge is purely for aesthetics though. In the PHP side of
mozilla.org, a few different PHP codebases coexist beside each other,
and a combination of Apache and PHP magic bind them all together (one
site to rule them all, or something like that).

Installing
==========

.. _mozilla-com:

mozilla.com
-----------

If you want to just work on the mozilla.com codebase (currently served
at mozilla.org/firefox), follow these steps. You will only get the
product pages. See :ref:`mozilla.org <mozilla-org>` for instructions
on installing the org side of the site. For more details on why
several codebases run the site, see :ref:`How a Request is Handled <merge>`.

.. note:: This assumes you are using Apache. Windows might have
          different steps, please contact us if you need help.

1. Install it with these commands:

::

  svn co https://svn.mozilla.org/projects/mozilla.com/trunk mozilla.com
  cd mozilla.com/includes
  cp config.inc.php-dist config.inc.php

2. Open /includes/config.inc.php and set the `server_name` to "mozilla.local" (or whatever you will use) and `file_root` to the site's path on the filesystem.
3. Set up `mozilla.local` to resolve to localhost. This is different for each OS, but a quick way on Linux/OS X is to add an entry to /etc/hosts.
4. Configure Apache to allow the site to run with a Directory and VirtualHost directive:

::

  <Directory /path/to/mozilla.com>
          Options Includes FollowSymLinks MultiViews Indexes
          AllowOverride All
          Order Deny,Allow
          Allow from all
  </Directory>

  <VirtualHost *:80>
      ServerName mozilla.local
      VirtualDocumentRoot "/path/to/mozilla.com"
  </VirtualHost>

Make sure to replace ServerName and /path/to/ to the correct values.

5. You *might* need to set the DocumentRoot to the site if you can't load any CSS files. We are looking to fix this.

::

  DocumentRoot "/path/to/mozilla/mozilla.com"

6. Restart Apache

If you go to http://mozilla.local/ you should see a page for downloading Firefox.

.. _mozilla-org:

mozilla.org
-----------

If you need to work on mozilla.org, you need to install it as well.
The installation process is identical to mozilla.com, with a few
tweaks.

.. note:: htaccess files do not work on mozilla.org. If you need to
          add anything to htaccess files, you must commit them to the
          mozilla.com codebase. See the section below about the merge
          for more info.

1. Make sure you install it as a subdirectory underneath mozilla.com named *org*.

::

  cd mozilla.com
  svn co https://svn.mozilla.org/projects/mozilla.org/trunk org
  cd org/includes
  cp config.inc.php-dist config.inc.php

2. Open /org/includes/config.inc.php and set the `server_name` to "mozilla.local" (or whatever you will use) and `file_root` to the site's path on the filesystem (including the org subdirectory).
3. In addition, set the 'js_prefix', 'img_prefix', 'style_prefix' config values to '/org'. **That is necessary**.
4. If you need the archive redirects to work, you need to add the RewriteMap directives to your Apache config for the site. Inside the VirtualHost section that you made while installing mozilla.com, add this:

::

  RewriteMap org-urls-410 txt:/path/to/mozilla.com/org-urls-410.txt
  RewriteMap org-urls-301 txt:/path/to/mozilla.com/org-urls-301.txt

5. Depending on your system settings, you might see warnings about relying on the system's timezone settings. If you get this, add the following to the config.inc.php for mozilla.org:

::

  date_default_timezone_set('America/New_York');

You can look up the correct timezone `here
<http://www.php.net/manual/en/timezones.php>`_.

That should be it. If you go to http://mozilla.local/ (or whatever
local server you set it to) you should see the org home page.

Thunderbird
-----------

The thunderbird site has been completely merged in with mozilla.org,
so you can install it by :ref:`installing mozilla.org <mozilla-org>`. It
will be served at /thunderbird.

.. _merge:

Workflow
========

If you are working on a bug, please follow these steps:

1. Commit your work to trunk
2. Comment on the bug and add the revision in the whiteboard field in the form "r=10000". Multiple revisions should be comma-delimited, like "r=10000,10001". You can add the revision in the comment too if you want people to have a link to the changes.
3. Add the keyword "qawanted" when finished
4. When all the work is done and has been QAed, mark as resolved.

We release a batch of resolved bugs every Tuesday. Other bugs can go
out between releases, but by default resolved bugs tagged with the
current milestone will go out the next Tuesday.

Stage isn't used for much, but it's useful for times when we are very
careful about rolling out something. You typically don't need to worry
about it. When bugs are pushed live, they are pushed to stage and
production at the same time.

Rolling out code
----------------

So you want to rollout a bug into production? If you look at our
workflow, there should be some SVN revisions logged into the
whiteboard of the bug. If not, you need to track down which revisions
to push from the comments.

Once you have this list, you need to merge them to the branches
`tags/stage` and `tags/production`. If the revisions are already
pushed to stage, only do the latter. These are the commands:

::

  cd tags/stage
  svn merge --ignore-ancestry -c<revs> ../../trunk
  svn commit -m 'merged <rev> from trunk for bug <id>'

`<revs>` is a single rev or comma-delimited like "10000,10001,10002".

Do the same for tags/production. Always format the log message like
the above. You must use `--ignore-ancestry` also to avoid bad things.

We wrote a script to automate this if you are doing this a lot. You
can find it it on trunk in `/bin/rollout
<https://github.com/jlongster/mozilla.com/blob/master/bin/rollout>`_.
The usage looks like this:

::

  Usage: rollout <bug-id> <revs> <branch>
           <revs> and <branch> are optional

  $ cd mozilla.com  # must have trunk, tags/stage, and tags/production checked out here
  $ rollout 654321
  
  Merging into tags/stage...
  --- Merging r654321 into '.':
  <svn output>

  Continue? y/n [n]y

  Committing tags/stage...

  Merging into tags/production...
  --- Merging r654321 into '.':
  <svn output>

  Continue? y/n [n]y
  Committing tags/production...

The script parses the revisions and branch from the whiteboard data in
bugzilla, and merges it from trunk to stage and production. If the
branch is already stage (b=stage in the whiteboard) it just merges it
to production.

After it does the merges, it asks you if you want to continue. If you
saw conflicts, you shouldn't continue and you should fix the conflicts
and either finish the rollout by hand or update the bugzilla
whiteboard and run the command again.

How a Request is Handled
========================

Magic should always be documented, so let's look at exactly how all
the PHP sites work together to handle a mozilla.org request.

mozilla.org is made up of three sites:

* mozilla.com (the product pages)
* mozilla.org (mofo)
* mozillamessaging.com (thunderbird)

These three sites are now all merged into http://mozilla.org/.
However, on the server a request can be handled by three different
codebases. We'll refer to the mozilla.com codebase as `moco`,
mozilla.org codebase as `mofo`, and messaging as `thunderbird`.

moco is the primary codebase. A request goes through the following steps:

* If the URL exists in the mofo codebase, load the page from there
* If the URL exists in the thunderbird codebase, load from there
* Else, let moco handle the URL like normal

The merge magic is installed into moco's htaccess and PHP files. We
let moco become the primary codebase because if there's any error in
the merge code, we can't afford to break the main Firefox product
pages. There's also more developer attention on moco.

**Special Note**: Only mozilla.com's .htaccess files are processed by
Apache. All the others have been merged in so you shouldn't add
anything to them. Please add all htaccess rules inthe mozilla.com
codebase.

Merge Magic
-----------

How we implement the merge is really important. Performance, site
breakage, and amount of work to move things around are all serious
considerations. The merge is meant to be temporary as the site is
moving to Python, so it's not worth the effort to literally merge all
the PHP code together.

It's also important to still allow the mofo and moco codebases to be
run individually. We don't want to suddenly break it for people who
have it locally checked out (short-term wise). Finally, the code of
each site also dictated possible solutions. There's a lot of edge
cases in each site so need to make sure we don't break anything.

Here's how the merge magic was implemented:

**Short version:**

* Check out the mofo codebase under moco as the subdirectory *org*.
* Redirect all mofo URLs to a PHP handler which loads those pages, do
  the same for thunderbird
* Fix loading of images, css, and js by setting prefix config values and more rewrites
* Merge .htaccess files into the moco codebase

**Long version:**

* Check out the mofo codebase under moco as the subdirectory *org*.

  * Thunderbird is a folder under org, at /org/thunderbird

* Generate a list of top-level folders in the org site and use Apache
  rewrites to `redirect all those URLs to a special php handler <https://github.com/jlongster/mozilla.com/blob/813aa578d7850f79d9f6b5274051f0f2175dd957/.htaccess#L805>`_
* Write the `special php handler
  <https://github.com/jlongster/mozilla.com/blob/813aa578d7850f79d9f6b5274051f0f2175dd957/includes/org-handler.php>`_
  to load mofo pages. This is basically a port of mofo's prefetch.php
* Write a `similar handler
  <https://github.com/jlongster/mozilla.com/blob/813aa578d7850f79d9f6b5274051f0f2175dd957/includes/thunderbird-handler.php>`_
  for the thunderbird pages and `redirect all /thunderbird URLs to it <https://github.com/jlongster/mozilla.com/blob/813aa578d7850f79d9f6b5274051f0f2175dd957/.htaccess#L616>`_
* Fix loading of assets

  * `Set config values
    <https://github.com/jlongster/mozilla.org/blob/master/includes/config.inc.php-dist#L96>`_
    to load assets with the "/org" prefix
  * For bad code that doesn't use the config, use `apache rewrites
    <https://github.com/jlongster/mozilla.com/blob/813aa578d7850f79d9f6b5274051f0f2175dd957/.htaccess#L579>`_
    to redirect `images` and `script` to the respective folder in
    "/org". These two folders don't conflict with the moco codebase.
    The `style` directory conflicts, so make sure all code uses the
    config prefix value.
  * `Redirect any other asset directory
    <https://github.com/jlongster/mozilla.com/blob/813aa578d7850f79d9f6b5274051f0f2175dd957/.htaccess#L590>`_
    to use the "/org" prefix (/thunderbird/img/, etc)

* Merge .htacess files

  * The biggest side effect of this is that only moco htaccess files
    are processed, but we should consolidate things anyway
  * `Move the redirects
    <https://github.com/jlongster/mozilla.com/blob/813aa578d7850f79d9f6b5274051f0f2175dd957/.htaccess#L619>`_
    and other appropriate rules from mofo's htaccess to moco's
  * `Optimize the crazy amount of 301 and 410 redirects
    <https://github.com/jlongster/mozilla.com/blob/813aa578d7850f79d9f6b5274051f0f2175dd957/.htaccess#L602>`_
    from mofo, mostly archive redirects, using RewriteMap
  * Test to make sure everything's working, implement special rewrites
    or org-handler.php hacks to fix any breakage

* Check file extensions for any leftover static types and `rewrite them <https://github.com/jlongster/mozilla.com/blob/master/.htaccess#L582>`_ to be served by Apache

The final result is the moco codebase which dispatches a lot of URLs
to the mofo and thunderbird codebases. 
