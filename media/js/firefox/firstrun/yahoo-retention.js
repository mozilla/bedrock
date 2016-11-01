/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla, $) {
    'use strict';

    var client = Mozilla.Client;
    var $tryButton = $('#try-it');

    /**
     * Check the user has search input in their pallet and Yahoo! is
     * in their list of possible search providers.
     * @returns Promise (resolve) if both requirements are met.
     */
    function shouldPromoteYahooSearch() {

        var searchProviders = new Promise(function(resolve, reject) {
            Mozilla.UITour.getConfiguration('search', function(config) {
                if (config && config.engines) {
                    resolve(config.engines);
                } else {
                    reject('UITour: search engines array not found.');
                }
            });
        });

        var availableTargets = new Promise(function(resolve, reject) {
            Mozilla.UITour.getConfiguration('availableTargets', function(config) {
                if (config && config.targets) {
                    resolve(config.targets);
                } else {
                    reject('UITour: targets property not found.');
                }
            });
        });

        return new Promise(function(resolve, reject) {
            Promise.all([searchProviders, availableTargets]).then(function(results) {
                var engines = results[0];
                var targets = results[1];
                resolve(targets && targets.indexOf('search') > -1 && engines && engines.indexOf('searchEngine-yahoo') > -1);
            }, function(reason) {
                reject(reason);
            });
        });
    }

    function openFallbackPage() {
        window.location.href = $tryButton.attr('href');
    }

    function openSearchUI() {
        var timeout = setTimeout(openFallbackPage, 500);

        Mozilla.UITour.openSearchPanel(function() {
            clearTimeout(timeout);
            Mozilla.UITour.setSearchTerm('');
            window.dataLayer.push({
                'event': 'yh-click',
                'eventLabel': 'Yahoo Search Click'
            });
        });
    }

    function initSearchUI(e) {
        e.preventDefault();
        shouldPromoteYahooSearch().then(function(result) {
            if (result) {
                openSearchUI();
            } else {
                openFallbackPage();
            }
        }).catch(function() {
            openFallbackPage();
        });
    }

    // getConfiguration('search') is only available in Firefox 43 and above.
    if (client.isFirefoxDesktop && client.FirefoxMajorVersion >= 43) {
        $tryButton.on('click', initSearchUI);
    }

})(window.Mozilla, window.jQuery);
