/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var client = window.Mozilla.Client;

    var $html = $('html');
    var $shield = $('#tracking-protection-animation');
    var $tryPBButtons = $('.try-pb-button');
    var panels = ['tracking-protection', 'when-to-use', 'control-center', 'cta'];

    $.each(panels, function(index, value) {
        new Waypoint({
            element: document.getElementById(value),
            handler: function(direction) {
                if(direction === 'down') {
                    registerGA(value);
                }
            },
            offset: 'bottom-in-view'
        });
    });

    function registerGA(section) {
        window.dataLayer.push({
            event: 'private-browsing-page-interactions',
            interaction: 'scroll',
            section: section
        });
    }

    if (client.isFirefox) {
        // iOS
        if (client.isFirefoxiOS) {
            // all iOS users have private browsing
            $html.addClass('firefox-up-to-date');

            // update SUMO link
            $tryPBButtons.attr('href', 'https://support.mozilla.org/kb/private-browsing-firefox-ios');
        // Android or desktop
        } else {
            // desktop & Android version numbers match
            if (client.FirefoxMajorVersion >= 42)  {
                // try private browsing button is available
                $html.addClass('firefox-up-to-date');

                if (client.isFirefoxAndroid) {
                    // update SUMO link
                    $tryPBButtons.attr('href', 'https://support.mozilla.org/kb/private-browsing-firefox-android');
                } else {
                    // initialize UITour
                    Mozilla.HighlightTarget.init('.try-pb-button');

                    $tryPBButtons.attr('role', 'button').on('highlight-target', function() {
                        $shield.addClass('blocked');
                    });
                }
            } else {
                $html.addClass('firefox-old');
            }
        }
    } else {
        $html.addClass('non-firefox');
    }

})(window.jQuery);
