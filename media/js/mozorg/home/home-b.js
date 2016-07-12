/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Waypoint) {
    'use strict';

    var mozClient = window.Mozilla.Client;

    var surveyWaypoint;
    var $surveyMsg;

    var $toggleInnovate = $('.toggle-innovate');
    var $toggleWho = $('.toggle-who');
    var $whoInnovateWrapper = $('#who-innovate-wrapper');
    var $who = $('#who');
    var $innovate = $('#innovate');

    function trackCollapseExpand(name, action) {
        window.dataLayer.push({
            'event': 'widget-action',
            'widget-name': name,
            'widget-action': action
        });
    }

    function enableWaypoints() {
        surveyWaypoint = new Waypoint({
            element: '#firefox',
            handler: function(direction) {
                if (direction === 'down') {
                    // slide up when scrolling down
                    $surveyMsg.addClass('stuck').css({ bottom: '-90px' }).animate({ bottom: '0' }, 500);
                } else if (direction === 'up') {
                    // slide down when scrolling up, then unstick
                    $surveyMsg.animate({ bottom: '-90px' }, 500, function() {
                        $surveyMsg.removeClass('stuck');
                    });
                }
            },
            offset: '60%'
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

    $toggleWho.on('click', function() {
        $whoInnovateWrapper.toggleClass('open-who');
        $who.toggleClass('open');

        trackCollapseExpand('Our Impact', $who.hasClass('open') ? 'Expose' : 'Close');
    });

    $toggleInnovate.on('click', function() {
        $whoInnovateWrapper.toggleClass('open-innovate');
        $innovate.toggleClass('open');

        trackCollapseExpand('Our Innovations', $innovate.hasClass('open') ? 'Expose' : 'Close');
    });

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
                    surveyWaypoint.destroy();

                    // reset survey positioning
                    $surveyMsg.css('bottom', '-90px').removeClass('stuck');
                }
            });
        }
    });
})(window.jQuery, window.Waypoint);
