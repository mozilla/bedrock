/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla, $) {
    'use strict';

    var client = Mozilla.Client;
    var $tryButton = $('#try-it');
    var $pointer = $('.pointer');

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

    function openSearchUI(e) {
        e.preventDefault();
        Mozilla.UITour.openSearchPanel(function() {
            Mozilla.UITour.setSearchTerm('Batman vs Superman');
            $tryButton.addClass('hidden');
            $pointer.removeClass('hidden');
        });
    }

    function initSearchUI() {
        shouldPromoteYahooSearch().then(function() {
            $tryButton.removeClass('hidden');
            $tryButton.on('click', openSearchUI);
        });
    }

    function animateSearch() {
        $('.ravioli').addClass('animate');
    }

    function initPageVisible() {
        setTimeout(animateSearch, 500);

        window.dataLayer.push({
            'event': 'firstrun-interactions',
            'interaction': 'tab-visible'
        });
    }

    $(window).on('load', function() {
        // register first time tab becomes visible
        if (document.hidden) {
            $(document).one('visibilitychange.learnmore', initPageVisible);
        } else {
            initPageVisible();
        }
    });

    // getConfiguration('search') is only available in Firefox 43 and above.
    if (client.isFirefoxDesktop && client.FirefoxMajorVersion >= 43) {
        initSearchUI();
    }

})(window.Mozilla, window.jQuery);
