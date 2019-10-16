/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';
    var _mqWide = matchMedia('(max-width: 767px)');
    if (_mqWide.matches) {
        window.Mzp.Details.init('.c-collapsible-section-heading');
    }
    _mqWide.addListener(function (mq) {
        if (mq.matches) {
            window.Mzp.Details.init('.c-collapsible-section-heading');
        } else {
            window.Mzp.Details.destroy('.c-collapsible-section-heading');
        }
    });
})();
