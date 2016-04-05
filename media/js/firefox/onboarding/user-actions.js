/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla, $) {
    'use strict';

    var client = Mozilla.Client;

    // *************
    // pin it/search variation
    // *************
    var $trySearch = $('#search-now');
    var $searchPointer = $('#search-pointer');

    // as this is for firstrun, search should almost certainly be available
    // best to double check though
    function shouldPromoteSearch() {
        return new Promise(function(resolve, reject) {
            Mozilla.UITour.getConfiguration('availableTargets', function(config) {
                if (config && config.targets && config.targets.indexOf('search') > -1) {
                    resolve(true);
                } else {
                    reject('UITour: search target not found.');
                }
            });
        });
    }

    function openSearchUI(e) {
        e.preventDefault();

        Mozilla.UITour.openSearchPanel(function() {
            Mozilla.UITour.setSearchTerm('What is the weather?');
            $trySearch.addClass('hidden');
            $searchPointer.removeClass('hidden');
        });
    }

    function initSearchUI() {
        shouldPromoteSearch().then(function() {
            $trySearch.removeClass('hidden');
            $trySearch.on('click', openSearchUI);
        });
    }

    // only 45+ desktop should hit this page, but safer to double check
    if (client.isFirefoxDesktop) {
        // ensure UITour is open for business
        Mozilla.UITour.ping(function() {
            initSearchUI();
        });
    }

    // *************
    // mobile/privacy variation
    // *************
    var $tryPB = $('#try-pb');

    if (client.FirefoxMajorVersion >= 42)  {
        // initialize UITour
        Mozilla.HighlightTarget.init('#try-pb');

        $tryPB.attr('role', 'button');
    }
})(window.Mozilla, window.jQuery);
