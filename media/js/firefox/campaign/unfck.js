/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */


/*
    Twitter sharing
*/
(function() {
    'use strict';

    // Twitter share
    function openTwitterSubwin(url) {
        var width = 550;
        var height = 420;
        var options = {
            'scrollbars': 'yes',
            'resizable': 'yes',
            'toolbar': 'no',
            'location': 'yes',
            'width': width,
            'height': height,
            'top': screen.height > height ? Math.round((screen.height / 2) - (height / 2)) : 0,
            'left': Math.round((screen.width / 2) - (width / 2))
        };

        window.open(url, 'twitter_share', window._SearchParams.objectToQueryString(options).replace(/&/g, ',')).focus();
    }

    // FB Share
    function openFacebookSubwin(url) {
        open(url, 'fb_share', 'height=380,width=660,resizable=0,toolbar=0,menubar=0,status=0,location=0,scrollbars=0').focus();
    }

    function handleShareLinkClick(e) {
        var link_href = e.target.href;
        var service = '';

        if(link_href.indexOf('twitter') > -1) {
            openTwitterSubwin(link_href);
            service = 'twitter';
            e.preventDefault();
        } else if(link_href.indexOf('facebook') > -1) {
            openFacebookSubwin(link_href);
            service = 'facebook';
            e.preventDefault();
        }

        // Track the event in GA
        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'checklist',
            'eLabel': 'share to ' + service,
        });
    }

    function onLoad() {
        // Set up twitter link handler
        var tw = document.getElementById('js-tw');
        var tw_jack = document.getElementById('js-tw-jack');
        var fb = document.getElementById('js-fb');

        tw.addEventListener('click', handleShareLinkClick, false);
        tw_jack.addEventListener('click', handleShareLinkClick, false);
        fb.addEventListener('click', handleShareLinkClick, false);
    }

    window.Mozilla.run(onLoad);
})();

