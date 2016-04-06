/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla) {
    'use strict';

    var client = Mozilla.Client;
    var helloAnimationStage = $('#hello-animation-stage');

    function triggerHelloAnimation() {
        helloAnimationStage.addClass('animate');
    }

    //Only run the tour if user is on Firefox 29 for desktop.
    if (client.isFirefoxDesktop && client.FirefoxMajorVersion >= 36) {

        // Query if the UITour API is working before we start the tour
        Mozilla.UITour.getConfiguration('sync', function () {

            var tour = new Mozilla.BrowserTour({
                id: $('#tour-page').data('telemetry'),
                helloPageId: 'hello-tour_OpenPanel_firstrun',
                allowScroll: true,
                onCloseTour: triggerHelloAnimation,
                onCompactTour: triggerHelloAnimation
            });

            tour.init();
        });
    }

})(window.jQuery, window.Mozilla);
