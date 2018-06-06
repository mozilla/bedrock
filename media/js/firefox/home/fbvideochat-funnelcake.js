/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function ($, Mozilla, Waypoint, dataLayer) {
    'use strict';

    var $fbVideochatBanner;

    var ieRegex = /MSIE|Trident|Edge/i;
    var isIE = ieRegex.test(window.navigator.userAgent);

    var fbRegex = /facebook\.com/i;
    var isFromFb = fbRegex.test(document.referrer);

    var hasCookies = typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled();

    if (hasCookies && window.site.platform === 'windows' && isFromFb && isIE) {
        // make sure visitor hasn't previously dismissed the banner
        var wasDismissed = Mozilla.Cookies.getItem('fbvideochat-banner-dismiss');

        if (wasDismissed === null) {
            $fbVideochatBanner = $('#fbvideochat-banner');

            // allow browser to laod the images
            $('.delay-load').each(function(i, img) {
                var $img = $(img);
                $img.attr('src', $img.data('src'));
                $img.attr('srcset', $img.data('srcset') + ' 1.5x');
                $img.removeAttr('data-src data-srcset').removeClass('delay-load');
            });

            // append funnelcake ID to Windows download links
            $('#download-fbvideochat').find('.os_win a, .os_win64 a').each(function(i, aTag) {
                aTag.href += '?f=134';
            });

            $('#fbvideochat-close').one('click', function() {
                // don't show the banner again for 7 days
                var d = new Date();
                d.setTime(d.getTime() + (7 * 24 * 60 * 60 * 1000));
                Mozilla.Cookies.setItem('fbvideochat-banner-dismiss', true, d.toUTCString(), '/');

                $fbVideochatBanner.slideUp('fast', function() {
                    // reset trigger point of sub nav
                    Waypoint.refreshAll();

                    dataLayer.push({
                        'eLabel': 'Banner Dismissal',
                        'data-banner-name': 'facebook-video-chat',
                        'data-banner-dismissal': '1',
                        'event': 'in-page-interaction'
                    });
                });
            });

            // slight delay before sliding down the banner
            setTimeout(function() {
                $fbVideochatBanner.slideDown(400, function() {
                    // reset trigger point of sub nav
                    Waypoint.refreshAll();

                    dataLayer.push({
                        'eLabel': 'Banner Impression',
                        'data-banner-name': 'facebook-video-chat',
                        'data-banner-impression': '1',
                        'event': 'non-interaction'
                    });
                });
            }, 500);
        }
    }
})(window.jQuery, window.Mozilla, window.Waypoint, window.dataLayer || []);
