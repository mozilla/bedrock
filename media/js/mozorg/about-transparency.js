/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    var _mqWide = matchMedia('(max-width: 767px)');
    if (_mqWide.matches) {
        window.MzpDetails.init('.c-collapsible-section-heading');
    }

    function handleMqChange(mq) {
        if (mq.matches) {
            window.MzpDetails.init('.c-collapsible-section-heading');
        } else {
            window.MzpDetails.destroy('.c-collapsible-section-heading');
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
