;(function($, Mozilla) {
    'use strict';

    var client = Mozilla.Client;

    var $tourStrings = $('#strings');
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
        } catch (e) {}
    }

    function triggerHelloAnimation() {
        helloAnimationStage.addClass('animate');
    }

    //Only run the tour if user is on Firefox 29 for desktop.
    if (client.isFirefoxDesktop && client.FirefoxMajorVersion >= 36) {

        // Query if the UITour API is working before we start the tour
        Mozilla.UITour.getConfiguration('availableTargets', function (config) {

            // if Hello icon is not in the pallet, show alternate door-hanger text
            if (config.targets && $.inArray('loop', config.targets) === -1) {
                $tourStrings.data('title', $tourStrings.data('title-no-icon'));
                $tourStrings.data('text', $tourStrings.data('text-no-icon'));
            }

            var tour = new Mozilla.BrowserTour({
                id: $('#tour-page').data('telemetry'),
                helloPageId: 'hello-tour_OpenPanel_whatsnew',
                allowScroll: true,
                onCloseTour: triggerHelloAnimation,
                onCompactTour: triggerHelloAnimation
            });

            tour.init();

            trackFirstTimeUse();
        });
    }

})(window.jQuery, window.Mozilla);
