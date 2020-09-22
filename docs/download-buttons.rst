.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _download-buttons:

========================
Firefox Download Buttons
========================

There are two Firefox download button helpers in bedrock to choose from. The first is a lightweight button
that links directly to the ``/firefox/download/thanks/`` page. Its sole purpose is to facilitate downloading
the main release version of Firefox.

.. code-block:: jinja

    {{ download_firefox_thanks() }}

The second type of button is more heavy weight, and can be configured to download any build of Firefox (e.g.
Release, Beta, Developer Edition, Nightly). It can also offer functionality such as direct (in-page) download
links, so it comes with a lot more complexity and in-page markup.

.. code-block:: jinja

    {{ download_firefox() }}

Which button should I use?
--------------------------

A good rule of thumb is to always use ``download_firefox_thanks()`` for regular landing pages (such as
``/firefox/new/``) where the main release version of Firefox is the product being offered. For pages pages
that require direct download links, or promote pre-release products (such as ``/firefox/channel/``)
then ``download_firefox()`` should be used instead.

Documentation
-------------

See `helpers.py`_ for documentation and supported parameters for both buttons.

.. _helpers.py: https://github.com/mozilla/bedrock/blob/master/bedrock/firefox/templatetags/helpers.py

