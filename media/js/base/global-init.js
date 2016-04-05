/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global initDownloadLinks, updateDownloadTextForOldFx, initMobileDownloadLinks,
   initLangSwitcher */

// init global.js functions
$(document).ready(function() {
    initDownloadLinks();
    initMobileDownloadLinks();
    updateDownloadTextForOldFx();
    initLangSwitcher();
    $(window).on('load', function () {
        $('html').addClass('loaded');
    });
});
