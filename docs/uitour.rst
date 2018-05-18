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

.. Important::

    The API is supported only on the desktop versions of Firefox. It doesn't
    work on Firefox for Android and iOS.

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

Tracking Protection UITour
--------------------------

In order to test the Tracking Protection tour on a local server or domain other
than www.mozilla.org, you must first set an additional preference in ``about:config``
in addition to white listing UITour for the domain.

* ``privacy.trackingprotection.introURL`` value e.g. ``http://127.0.0.1:8000/%LOCALE%/firefox/%VERSION%/tracking-protection/start/``

Once this preference has been set, the tour can be accessed by opening a new Private Window
and then by clicking the "See how this works" CTA button.

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
* ``'searchIcon'`` (Firefox 34 and above)
* ``'urlbar'``
* ``'loop'``
* ``'forget'``
* ``'privateWindow'``
* ``'trackingProtection'`` (Firefox 42 and above)
* ``'controlCenter-trackingUnblock'`` (Firefox 42 and above)
* ``'controlCenter-trackingBlock'`` (Firefox 42 and above)

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
* ``'loop'`` (Firefox 35 and above)
* ``'controlCenter'`` (Firefox 42 and above)

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
* ``'search'``
* ``'canReset'``

Other parameters:

* ``callback`` function to execute and return with the queried data

Specific use cases:

**sync**

If ``'sync'`` is queried the object returned can be used to determine if the user has Sync enabled, and also metrics on the number and types of devices used.

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('sync', function (config) {
        console.log(config) // { setup: true, desktopDevices: 2, mobileDevices: 1, totalDevices: 3 }
    });

.. Important::

    Sync device count metrics only available in Firefox 50 onwards.

**availableTargets**

If ``'availableTargets'`` is queried the object returned by the callback contain array called ``targets``. This can be used to determine what highlight targets are currently available in the browser chrome:

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('availableTargets', function (config) {
        console.dir(config.targets);
    });

**appinfo**

If ``'appinfo'`` is queried the object returned gives information on the users current Firefox version.

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('appinfo', function (config) {
        console.dir(config); //{defaultUpdateChannel: "aurora", version: "48.0a2", distribution: "default", defaultBrowser: true}
    });

The ``defaultUpdateChannel`` key has many possible values, the most important being:

* ``'release'``
* ``'beta'``
* ``'aurora'``
* ``'nightly'``
* ``'default'`` (self-build or automated testing builds)

The ``distribution`` key holds the value for the Firefox distributionId property. This value will be ``default`` in most cases but can differ for repack or funnelcake builds.

The ``profileCreatedWeeksAgo`` key returns the number of weeks since the profile was created, starting from 0 for profiles dating less than seven days old.

The ``profileResetWeeksAgo`` key returns the number of weeks since the profile was last reset, starting from 0 for profiles reset less than seven days ago. If the profile has never been reset it returns ``null``.

.. Important::

    ``appinfo`` is only available in Firefox 35 onward. The ``defaultBrowser`` property will only be returned on Firefox 40 or later. The ``distribution`` property will only be returned on Firefox 48 or later.  Properties ``profileCreatedWeeksAgo`` and ``profileResetWeeksAgo`` will only be returned on Firefox 56 or later.

**selectedSearchEngine**

If ``'selectedSearchEngine'`` is queried the object returned gives the currently selected default search provider.

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('selectedSearchEngine', function (data) {
        console.log(data.searchEngineIdentifier); // 'google'
    });

.. Important::

    ``selectedSearchEngine`` is only available in Firefox 34 onward.

**search**

This is an alias to ``'selectedSearchEngine'`` that also returns an array of available search engines.

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('search', function (data) {
        console.log(data); // { searchEngineIdentifier: "google", engines: Array[8] }
    });

    .. Important::

        ``search`` is only available in Firefox 43 onward.

**canReset**

If ``'canReset'`` is queried the callback returns a boolean value to indicate if a user can refresh their Firefox profile via ``resetFirefox()``

.. code-block:: javascript

    Mozilla.UITour.getConfiguration('canReset', function (canReset) {
        console.log(canReset); // true
    });

.. Important::

    ``canReset`` is only available in Firefox 48 onward.

setConfiguration(name, value);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sets a specific browser preference using a given key value pair.

Available key names:

* ``'defaultBrowser'``

Specific use cases:

**defaultBrowser**

Passing ``defaultBrowser`` will set Firefox as the default web browser.

.. code-block:: javascript

    Mozilla.UITour.setConfiguration('defaultBrowser');

.. Important::

    ``setConfiguration('defaultBrowser')`` is only available in Firefox 40 onward.

showFirefoxAccounts(extraURLCampaignParams);
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Allows a web page to navigate directly to
``https://accounts.firefox.com/signup?entrypoint=uitour``. In Firefox 47 and beyond,
optionally accepts an object of ``utm_*`` key/values, which will be encoded and
appended to the ``https://accounts.firefox.com/signup`` querystring.

.. Important::

    All keys in ``extraURLCampaignParams`` must begin with ``utm_``. If an
    invalid key is present, the call to ``showFirefoxAccounts`` will fail.

.. code-block:: javascript

    // no extra utm_ campaign params. will open
    // https://accounts.firefox.com/signup?entrypoint=uitour
    Mozilla.UITour.showFirefoxAccounts();

    // with extra utm_ campaign params. will open
    // https://accounts.firefox.com/signup?&entrypoint=uitour&utm_foo=bar&utm_bar=baz
    Mozilla.UITour.showFirefoxAccounts({
        'utm_foo': 'bar',
        'utm_bar': 'baz'
    });

.. Important::

    ``showFirefoxAccounts()`` is only available in Firefox 31 onward.
    ``extraURLCampaignParams`` parameter only functional in Firefox 47 onward.

.. note::

    A convenience method named ``utmParamsFxA`` exists in
    ``js/base/search-params.js`` that pulls all ``utm_`` params from the current
    page's URL and places them in an object (along with pre-defined defaults)
    ready to pass to ``showFirefoxAccounts``.

resetFirefox();
^^^^^^^^^^^^^^^

Opens the Firefox reset panel, allowing users to choose to reomve add-ons and customizations, as well as restore browser defaults.

.. code-block:: javascript

    Mozilla.UITour.resetFirefox();

.. Important::

    ``resetFirefox()`` should be called only in Firefox 48 onwards, and only after
    first calling ``getConfiguration('canReset')`` to determine if the user profile
    is eligible.

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

Retrieved the value for a set `FHR`_ treatment tag.

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

openPreferences(id);
^^^^^^^^^^^^^^^^^^^^

Opens the Firefox Preferences tab at a specified section.
Accepts one of the following options to be passed as an `id`:

* ``'general'``
* ``'search'``
* ``'content'``
* ``'applications'``
* ``'privacy'``
* ``'security'``
* ``'sync'``
* ``'advanced'``

.. code-block:: javascript

    Mozilla.UITour.openPreferences('privacy');

.. Important::

    Only available in Firefox 42 onward.

closeTab();
^^^^^^^^^^^

Closes the current tab.

.. code-block:: javascript

    Mozilla.UITour.closeTab();

.. Important::

    This function will do nothing when called from the last browser window when it contains
    only one tab. You may need to provide a work around for this edge case in your code.
    This function is also only available in Firefox 46 onward.

showNewTab();
^^^^^^^^^^^^^

Opens about:newtab in the same tab.

.. code-block:: javascript

    Mozilla.UITour.showNewTab();

.. Important::

    This function is only available in Firefox 51 onward.

.. _Mozilla Central: http://dxr.mozilla.org/mozilla-central/source/browser/components/uitour/UITour-lib.js
.. _Telemetry: https://wiki.mozilla.org/Telemetry
.. _FHR: https://support.mozilla.org/en-US/kb/firefox-health-report-understand-your-browser-perf
