/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global initDownloadLinks, initMobileDownloadLinks, initLangSwitcher,
   maybeSwitchToDistDownloadLinks */

// init global.js functions
$(document).ready(function() {
    initDownloadLinks();
    initMobileDownloadLinks();
    initLangSwitcher();

    /* Bug 1264843: In partner distribution of desktop Firefox, switch the
       downloads to corresponding partner build of Firefox for Android. */
    if (Mozilla.Client.isFirefoxDesktop) {
        Mozilla.Client.getFirefoxDetails(maybeSwitchToDistDownloadLinks);
    }

    $(window).on('load', function () {
        $('html').addClass('loaded');
    });
});
