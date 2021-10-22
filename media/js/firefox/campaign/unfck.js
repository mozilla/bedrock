/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/*
    Image lazy loading
*/
(function () {
    'use strict';

    /**
     * Safari on iOS and macOS does not yet support loading="lazy", so make sure that images
     * with display: none; in CSS are not loaded wastefully.
     */
    var isFirefox = document
        .getElementsByTagName('html')[0]
        .classList.contains('is-firefox');
    var lazyImages = document.querySelectorAll('.c-item-gif');

    if (isFirefox) {
        lazyImages = document.querySelectorAll(
            '.c-section-unfck-list.cc-firefox .c-item-gif'
        );
    } else {
        lazyImages = document.querySelectorAll(
            '.c-section-unfck-list.cc-default .c-item-gif'
        );
    }

    for (var i = 0; i < lazyImages.length; i++) {
        var sources = lazyImages[i].childNodes;

        for (var j = 0; j < sources.length; j++) {
            // skip text nodes
            if (sources[j].nodeType === 3) {
                continue;
            }
            if (sources[j].hasAttribute('data-srcset')) {
                sources[j].srcset = sources[j].getAttribute('data-srcset');
            } else if (sources[j].hasAttribute('data-src')) {
                sources[j].src = sources[j].getAttribute('data-src');
            }
        }
    }
})();

/*
    Twitter sharing
*/
(function () {
    'use strict';

    // Twitter share
    function openTwitterSubwin(url) {
        var width = 550;
        var height = 420;
        var options = {
            scrollbars: 'yes',
            resizable: 'yes',
            toolbar: 'no',
            location: 'yes',
            width: width,
            height: height,
            top:
                screen.height > height
                    ? Math.round(screen.height / 2 - height / 2)
                    : 0,
            left: Math.round(screen.width / 2 - width / 2)
        };

        window
            .open(
                url,
                'twitter_share',
                window._SearchParams
                    .objectToQueryString(options)
                    .replace(/&/g, ',')
            )
            .focus();
    }

    // FB Share
    function openFacebookSubwin(url) {
        open(
            url,
            'fb_share',
            'height=380,width=660,resizable=0,toolbar=0,menubar=0,status=0,location=0,scrollbars=0'
        ).focus();
    }

    function handleShareLinkClick(e) {
        var linkHref = e.target.href;
        var service = '';

        if (linkHref.indexOf('twitter') > -1) {
            openTwitterSubwin(linkHref);
            service = 'twitter';
            e.preventDefault();
        } else if (linkHref.indexOf('facebook') > -1) {
            openFacebookSubwin(linkHref);
            service = 'facebook';
            e.preventDefault();
        }

        // Track the event in GA
        window.dataLayer.push({
            event: 'in-page-interaction',
            eAction: 'share',
            eLabel: 'share to ' + service
        });
    }

    function onLoad() {
        // Set up twitter link handler
        var tw = document.getElementById('js-tw');
        var fb = document.getElementById('js-fb');

        tw.addEventListener('click', handleShareLinkClick, false);
        fb.addEventListener('click', handleShareLinkClick, false);
    }

    window.Mozilla.run(onLoad);
})();
