/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// temporary a11y patch needs to be pack ported to protocol: https://github.com/mozilla/protocol/issues/999
var MzpSideMenu = require('./protocol/sidemenu.es6');

(function () {
    'use strict';

    // Initialize Protocol side menu.
    MzpSideMenu.init();

    var _mqWide = matchMedia('(max-width: 767px)');

    if (_mqWide.matches) {
        window.MzpDetails.init('.side-reference-title');
    }

    function handleMqChange(mq) {
        if (mq.matches) {
            window.MzpDetails.init('.side-reference-title');
        } else {
            window.MzpDetails.destroy('.side-reference-title');
        }
    }

    if (window.matchMedia('all').addEventListener) {
        // evergreen
        _mqWide.addEventListener('change', handleMqChange, false);
    } else if (window.matchMedia('all').addListener) {
        // IE fallback
        _mqWide.addListener(handleMqChange);
    }
})();
