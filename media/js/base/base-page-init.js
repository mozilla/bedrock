/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * General DOM ready handler applied to all pages in base template.
 */
(function($) {
    'use strict';

    // page must be loaded and ready before onWindowLoad fires
    var loaded = false;
    var ready = false;

    function onWindowLoad() {
        $('html').addClass('loaded');
    }

    $(document).ready(function() {

        var client = Mozilla.Client;
        var utils = Mozilla.Utils;

        utils.initMobileDownloadLinks();
        utils.trackDownloadThanksButton();

        /* Bug 1264843: In partner distribution of desktop Firefox, switch the
        downloads to corresponding partner build of Firefox for Android. */
        if (client.isFirefoxDesktop) {
            client.getFirefoxDetails(utils.maybeSwitchToChinaRepackImages);
        }

        // if window.load happened already, fire onWindowLoad
        if (loaded) {
            onWindowLoad();
        }

        // note that document.ready happened to inform window.load
        ready = true;
    });

    $(window).on('load', function () {
        // if document.ready happened already, fire onWindowLoad
        if (ready) {
            onWindowLoad();
        }

        // note that window.load happened in case document.ready hasn't
        // finished yet
        loaded = true;
    });
})(window.jQuery);
