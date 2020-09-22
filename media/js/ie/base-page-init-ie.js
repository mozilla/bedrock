/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * General DOM ready handler applied to all pages in base template.
 */

/* eslint-disable no-jquery/no-class */
/* eslint-disable no-jquery/no-jquery-constructor */
/* eslint-disable no-jquery/no-other-methods */
/* eslint-disable no-jquery/no-ready-shorthand */

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

/* eslint-enable no-jquery/no-class */
/* eslint-enable no-jquery/no-jquery-constructor */
/* eslint-enable no-jquery/no-other-methods */
/* eslint-enable no-jquery/no-ready-shorthand */
