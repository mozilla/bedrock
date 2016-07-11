/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var mozClient = window.Mozilla.Client;

    var $toggleInnovate = $('.toggle-innovate');
    var $toggleWho = $('.toggle-who');
    var $whoInnovateWrapper = $('#who-innovate-wrapper');
    var $who = $('#who');
    var $innovate = $('#innovate');

    // hide download button for up-to-date fx desktop/android users
    if ((mozClient.isFirefoxDesktop || mozClient.isFirefoxAndroid) && mozClient._isFirefoxUpToDate(false)) {
        $('#nav-download-firefox').css('display', 'none');
    }

    // show mobile download buttons if on mobile platform and not fx
    if (mozClient.isMobile && !mozClient.isFirefox) {
        $('#fxmobile-download-buttons').addClass('visible');
        $('#fx-download-link').addClass('hidden');
    }

    $toggleWho.on('click', function() {
        $whoInnovateWrapper.toggleClass('open-who');
        $who.toggleClass('open');
    });

    $toggleInnovate.on('click', function() {
        $whoInnovateWrapper.toggleClass('open-innovate');
        $innovate.toggleClass('open');
    });
})(window.jQuery);
