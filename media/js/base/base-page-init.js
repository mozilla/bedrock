/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * General DOM ready handler applied to all pages in base template.
 */
$(document).ready(function() {

    var client = Mozilla.Client;
    var utils = Mozilla.Utils;

    utils.initDownloadLinks();
    utils.initMobileDownloadLinks();
    utils.initLangSwitcher();

    /* Bug 1264843: In partner distribution of desktop Firefox, switch the
       downloads to corresponding partner build of Firefox for Android. */
    if (client.isFirefoxDesktop) {
        client.getFirefoxDetails(utils.maybeSwitchToDistDownloadLinks);
    }

    $(window).on('load', function () {
        $('html').addClass('loaded');
    });
});
