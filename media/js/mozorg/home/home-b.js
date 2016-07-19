/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Waypoint) {
    'use strict';

    var mozClient = window.Mozilla.Client;

    var impactInnovationWaypoint;
    var firefoxWaypoint;

    var $surveyMsg;

    function handleWaypoint(target, callback) {
        return function(direction) {
            window.dataLayer.push({
                'event': 'scroll-section',
                'section': target
            });

            if (typeof callback === 'function') {
                callback(direction);
            }
        };
    }

    function toggleSurvey(direction) {
        if (direction === 'down') {
            // slide up when scrolling down
            $surveyMsg.addClass('stuck').css({ bottom: '-90px' }).animate({ bottom: '0' }, 500);
        } else if (direction === 'up') {
            // slide down when scrolling up, then unstick
            $surveyMsg.animate({ bottom: '-90px' }, 500, function() {
                $surveyMsg.removeClass('stuck');
            });
        }
    }

    function enableWaypoints() {
        impactInnovationWaypoint = new Waypoint({
            element: '#who-innovate-wrapper',
            handler: handleWaypoint('impact-innovation'),
            offset: '40%'
        });

        firefoxWaypoint = new Waypoint({
            element: '#firefox',
            handler: handleWaypoint('firefox', toggleSurvey),
            offset: '40%'
        });
    }

    // hide download button for up-to-date fx desktop/android users
    if ((mozClient.isFirefoxDesktop || mozClient.isFirefoxAndroid) && mozClient._isFirefoxUpToDate(false)) {
        $('#nav-download-firefox').css('display', 'none');
    }

    // show mobile download buttons if on mobile platform and not fx
    if (mozClient.isMobile && !mozClient.isFirefox) {
        $('#fxmobile-download-buttons').addClass('visible');
        $('#fx-download-link').addClass('hidden');
    }

    // set up waypoints if survey is present & media queries supported
    // must be in doc.ready as #survey-message is added in another script
    $(function() {
        var mqIsTablet;

        // test for matchMedia
        if ('matchMedia' in window) {
            mqIsTablet = matchMedia('(min-width: 760px)');
        }

        $surveyMsg = $('#survey-message');

        if ($surveyMsg.length && mqIsTablet) {
            if (mqIsTablet.matches) {
                enableWaypoints();
            }

            mqIsTablet.addListener(function(mq) {
                if (mq.matches) {
                    enableWaypoints();
                } else {
                    impactInnovationWaypoint.destroy();
                    firefoxWaypoint.destroy();

                    // reset survey positioning
                    $surveyMsg.css('bottom', '-90px').removeClass('stuck');
                }
            });
        }
    });
})(window.jQuery, window.Waypoint);
