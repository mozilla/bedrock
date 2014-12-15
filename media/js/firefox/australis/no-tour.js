;(function($, Mozilla) {
    'use strict';

    // Mozilla.UITour should run on Firefox 29 and above for Desktop only.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 29) {
        // Register page id for Telemetry
        Mozilla.UITour.registerPageID($('#tour-page').data('telemetry'));

        // if user has Sync already, don't show the page prommo
        Mozilla.UITour.getConfiguration('sync', function (config) {
            var visible = '';

            if (config.setup === false) {
                visible = 'YES';
            } else if (config.setup === true) {
                visible = 'NO';
            }

            // Push custom GA variable to track Sync visibility
            gaTrack(['_setCustomVar', 6, 'Sync Visible', visible, 2]);
            gaTrack(['_trackEvent', 'Tour Visibility', 'on load', 'No Tour Visible', 0, 1]);
        });
    }

})(window.jQuery, window.Mozilla);
