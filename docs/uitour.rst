.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _ui-tour:

==============
Mozilla.UITour
==============

Introduction
------------

`Mozilla.UITour` is a JS library that exposes an event-based Web API for
communicating with the Firefox browser chrome. It can be used for tasks such
as opening menu panels and highlighting the position of buttons in the toolbar.
It is supported in Firefox 29 onward.

For security reasons `Mozilla.UITour` will only work on white-listed domains and
over a secure connection. The white-listed domains are https://www.mozilla.org
and https://support.mozilla.org.

The `Mozilla.UITour` library is currently maintained in a external `GiHub Repo`_.

Local development
-----------------

To develop or test using Mozilla.UITour locally you need to create some custom
preferences in `about:config`.

* `browser.uitour.whitelist.add.testing` (string) (value: local address e.g. `127.0.0.1:8000`)
* `browser.uitour.requireSecure` (boolean) (value: `false`)

Then restart Firefox and the API should then work.

Web API
-------

`Mozilla.UITour.registerPageID(pageId)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Register a ID for use in `Telemetry`_. `pageId` must be a string unique to the page.

`Mozilla.UITour.showHighlight(target, effect)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Highlight a button in the browser chrome. `target` is the string ID for the button
and `effect` is the animation type.

Available targets:

* `'pinnedTab'`
* `'accountStatus'`
* `'addons'`
* `'appMenu'`
* `'backForward'`
* `'bookmarks'`
* `'customize'`
* `'help'`
* `'home'`
* `'quit'`
* `'search'`
* `'searchProvider'`
* `'urlbar'`

Animation types:

* `'random'`
* `'wobble'`
* `'zoom'`
* `'color'`
* `'none'` (default)

`Mozilla.UITour.hideHighlight()`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hides the currently visible highlight.

`Mozilla.UITour.showInfo(target, title, text, icon, buttons, options)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Displays a customizable information panel pointing to a given target.

Available targets:

* `'appMenu'`
* `'bookmarks'`

Additional parameters:

* `title` panel title (string).
* `text` panel description (string).
* `icon` panel icon url (string). Icon should be 48px x 48px.
* `buttons` array of buttons (object)
* `options` (object)

`buttons` array items can have the following properties:

* `label` button text (string)
* `icon` button icon url (string)
* `style` button style can be either `primary` or `link` (string)
* `callback` to be excecuted when the button is clicked (function)
* `options` (object)

`options` can have the following properties:

* `closeButtonCallback` to be excecuted when the (x) close button is clicked (function)

`Mozilla.UITour.hideInfo()`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hides the currently visible info panel.

`Mozilla.UITour.previewTheme(theme)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Previews a Firefox theme. `theme` is a JSON literal e.g.

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

`Mozilla.UITour.resetTheme()`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removes the previewed theme and resets back to default

`Mozilla.UITour.cycleThemes(themes, delay, callback)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cycles through an array of themes at a set interval with a callback on each step.

* `themes` (array)
* `delay` in milliseconds (number)
* `callback` to excecute at each step (function)

`Mozilla.UITour.addPinnedTab()`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adds a pinned tab to the browser window. For security reasons the URL for this pinned tab
is hard-coded in the browser.

`Mozilla.UITour.removePinnedTab()`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removes the pinned tab if one was created.

`Mozilla.UITour.getConfiguration(configName, callback)`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Queries the current browser configuration so the web page can make informed decisions on
available highlight targets.

* `configName` can be either `'sync'` or `'availableTargets'` (string)
* `callback` to excecute and return with the queried data (function)

If `sync` is queried, the callback will determine if the user is already using Firefox
Sync by returning a `setup` boolean property:

    .. code-block:: javascript

        Mozilla.UITour.getConfiguration('sync', function (config) {
            if (config.setup === false) {
                // user is not using Firefox Sync
            }
        });

If `availableTargets` is queried, the callback will return an array called `targets`:

    .. code-block:: javascript

        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            console.dir(config.targets)
        });

.. _GiHub Repo: https://github.com/Unfocused/mozilla-uitour
.. _Telemetry: https://wiki.mozilla.org/Telemetry
