/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var clientHelper = {};

    clientHelper.triggerEvent = function(eventName, elem) {
        var evt = document.createEvent('Event');
        evt.initEvent(eventName, true, true);
        elem.dispatchEvent(evt);
    };

    window.__clientHelper__ = clientHelper;
})();
