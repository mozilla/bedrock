;(function($, Mozilla) {
    'use strict';

    window.dataLayer = window.dataLayer || [];

    var client = Mozilla.Client;
    var firstTime = 'True';

    // GA tracking for Firstrun tests
    // https://bugzilla.mozilla.org/show_bug.cgi?id=1128726
    // should be removed after 2/24/2015
    if (window.location.search.indexOf('f=34') > -1) {
        window.dataLayer.push({
            'event': 'firstrun-optimization',
            'testVaration': 'variation 1'
        });
    }

    //Only run the tour if user is on Firefox 29 for desktop.
    if (client.isFirefoxDesktop && client.FirefoxMajorVersion >= 29) {

        // Query if the UITour API is working before we start the tour
        Mozilla.UITour.getConfiguration('sync', function (config) {
            var visible = '';

            // if user has submitted newsletter don't show the tour again
            if (window.location.hash !== '#footer-email-form') {
                // add a callback when user finishes tour to update the cta
                // id is used for Telemetry
                var tour = new Mozilla.BrowserTour({
                    id: $('#tour-page').data('telemetry')
                });

                tour.init();
            }

            // if user has Sync already, don't show the page prommo
            if (config.setup === false) {
                visible = 'YES';
            } else if (config.setup === true) {
                visible = 'NO';
            }

            // Push custom GA variable to track Sync visibility
            window.dataLayer.push({
                'event': 'set-sync-visibility',
                'syncVisibility': visible
            });
        });

        //track if this is the first time a user has seen any tour (firstrun or whatsnew)
        try {
            if (localStorage.getItem('mozUITourGlobalFlag') === 'taken') {
                firstTime = 'False';
            } else {
                localStorage.setItem('mozUITourGlobalFlag', 'taken');
            }

            window.dataLayer.push({
                'event': 'first-run',
                'isFirstRun': firstTime
            });
        } catch (e) {}

        // track default search engine for Firefox 34
        if (client.FirefoxMajorVersion >= 34) {
            Mozilla.UITour.getConfiguration('selectedSearchEngine', function (data) {
                var selectedEngineID = data.searchEngineIdentifier;

                if (!selectedEngineID) {
                    return;
                }

                if (selectedEngineID === 'yahoo') {
                    Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'firstrun_yahooDefault');
                    Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ViewPage');
                    window.dataLayer.push({
                        'event': 'search-change-interaction',
                        'searchEngine': 'yahooDefault'
                    });
                } else {
                    Mozilla.UITour.setTreatmentTag('srch-chg-treatment', 'firstrun_otherDefault');
                    Mozilla.UITour.setTreatmentTag('srch-chg-action', 'ViewPage');
                    window.dataLayer.push({
                        'event': 'search-change-interaction',
                        'searchEngine': 'otherDefault'
                    });
                }
            });
        }

    }

})(window.jQuery, window.Mozilla);
