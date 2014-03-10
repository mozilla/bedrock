;(function($, Mozilla) {
    'use strict';

    var isMobile = (/Android|Mobile|Tablet|Fennec/i).test(navigator.userAgent);
    var $giveTry = $('#give-it-a-try');
    var $learnMore = $('#learn-more');
    var $window = $(window);

    // Users who reach the last step of the tour get a different cta.
    function updateCTALinks () {
        $giveTry.hide();
        $learnMore.css('display', 'inline-block');
    }

    // Only run the tour if user is on Firefox 29 for desktop.
    if (window.isFirefox() && !isMobile && window.getFirefoxMasterVersion() >= 29) {

        // add a callback when user finishes tour to update the cta
        // id is used for Telemetry
        var tour = new Mozilla.BrowserTour({
            id: 'australis-tour-aurora-29.0a2',
            onTourComplete: updateCTALinks
        });

        // scroll to top of window for mask overlay
        if ($window.scrollTop() > 0) {
            $window.scrollTop(0);
        }

        // start the by showing the doorhanger.
        tour.init();

        // show in-page cta to restart the tour
        $giveTry.show().on('click', function (e) {
            e.preventDefault();
            tour.restartTour();
            gaTrack(['_trackEvent', 'whatsnew Page Interactions - New Firefox Tour', 'click', 'Give it a try']);
        });

        // track blue post-tour cta button
        $learnMore.on('click', function (e) {
            e.preventDefault();
            var href = this.href;
            var callback = function() {
                window.location = href;
            };
            gaTrack(['_trackEvent', 'whatsnew Page Interactions - New Firefox Tour', 'click', 'Learn More CTA'], callback);
        });
    }

})(window.jQuery, window.Mozilla);
