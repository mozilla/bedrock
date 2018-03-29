/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
    'use strict';

    // Open Twitter in a sub window
    var openTwitterSubwin = function (url) {
        var width = 550;
        var height = 420;
        var options = {
            'scrollbars': 'yes',
            'resizable': 'yes',
            'toolbar': 'no',
            'location': 'yes',
            'width': width,
            'height': height,
            'top': screen.height > height ? Math.round((screen.height / 2) - (height / 2)) : 0,
            'left': Math.round((screen.width / 2) - (width / 2))
        };

        window.open(url, 'twitter_share', $.param(options).replace(/&/g, ',')).focus();
    };

    // Set up twitter link handler
    $('.js-manifesto-share').on('click', function (event) {
        var href = $(this).attr('href');

        // Open Twitter in a sub window
        openTwitterSubwin(href);
        event.preventDefault();
    });
});
