/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    var client = Mozilla.Client;

    var $main = $('main');

    // use a slight delay for showing the main page content
    // to allow for initial page state to be determined
    setTimeout(function () {
        $main.css('visibility', 'visible');
    }, 500);

    // FTE will only run on Firefox Desktop 35 and above
    if (client.isFirefoxDesktop && client.FirefoxMajorVersion >= 35) {
        Mozilla.HelloFTU.init();
    }

})(window.jQuery, window.Mozilla);
