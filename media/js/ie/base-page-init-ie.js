/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * General DOM ready handler applied to all pages in base template.
 */
$(document).ready(function() {
    'use strict';

    // Initialize download buttons.
    Mozilla.UtilsIE.initDownloadLinks();

    // Initialize navigation.
    Mozilla.UtilsIE.initNavigation();

    $(window).on('load', function() {
        $('html').addClass('loaded');
    });
});
