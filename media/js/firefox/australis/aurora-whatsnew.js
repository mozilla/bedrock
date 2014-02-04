;(function($, Mozilla) {
    'use strict';

    var isMobile = (/Android|Mobile|Tablet|Fennec/i).test(navigator.userAgent);
    var $survey = $('#survey-link');
    var $giveTry = $('#give-it-a-try');
    var $learnMore = $('#learn-more');
    var $window = $(window);

    // Users who reach the last step of the tour get a different survey
    // to users who don't complete or didn't start the tour.
    function updateCTALinks () {
        $survey.attr('href', 'https://www.surveygizmo.com/s3/1525011/firefox-29a-t');
        $giveTry.hide();
        $learnMore.css('display', 'inline-block');
    }

    // Open survey link in new window and track click
    function openSurvey (e) {
        e.preventDefault();
        window.open(this.href, '_blank');
        gaTrack(['_trackEvent', 'whatsnew Page Interactions - New Firefox Tour', 'survey link', this.href]);
    }

    // Only run the tour if user is on Firefox 29 for desktop.
    if (window.isFirefox() && !isMobile && window.getFirefoxMasterVersion() >= 29) {

        // add a callback when user finishes tour to swap the survey links
        var tour = new Mozilla.BrowserTour({
            onTourComplete: updateCTALinks
        });

        /*
         * Get Firefox Account Sync configuration.
         * This will be used to determine conditional messaging.
         * Note: Sync isn't being used in the first release,
         * but this callback acts as a useful way to only start
         * the tour is the API is working!
         */
        Mozilla.UITour.getSyncConfiguration(function (config) {

            // scroll to top of window for mask overlay
            if ($window.scrollTop() > 0) {
                $window.scrollTop(0);
            }

            // start the by showing the doorhanger.
            tour.init();

            // show the survey link and track clicks
            $survey.show().on('click', openSurvey);

            // show in-page cta to restart the tour
            $giveTry.show().on('click', function (e) {
                e.preventDefault();
                tour.restartTour();
                gaTrack(['_trackEvent', 'whatsnew Page Interactions - New Firefox Tour', 'click', 'Give it a try']);
            });
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
