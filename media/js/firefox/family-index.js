/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $html = $(document.documentElement);
    var $downloadbar = $('#conditional-download-bar');

    // Open external links in new window/tab
    $('.product a[rel="external"]').attr('target', '_blank');

    // Dismiss the conditional download bar
    $downloadbar.on('click', '.btn-close', function() {
        $downloadbar.animate({
            top: '-' + ($downloadbar.height() + 10)
        }, 350, function() {
            $downloadbar.fadeOut('fast', function() {
                $downloadbar.remove();
            });
        });
    });

    // Check Firefox version
    if (isFirefox()) {
        // data-latest-firefox includes point release information
        var latestFirefoxVersionFull = $html.attr('data-latest-firefox');

        // get latest full version (no point release info) for initial check
        var latestFirefoxVersion = parseInt(latestFirefoxVersionFull.split('.')[0], 10);

        if (isFirefoxUpToDate(latestFirefoxVersion + '')) {
            $html.addClass('firefox-latest');
        } else {
            $html.addClass('firefox-old');
        }
    }

    // Track product clicks
    $('.product-list').on('click', 'a', function(e) {
        var newTab = ($(this).target === '_blank' || e.metaKey || e.ctrlKey);
        var href = $(this).attr('href');
        var product = $(this).data('product');
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', '/firefox/products/ Interactions', 'product click', href]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', '/firefox/products/ Interactions', 'product click', href], callback);
        }
    });

    // Track download bar clicks
    $downloadbar.on('click', 'a', function(e) {
        var newTab = ($(this).target === '_blank' || e.metaKey || e.ctrlKey);
        var href = $(this).attr('href');
        var product = $(this).data('product');
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', '/firefox/products/ Interactions', 'Firefox downloads', href]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', '/firefox/products/ Interactions', 'Firefox downloads', href], callback);
        }
    });

})(window.jQuery);
