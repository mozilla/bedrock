/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function(Mozilla) {
    'use strict';

    // temporarily disable UITour CTA until Firefox 40.0.1 is released.
    Mozilla.Win10Welcome.showDefaultContent();

    // Conditional content for Firefox Desktop 40 and above only.
    // if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 40) {
    //     Mozilla.Win10Welcome.initPage();
    // } else {
    //     // We're not concerned about non-Firefox browsers for this page, but we need to
    //     // show them something so here are some nice links.
    //     Mozilla.Win10Welcome.showDefaultContent();
    // }

})(window.Mozilla);
