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

The ``Mozilla.UITour`` library is maintained on `Mozilla Central`_.

Local development
-----------------

To develop or test using Mozilla.UITour locally you need to create some custom
preferences in ``about:config``.

* ``browser.uitour.testingOrigins`` (string) (value: local address e.g. ``http://127.0.0.1:8000``)
* ``browser.uitour.requireSecure`` (boolean) (value: ``false``)

Note that ``browser.uitour.testingOrigins`` can be a comma separated list of domains, e.g.

    'http://127.0.0.1:8000, https://www-demo2.allizom.org'

.. Important::

    Prior to Firefox 36, the testing preference was called ``browser.uitour.whitelist.add.testing``
    (Bug 1081772). This old preference does not accept a comma separated list of domains, and you
    must also exclude the domain protocol e.g. ``https://``. A browser restart is also required
    after adding a whitelisted domain.

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
* ``'searchProvider'`` (Firefox 33 and below)
* ``'searchIcon'`` (Firefox 34 and above)
* ``'urlbar'``
* ``'loop'``
* ``'forget'``
* ``'privateWindow'``

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
            callback: cancelBtnCallback
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

Any target that can be highlighted can have an information panel attached.

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

showMenu(target, callback)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Opens a targeted menu in the browser chrome.

.. code-block:: javascript

    Mozilla.UITour.showMenu('appMenu', function() {
        console.log('menu was opened');
    });

Available targets:

* ``'appMenu'``
* ``'bookmarks'``
* ``'searchEngines'`` (only works for the old Search UI prior to Firefox 34)
* ``'loop'`` (Firefox 35 and greater)

Optional parameters:

* ``callback`` function to be called when the menu was sucessfully opened.

hideMenu(target)
^^^^^^^^^^^^^^^^

.. code-block:: javascript

    Mozilla.UITour.hideMenu('appMenu');

Closes a menu panel.

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

getConfiguration(type, callback)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Queries the current browser configuration so the web page can make informed decisions on
available highlight targets.

Available ``type`` values:

* ``'sync'``
* ``'availableTargets'``
* ``'appinfo'``
* ``'selectedSearchEngine'``
* ``'loop'``

Other parameters:

* ``callback`` function to excecute and return with the queried data

Specific use cases:

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
        console.dir(config.targets);
    });

If ``'appinfo'`` is queried the object returned gives information on the users current Firefox version.

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('appinfo', function (config) {
        console.dir(config); //{defaultUpdateChannel: "nightly", version: "36.0a1"}
    });

The ``defaultUpdateChannel`` key has many possible values, the most important being:

* ``'release'``
* ``'beta'``
* ``'aurora'``
* ``'nightly'``
* ``'default'`` (self-build or automated testing builds)

.. Important::

    ``appinfo`` is only available in Firefox 35 onward.

If ``'selectedSearchEngine'`` is queried the object returned gives the currently selected default search provider.

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('selectedSearchEngine', function (data) {
        console.log(data.searchEngineIdentifier); // 'google'
    });

.. Important::

    ``selectedSearchEngine`` is only available in Firefox 34 onward.

If ``'loop'`` is queried the object returns the boolean value for the ``'loop.gettingStarted.seen'`` preference.

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('loop', function (data) {
        console.log(data.gettingStartedSeen); // true
    });

.. Important::

    ``loop`` is only available in Firefox 36 onward.

setConfiguration(name, value);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sets a specific browser preference using a given key value pair.

Available key names:

* ``'Loop:ResumeTourOnFirstJoin'``

Specific use cases:

Setting the value for ``'Loop:ResumeTourOnFirstJoin'`` will enable Firefox to resume the FTE tour when the user joins their first conversation.

.. code-block:: javascript

    Mozilla.UITour.setConfiguration('Loop:ResumeTourOnFirstJoin', true);

Note: Don't try setting this value to ``false``. The current Hello code in Firefox handles when ``false`` should be set, and will actually set this value to ``true`` regardless whenever it is called. This will likely lead to unexpected results.

.. Important::

    ``setConfiguration('Loop:ResumeTourOnFirstJoin', ...)`` is only available in Firefox 35 onward.

showFirefoxAccounts();
^^^^^^^^^^^^^^^^^^^^^^

Allows a web page to navigate directly to ``about:accounts?action=signup``

.. code-block:: javascript

    Mozilla.UITour.showFirefoxAccounts();

.. Important::

    ``showFirefoxAccounts()`` is only available in Firefox 31 onward.

resetFirefox();
^^^^^^^^^^^^^^^

Opens the Firefox reset panel, allowing users to choose to reomve add-ons and customizations, as well as restore browser defaults.

.. code-block:: javascript

    Mozilla.UITour.resetFirefox();

.. Important::

    ``showFirefoxAccounts()`` is only available in Firefox 35 onward.

addNavBarWidget(target, callback);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adds an icon to the users toolbar

* ``target`` can be an highlight target e.g. ``forget`` (string)
* ``callback`` to excecute once icon added successfully (function)

.. code-block:: javascript

    Mozilla.UITour.addNavBarWidget('forget', function (config) {
        console.log('forget button added to toolbar');
    });

.. Important::

    Only available in Firefox 33.1 onward.

setDefaultSearchEngine(id);
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sets the browser default search engine provider.

* ``id`` string identifier e.g. 'yahoo' or 'google'.

.. code-block:: javascript

    Mozilla.UITour.setDefaultSearchEngine('yahoo');

* Identifiers for en-US builds: https://mxr.mozilla.org/mozilla-release/source/browser/locales/en-US/searchplugins/list.txt
* Identifiers for other locales: https://mxr.mozilla.org/l10n-mozilla-release/find?string=browser%2Fsearchplugins%2Flist.txt

.. Important::

    Only available in Firefox 34 onward.

setSearchTerm(string);
^^^^^^^^^^^^^^^^^^^^^^

Populates the search UI with a given search term.

* ``string`` search term e.g. 'Firefox'

.. code-block:: javascript

    Mozilla.UITour.setSearchTerm('Firefox');

.. Important::

    Only available in Firefox 34 onward.

openSearchPanel(callback);
^^^^^^^^^^^^^^^^^^^^^^^^^^

Opens the search UI drop down panel.

* ``callback`` function to excecute once the search panel has opened

.. code-block:: javascript

    Mozilla.UITour.openSearchPanel(function() {
        console.log('search panel opened');
    });

.. Important::

    Only available in Firefox 34 onward.

setTreatmentTag(name, value);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sets a key value pair as a treatment tag for recording in `FHR`_.

* ``name`` tag name for the treatment
* ``value`` tag value for the treatment

.. code-block:: javascript

    Mozilla.UITour.setTreatmentTag('srch-chg-action', 'Switch');

.. Important::

    Only available in Firefox 34 onward.

getTreatmentTag(name, callback);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieved the value for a set `FHR`_. treatment tag.

* ``name`` tag name to be retrieved
* ``callback`` function to execute once the data has been retrieved

.. code-block:: javascript

    Mozilla.UITour.getTreatmentTag('srch-chg-action', function(value) {
        console.log(value);
    });

.. Important::

    Only available in Firefox 34 onward.

ping(callback);
^^^^^^^^^^^^^^^

Pings Firefox to register that the page is using UiTour API.

* ``callback`` function to execute when Firefox has acknowledged the ping.

.. code-block:: javascript

    Mozilla.UITour.ping(function() {
        console.log('UiTour is working!');
    });

.. Important::

    Only available in Firefox 35 onward.

observe(listener, callback);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Register to listen for Firefox Hello events.

* ``listener`` event handler for receiving Hello events
* ``callback`` function to execute when event listener has been registered correctly

.. code-block:: javascript

    Mozilla.UITour.observe(function(event, data) {
        console.log(event);
        console.log(data);
    }, function () {
        console.log('event listener registered successfully');
    });

Event types:

* ``'Loop:ChatWindowOpened'`` - User opens the chat window.
* ``'Loop:ChatWindowClosed'`` - User closes the chat window.
* ``'Loop:ChatWindowShown'`` - User expands the chat window (also fires when chat window is opened).
* ``'Loop:ChatWindowHidden'`` - User hides the chat window.
* ``'Loop:ChatWindowDetached'`` - User detaches the chat window.
* ``'Loop:IncomingConversation'`` - User has an incoming conversation. Event will have data boolean value ``conversationOpen`` set to ``true`` or ``false`` depending on if the chat window is open or not.
* ``'Loop:RoomURLCopied'`` - User clicks the copy button to share a chat URL.
* ``'Loop:RoomURLEmailed'`` - User clicks the email button to share a chat URL.
* ``'Loop:PanelTabChanged'`` - User clicks on the Contacts or Room tab in the panel. Event will return data = ``rooms`` or ``contacts`` depending on which tab the user clicked on.

Note: UiTour can only create a single listener that is responsible for handling all event types. It is not currently possible to listen for only specific event types.

To unbind listening for events, you can do:

.. code-block:: javascript

    Mozilla.UITour.observe(null);

.. Important::

    Only available in Firefox 35 onward.


.. _Mozilla Central: http://dxr.mozilla.org/mozilla-central/source/browser/components/uitour/UITour-lib.js
.. _Telemetry: https://wiki.mozilla.org/Telemetry
.. _FHR: https://support.mozilla.org/en-US/kb/firefox-health-report-understand-your-browser-perf
