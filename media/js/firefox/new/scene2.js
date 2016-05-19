/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, dataLayer) {
    'use strict';

    var isIELT9 = window.Mozilla.Client.platform === 'windows' && /MSIE\s[1-8]\./.test(navigator.userAgent);
    var $directDownloadLink = $('#direct-download-link');
    var $platformLink = $('#download-button-wrapper-desktop .download-list li:visible .download-link');
    var $stage = $('#stage');

    // build virtualUrl for GA
    var pathParts = window.location.pathname.split('/');
    var queryStr = window.location.search ? window.location.search + '&' : '?';
    var referrer = pathParts[pathParts.length - 2];
    var locale = pathParts[1];
    var virtualUrl = ('/' + locale + '/products/download.html' +
                       queryStr + 'referrer=' + referrer);

    // pixel remains in perpetuity (https://bugzilla.mozilla.org/show_bug.cgi?id=1222945#c2)
    function addPixel() {
        if (!window._dntEnabled()) {
            var $body = $('body');

            var $pixel = $('<img />', {
                width: '1',
                height: '1',
                src: 'https://servedby.flashtalking.com/spot/8/6247;40428;4669/?spotName=Mozilla_Download_Conversion'
            });

            $body.append($pixel);
        }
    }

    if ($platformLink.length) {
        // Pull download link from the download button and add to the
        // 'click here' link.
        // TODO: Remove and generate link in bedrock.
        $directDownloadLink.attr('href', $platformLink.attr('href'));
    }

    // #direct-download-link = "click here" text on page
    // .download-link = any links in download button (which are effectively
    // hidden, but could be clicked by screen reader?)
    $stage.on('click', '#direct-download-link, .download-link', function(e) {
        e.preventDefault();

        var url = $(e.currentTarget).attr('href');

        // An iframe cannot be used here to trigger the download because
        // it will be blocked by Chrome if the download link redirects
        // to a HTTP URI and we are on HTTPS.
        dataLayer.push({
            'event': 'virtual-pageview',
            'virtualUrl': virtualUrl
        });

        window.location.href = url;
    });

    addPixel();

    // if user is not on an IE that blocks JS triggered downloads, start the
    // platform-detected download after window (read: images) have loaded.
    // only auto-start the download if a visible platform link is detected.
    if (!isIELT9 && $platformLink.length) {
        $(window).on('load', function() {
            $directDownloadLink.trigger('click');
        });
    }
})(window.jQuery, window.dataLayer = window.dataLayer || []);
