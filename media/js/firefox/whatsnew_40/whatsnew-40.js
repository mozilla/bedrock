/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    // Conditional content for Firefox Desktop 40 and above only.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 40) {
        Mozilla.FirefoxDefault.isDefaultBrowser(function(isDefault) {
            if (window.location.href.indexOf('?default=false') !== -1 || isDefault === 'no') {
                $('main').addClass('firefox-not-default');
                $('#set-default').on('click', Mozilla.FirefoxDefault.setDefaultBrowser);
            } else {
                $('main').addClass('firefox-default');
            }
        });
    }

})(window.jQuery, window.Mozilla);
