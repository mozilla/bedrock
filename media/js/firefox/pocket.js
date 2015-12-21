/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla){
    'use strict';

    var $window = $(window);
    var $document = $(document);
    var $html = $(document.documentElement);

    var client = Mozilla.Client;
    var supportsPromises = 'Promise' in window;

    function closePocketMenu() {
        Mozilla.UITour.hideMenu('pocket');
        $document.off('click.pocket');
        $document.off('visibilitychange.pocket');
        $window.off('resize.pocket');
    }

    function handleVisibilityChange() {
        if (document.hidden) {
            closePocketMenu();
        }
    }

    function hasTarget(target) {
        return new Promise(function(resolve) {
            Mozilla.UITour.getConfiguration('availableTargets', function(config) {
                if (config.targets && $.inArray(target, config.targets) !== -1) {
                    resolve('available');
                } else {
                    resolve('not-available');
                }
            });
        });
    }

    function openPocketMenu(e) {
        e.preventDefault();

        hasTarget('pocket').then(function(result) {
            if (result === 'available') {
                Mozilla.UITour.showMenu('pocket');
                $document.one('click.pocket', closePocketMenu);
                $document.one('visibilitychange.pocket', handleVisibilityChange);
                $window.one('resize.pocket', closePocketMenu);
            } else {
                window.location = e.target.href;
            }
        });
    }

    if (supportsPromises && client.isFirefoxDesktop && client.FirefoxMajorVersion >= 38) {
        // only bind click event if UITour is working
        Mozilla.UITour.ping(function() {
            $('.try-pocket').on('click.pocket', openPocketMenu);

            // Add a class if Firefox is up to date
            $html.addClass('firefox-latest');

            // Add a class if Pocket is in the toolbar
            hasTarget('pocket').then(function(result) {
                if (result === 'available') {
                    $html.addClass('available');
                }
            });
        });
    }

})(window.jQuery, window.Mozilla);
