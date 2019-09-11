.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _funnelcake:

===============================
Funnel cakes and Partner Builds
===============================

Funnel cakes
------------

In addition to being `an American delicacy <https://en.wikipedia.org/wiki/Funnel_cake>`_
funnel cakes are what we call special builds of Firefox. They can come with
extensions preinstalled and/or a custom first-run experience.

    "The whole funnelcake system is so marred by history at this point I don't
    know if anyone fully understands what it's supposed to do in all situations"
    - pmac

Funnelcakes are configured by the Release Engineering team. You can see the
configs in the `funnelcake git repo <https://github.com/mozilla-partners/funnelcake>`_

Currently bedrock only supports funnelcakes for "stub installer platforms". Which
means they are windows only. However, funnelcakes can be made for all platforms
so `bedrock support may expand <https://github.com/mozilla/bedrock/issues/6251>`_.

We signal to bedrock that we want a funnelcake when linking to the download
page by appending the query variable `f` with a value equal to the funnelcake
number being requested.

.. code-block:: text

    https://www.mozilla.org/en-US/firefox/download/thanks/?f=137

Bedrock checks to see if the funnelcake is configured (this is handled in the
`www-config repo <https://github.com/mozmeao/www-config/blob/master/waffle_configs/bedrock-prod.env>`_)

.. code-block:: bash

    FUNNELCAKE_135_LOCALES=en-US
    FUNNELCAKE_135_PLATFORMS=win,win64

Bedrock then converts that into a request to download a file like so:

Windows:

.. code-block:: text

    https://download.mozilla.org/?product=firefox-stub-f137&os=win&lang=en-US

Mac (You can see the mac one does not pass the funnelcake number along.):

.. code-block:: text

    https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US

Someone in Release Engineering needs to set up the redirects on their side to
take the request from here.

Places things can go wrong
~~~~~~~~~~~~~~~~~~~~~~~~~~

As with many technical things, the biggest potential problems are with people:

- Does it have executive approval?
- Did legal sign off?
- Has it had a security review?

On the technical side:

- Is the switch enabled?
- Is the variable being passed?

Partner builds
--------------

Bedrock does not have an automated way of handling these, so you'll have to
craft your own download button:

.. code-block:: html

    <a href="https://download.mozilla.org/?product=firefox-election-edition&os=win&lang=en-US">
    Download</a>

------------

Bugs that might have useful info:

- https://bugzilla.mozilla.org/show_bug.cgi?id=1450463
- https://bugzilla.mozilla.org/show_bug.cgi?id=1495050

PRs that might have useful code:

- https://github.com/mozilla/bedrock/pull/5555
