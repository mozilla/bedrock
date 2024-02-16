.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _sitemap:

========
Sitemaps
========

``bedrock`` serves a root sitemap at ``/sitemap.xml``, which links to localised sitemaps for each supported locale.

The sitemap data is (re)generated on a schedule by `www-sitemap-generator <https://github.com/mozmeao/www-sitemap-generator>`_ and then is pulled into ``bedrock``'s database, from which the XML sitemaps are rendered.


Quick summary
#############

What does ``www-sitemap-generator`` do?
---------------------------------------

``www-sitemap-generator``, ultimately, produces an updated ``sitemap.json`` file if it detects changes in pages since the last time the sitemap was generated. It does this by loading every page and checking its ETag. This ``sitemap.json`` data is key to sitemap rendering by ``bedrock``.

The update process is run on a schedule via our `Gitlab CI <https://gitlab.com/mozmeao/www-sitemap-generator>`_ setup.

.. note ::

    ``www-sitemap-generator`` uses the main ``bedrock`` release Docker image as its own base container image, which means it has access to all of ``bedrock``'s code and data-loading utils.

    Bear this in mind when looking at management commands in ``bedrock``; ``update_sitemaps`` is actually only called by ``www-sitemap-generator`` even though it (currently) lives in ``bedrock``


When is the sitemap data pulled into ``bedrock``?
-------------------------------------------------
Bedrock's clock pod regularly runs ``bin/run-db-update.sh``, which calls the ``update_sitemaps_data`` management command. This is what pulls in data from the ``www-sitemap-generator`` git repo and refreshes the ``SitemapURL`` records in Bedrock's database. It is from these ``SitemapURL`` records that the XML sitemap tree is rendered by ``bedrock``.
