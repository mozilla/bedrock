.. _php:

==========================================
Installing and Learning About the PHP Site
==========================================

The previous version of mozilla.org was written in PHP. The PHP
codebase still serves some of the mozilla.org pages because we haven't
migrated everything over. A request runs through the following stack:

* If the page exists in Bedrock, serve from Bedrock
* If the page exists in the PHP site, serve from PHP
* Else, serve a 404 page

.. note:: As of right now, Bedrock isn't actually live yet, so the PHP
          site still serves everything, so ignore the above.

History
-------

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
----------

.. _mozilla-com:
mozilla.com
~~~~~~~~~~~

If you want to just work on the mozilla.com codebase (currently served
at mozilla.org/firefox), install it with these commands:

::

  svn co https://svn.mozilla.org/projects/mozilla.com/trunk mozilla.com
  cd mozilla.com/includes
  cp config.inc.php-dist config.inc.php

You need to set the 'server_name' and 'file_root' variables in config.inc.php.

Now configure Apache to allow the site to run with a Directory and VirtualHost directive:

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

Change ServerName and /path/to/ to the correct values. Additionally,
you *might* need to set the DocumentRoot to the site if you can't load
any CSS files. We are looking to fix this.

::

  DocumentRoot "/path/to/mozilla/mozilla.com"

If you go to http://mozilla.local/ you should see a page for downloading Firefox.

.. _mozilla-org:
mozilla.org
~~~~~~~~~~~

If you need to work on mozilla.org, you need to install it as well.
The installation process is identical to mozilla.com, with a few
tweaks. First, make sure you install it as a subdirectory underneath
mozilla.com named *org*.

::

  cd mozilla.com
  svn co https://svn.mozilla.org/projects/mozilla.org/trunk org
  cd org/includes
  cp config.inc.php-dist config.inc.php

Set the 'server_name' and 'file_root' variables in config.inc.php like
you did for mozilla.com. In addition, set the 'js_prefix',
'img_prefix', 'style_prefix' config values to '/org'. **That is necessary**.

If you need the archive redirects to work, you need to add the
RewriteMap directives to your Apache config for the site. Inside the
VirtualHost section that you made while installing mozilla.com, add this::

    RewriteMap org-urls-410 txt:/path/to/mozilla.com/org-urls-410.txt
    RewriteMap org-urls-301 txt:/path/to/mozilla.com/org-urls-301.txt

That should be it. If you go to http://mozilla.local/ (or whatever
local server you set it to) you should see the org home page.

Thunderbird
~~~~~~~~~~~

The thunderbird site has been completely merged in with mozilla.org,
so you can install it by `installing mozilla.org <mozilla-org>`. It
will be served at /thunderbird.

How a Request is Handled
------------------------

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
~~~~~~~~~~~

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

* Checkout the mofo codebase under moco as the subdirectory *org*.
* Redirect all mofo URLs to a PHP handler which loads those pages, do
  the same for thunderbird
* Fix loading of images, css, and js by setting prefix config values and more rewrites
* Merge .htaccess files into the moco codebase

**Long version:**

* Checkout the mofo codebase under moco as the subdirectory *org*.
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



.. ::




..    +-----------------------------------+          +------------------------+
..    |  Page exist in Bedrock (Python)?  |--------->|  Serve from Bedrock    |
..    +-----------------------------------+   Yes    +------------------------+
..                    |
..                    | No 
..                    v   
..    +-----------------------------------+          +------------------------+
..    |  Page exist in PHP site?          |--------> |  Serve from PHP        |
..    +-----------------------------------+   Yes    +------------------------+
..                    |   
..                    | No
..                    v
..    +----------------------------------+
..    |  Serve 404 page                  |
..    +----------------------------------+
