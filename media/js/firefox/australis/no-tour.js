;(function($, Mozilla) {
    'use strict';

    var client = Mozilla.Client;

    // Mozilla.UITour should run on Firefox 29 and above for Desktop only.
    if (client.isFirefoxDesktop && client.FirefoxMajorVersion >= 29) {
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
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'tour-visiblity',
                'syncVisibility': visible
            });
        });
    }

})(window.jQuery, window.Mozilla);
