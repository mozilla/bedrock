;(function($, Mozilla) {
    'use strict';

    var helloAnimationStage = $('#hello-animation-stage');

    //track if this is the first time a user has seen tour
    function trackFirstTimeUse() {
        var firstTime = 'True';
        try {
            if (localStorage.getItem('mozUITourGlobalFlag') === 'taken') {
                firstTime = 'False';
            } else {
                localStorage.setItem('mozUITourGlobalFlag', 'taken');
            }
            gaTrack(['_trackEvent', 'Tour Interaction', 'First Time Seeing Tour', firstTime, 0, true]);
        } catch (e) {}
    }

    function triggerHelloAnimation() {
        helloAnimationStage.addClass('animate');
    }

    //Only run the tour if user is on Firefox 29 for desktop.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 36) {

        // Query if the UITour API is working before we start the tour
        Mozilla.UITour.getConfiguration('sync', function (config) {

            var tour = new Mozilla.BrowserTour({
                id: $('#tour-page').data('telemetry'),
                helloPageId: 'hello-tour_OpenPanel_firstrun',
                allowScroll: true,
                onCloseTour: triggerHelloAnimation,
                onCompactTour: triggerHelloAnimation
            });

            tour.init();

            trackFirstTimeUse();
        });
    }

})(window.jQuery, window.Mozilla);
