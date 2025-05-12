/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/*
    scroll animations
    - add class to animate
    - add observer to trigger animations
*/
(function () {
    'use strict';

    var supportsInsersectionObserver = (function () {
        return (
            'IntersectionObserver' in window &&
            'IntersectionObserverEntry' in window &&
            'intersectionRatio' in window.IntersectionObserverEntry.prototype
        );
    })();

    // check for support
    if (
        supportsInsersectionObserver &&
        window.NodeList &&
        NodeList.prototype.forEach
    ) {
        // needs a sec to report rect.top right if the page loaded partially scrolled already
        setTimeout(function () {
            // define observer behaviour
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        // trigger animation
                        entry.target.classList.add('is-animated');
                        // remove observer after triggering animation
                        observer.unobserve(entry.target);
                    }
                });
            });

            // add observers
            document
                .querySelectorAll('.js-animate')
                .forEach(function (element) {
                    var rect = element.getBoundingClientRect();
                    var viewHeight = window.innerHeight;
                    // check element isn't above user's current position on the page
                    if (rect.top > viewHeight) {
                        element.classList.add('has-animate');
                        observer.observe(element);
                    }
                });
        }, 200);
    }
})();

/*
    protection report button
    - check for support
    - add listener, enable, and show button
*/
(function (Mozilla) {
    'use strict';

    var client = Mozilla.Client;

    function handleOpenProtectionReport(e) {
        e.preventDefault();

        // GA4
        window.dataLayer.push({
            event: 'widget_action',
            type: 'protection report',
            action: 'open',
            label: 'See your protection report'
        });

        Mozilla.UITour.showProtectionReport();
    }

    if (client.isFirefoxDesktop) {
        if (client._getFirefoxMajorVersion() >= 70) {
            // show "See what Firefox has blocked for you" links.
            document
                .querySelector('body')
                .classList.add('state-firefox-desktop-70');

            // Intercept link clicks to open about:protections page using UITour.
            Mozilla.UITour.ping(function () {
                document
                    .getElementById('protection-report')
                    .addEventListener(
                        'click',
                        handleOpenProtectionReport,
                        false
                    );
            });
        }
    }
})(window.Mozilla);
