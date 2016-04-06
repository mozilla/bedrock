/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* globals Promise */

(function(Mozilla, window, $) {
    'use strict';

    var $window = $(window);
    var $document = $(document);
    var client = Mozilla.Client;
    var $outerWrapper = $('#outer-wrapper');
    var $tryHelloButton = $('.try-hello-button');

    function shouldOpenHelloMenu() {
        // check for the browser channel info
        var appInfo = new Promise(function(resolve, reject) {
            Mozilla.UITour.getConfiguration('appinfo', function(config) {
                if (config && config.defaultUpdateChannel) {
                    resolve(config.defaultUpdateChannel);
                } else {
                    reject('UITour: defaultUpdateChannel property not found.');
                }
            });
        });

        // see if Hello is an available target in toolbar/overflow/customize menu
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
            Promise.all([appInfo, availableTargets]).then(function(results) {
                var channel = results[0];
                var targets = results[1];
                resolve(channel !== 'esr' && targets && targets.indexOf('loop') > -1);
            }, function(reason) {
                reject(reason);
            });
        });
    }

    function openHelloMenu() {
        Mozilla.UITour.showMenu('loop', function() {
            $document.one('click.hello', closeHelloMenu);
            $window.one('resize.hello', closeHelloMenu);
            $document.on('visibilitychange.hello', handleVisibilityChange);

            window.dataLayer.push({
                'event': 'hello-interactions',
                'category': '/hello interactions',
                'location': 'productPage',
                'browserAction': 'Open'
            });
        });
    }

    function closeHelloMenu() {
        Mozilla.UITour.hideMenu('loop');
        $document.off('click.hello');
        $document.off('visibilitychange.hello');
        $window.off('resize.hello');
    }

    function handleVisibilityChange() {
        if (document.hidden) {
            closeHelloMenu();
        }
    }

    function trackEligibleView() {
        shouldOpenHelloMenu().then(function(result) {
            var view = result ? 'EligibleView' : 'IneligibleView';
            window.dataLayer.push({
                'event': 'hello-interactions',
                'category': '/hello interactions',
                'location': 'productPage',
                'browserAction': view
            });
        });
    }

    function handleHelloButtonClick(e) {
        e.preventDefault();
        shouldOpenHelloMenu().then(function(result) {
            if (result) {
                openHelloMenu();
            } else {
                window.location = e.target.href;
            }
        }, function() {
            // if promise rejected then simply go to SUMO.
            window.location = e.target.href;
        });
    }

    function initHelloPage() {

        if (client.isFirefoxDesktop) {
            // The new Firefox Hello is available to Firefox 45 users and upward.
            if (client.FirefoxMajorVersion >= 45) {
                $outerWrapper.addClass('firefox-up-to-date');
                // ping UITour to make sure it's working before binding
                // click handlers.
                Mozilla.UITour.ping(function() {
                    $tryHelloButton.on('click', handleHelloButtonClick);
                    trackEligibleView();
                });
            } else {
                $outerWrapper.addClass('firefox-out-of-date');
            }
        } else if (client.isMobile) {
            $outerWrapper.addClass('mobile-device');
        } else {
            $outerWrapper.addClass('non-firefox');
        }

        // show fallback Hello wordmark for older browsers
        Mozilla.SVGImage.fallback();
    }

    initHelloPage();

})(window.Mozilla, window, window.jQuery);
