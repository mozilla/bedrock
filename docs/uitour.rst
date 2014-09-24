.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _ui-tour:

==============
Mozilla.UITour
==============

Introduction
------------

``Mozilla.UITour`` is a JS library that exposes an event-based Web API for
communicating with the Firefox browser chrome. It can be used for tasks such
as opening menu panels and highlighting the position of buttons in the toolbar.
It is supported in Firefox 29 onward.

For security reasons ``Mozilla.UITour`` will only work on white-listed domains and
over a secure connection. The white-listed domains are https://www.mozilla.org and
https://support.mozilla.org and the special about:home page.

The ``Mozilla.UITour`` library is currently maintained in a external `GiHub Repo`_.

Local development
-----------------

To develop or test using Mozilla.UITour locally you need to create some custom
preferences in ``about:config``.

* ``browser.uitour.whitelist.add.testing`` (string) (value: local address e.g. ``127.0.0.1:8000``)
* ``browser.uitour.requireSecure`` (boolean) (value: ``false``)

Then restart Firefox and the API should work.

JavaScript API
--------------

registerPageID(pageId)
^^^^^^^^^^^^^^^^^^^^^^

Register an ID for use in `Telemetry`_. ``pageId`` must be a string unique to the page:

.. code-block:: javascript

    var pageId = 'firstrun-page-firefox-29';

    Mozilla.UITour.registerPageID(pageId);

showHighlight(target, effect)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Highlight a button in the browser chrome. ``target`` is the string ID for the button
and ``effect`` is the animation type:

.. code-block:: javascript

    Mozilla.UITour.showHighlight('appMenu', 'wobble');

Target types:

* ``'pinnedTab'``
* ``'accountStatus'``
* ``'addons'``
* ``'appMenu'``
* ``'backForward'``
* ``'bookmarks'``
* ``'customize'``
* ``'help'``
* ``'home'``
* ``'quit'``
* ``'search'``
* ``'searchProvider'``
* ``'urlbar'``

Effect types:

* ``'random'``
* ``'wobble'``
* ``'zoom'``
* ``'color'``
* ``'none'`` (default)

hideHighlight()
^^^^^^^^^^^^^^^

Hides the currently visible highlight:

.. code-block:: javascript

    Mozilla.UITour.hideHighlight();

showInfo(target, title, text, icon, buttons, options)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Displays a customizable information panel pointing to a given target:

.. code-block:: javascript

    var buttons = [
        {
            label: 'Cancel',
            style: 'link',
            callback: cancalBtnCallback
        },
        {
            label: 'Confirm',
            style: 'primary',
            callback: confirmBtnCallback
        }
    ];

    var icon = '//mozorg.cdn.mozilla.net/media/img/firefox/australis/logo.png';

    var options = {
        closeButtonCallback: closeBtnCallback
    };

    Mozilla.UITour.showInfo('appMenu', 'my title', 'my text', icon, buttons, options);

Available targets:

* ``'appMenu'``
* ``'bookmarks'``

Additional parameters:

* ``title`` panel title (string).
* ``text`` panel description (string).
* ``icon`` panel icon absolute url (string). Icon should be 48px x 48px.
* ``buttons`` array of buttons (object)
* ``options`` (object)

``buttons`` array items can have the following properties:

* ``label`` button text (string)
* ``icon`` button icon url (string)
* ``style`` button style can be either `primary` or `link` (string)
* ``callback`` to be excecuted when the button is clicked (function)
* ``options`` (object)

``options`` can have the following properties:

* ``closeButtonCallback`` to be excecuted when the (x) close button is clicked (function)

hideInfo()
^^^^^^^^^^

Hides the currently visible info panel:

.. code-block:: javascript

    Mozilla.UITour.hideInfo();

previewTheme(theme)
^^^^^^^^^^^^^^^^^^^

Previews a Firefox theme. ``theme`` should be a JSON literal:

.. code-block:: javascript

    var theme = {
        "category":     "Firefox",
        "iconURL":      "https://addons.mozilla.org/_files/18066/preview_small.jpg?1241572934",
        "headerURL":    "https://addons.mozilla.org/_files/18066/1232849758499.jpg?1241572934",
        "name":         "Dark Fox",
        "author":       "randomaster",
        "footer":       "https://addons.mozilla.org/_files/18066/1232849758500.jpg?1241572934",
        "previewURL":   "https://addons.mozilla.org/_files/18066/preview.jpg?1241572934",
        "updateURL":    "https://versioncheck.addons.mozilla.org/en-US/themes/update-check/18066",
        "accentcolor":  "#000000",
        "header":       "https://addons.mozilla.org/_files/18066/1232849758499.jpg?1241572934",
        "version":      "1.0",
        "footerURL":    "https://addons.mozilla.org/_files/18066/1232849758500.jpg?1241572934",
        "detailURL":    "https://addons.mozilla.org/en-US/firefox/addon/dark-fox-18066/",
        "textcolor":    "#ffffff",
        "id":           "18066",
        "description":  "My dark version of the Firefox logo."
    };

    Mozilla.UITour.previewTheme(theme);

resetTheme()
^^^^^^^^^^^^

Removes the previewed theme and resets back to default:

.. code-block:: javascript

    Mozilla.UITour.resetTheme();

cycleThemes(themes, delay, callback)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cycles through an array of themes at a set interval with a callback on each step:

.. code-block:: javascript

    var themes = [
        ...
    ];

    var myCallback = function () {
        ...
    };

    Mozilla.UITour.cycleThemes(themes, 5000, myCallback);

* ``themes`` (array)
* ``delay`` in milliseconds (number)
* ``callback`` to excecute at each step (function)

addPinnedTab()
^^^^^^^^^^^^^^

Adds a pinned tab to the browser window. For security reasons the URL for this pinned tab
is hard-coded in the browser, and currently points to ``https://support.mozilla.org/kb/pinned-tabs-keep-favorite-websites-open``

.. code-block:: javascript

    Mozilla.UITour.addPinnedTab();

removePinnedTab()
^^^^^^^^^^^^^^^^^

Removes the pinned tab if one was created.

.. code-block:: javascript

    Mozilla.UITour.removePinnedTab();

getConfiguration(type, callback)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Queries the current browser configuration so the web page can make informed decisions on
available highlight targets.

* ``type`` can be either ``'sync'`` or ``'availableTargets'`` (string)
* ``callback`` to excecute and return with the queried data (function)

If ``'sync'`` is queried the object returned by the callback will contain an object called ``setup``. This can be used to determine if the user is already using Firefox Sync:

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('sync', function (config) {
        if (config.setup === false) {
            // user is not using Firefox Sync
        }
    });

If ``'availableTargets'`` is queried the object returned by the callback contain array called ``targets``. This can be used to determine what highlight targets are currently available in the browser chrome:

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('availableTargets', function (config) {
        console.dir(config.targets)
    });

showFirefoxAccounts();
^^^^^^^^^^^^^^^^^^^^^^

Allows a web page to navigate directly to ``about:accounts?action=signup``

.. code-block:: javascript

    Mozilla.UITour.showFirefoxAccounts();

.. Important::

    ``showFirefoxAccounts()`` is only available in Firefox 31 onward!

.. _GiHub Repo: https://github.com/Unfocused/mozilla-uitour
.. _Telemetry: https://wiki.mozilla.org/Telemetry
