;(function($, Mozilla) {
    'use strict';

    var firstTime = 'True';

    //Only run the tour if user is on Firefox 29 for desktop.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 29) {

        // add a callback when user finishes tour to update the cta
        // id is used for Telemetry
        var tour = new Mozilla.BrowserTour({
            id: 'australis-tour-whatsnew-29-release'
        });

        tour.init();

        // if user has Sync already, don't show the page prommo
        Mozilla.UITour.getConfiguration('sync', function (config) {
            var visible = '';

            if (config.setup === false) {
                // Show CTA if the user does not already have Sync
                $('.sync-cta').show();
                visible = 'YES';
            } else if (config.setup === true) {
                // Hide Sync section in post tour-page
                $('.main-container').addClass('hide-sync');
                // hide Sync link in last step of tour
                $('#sync-link').hide();
                visible = 'NO';
            }

            // Push custom GA variable to track Sync visibility
            gaTrack(['_setCustomVar', 6, 'Sync Visible', visible, 2]);
        });

        //track if this is the first time a user has seen any tour (firstrun or whatsnew)
        try {
            if (localStorage.getItem('mozUITourGlobalFlag') === 'taken') {
                firstTime = 'False';
            } else {
                localStorage.setItem('mozUITourGlobalFlag', 'taken');
            }
            gaTrack(['_trackEvent', 'Tour Interaction', 'First Time Seeing Tour', firstTime, 0, true]);
        } catch (e) {}
    }

})(window.jQuery, window.Mozilla);
