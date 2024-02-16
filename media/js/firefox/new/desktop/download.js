/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/*
    mobile banner
    - on mobile, move the mobile banner to the top of the main content area
*/
(function () {
    'use strict';

    // if platform is ios or android
    if (
        /ios/.test(window.site.platform) ||
        /android/.test(window.site.platform)
    ) {
        // move the banner up to the top of main
        var mobileBanner = document.getElementById('mobile-banner');
        var desktopBanner = document.getElementById('desktop-banner');
        var container = desktopBanner.parentNode;
        container.insertBefore(mobileBanner, desktopBanner);
    }
})();

/*
    comparison chart
    - show a comparison to the users current browser or their operating system default
    - add button listeners to allow changing
*/
(function () {
    'use strict';

    var cells = {
        all: document.querySelectorAll('#compare-table tr > *:nth-child(1n+3)'),
        chrome: document.querySelectorAll('#compare-table tr *:nth-child(3)'),
        edge: document.querySelectorAll('#compare-table tr *:nth-child(4)'),
        safari: document.querySelectorAll('#compare-table tr *:nth-child(5)')
    };
    var buttons = document.querySelectorAll('.c-compare-button');
    var ua = navigator.userAgent;
    var compareTo = (function () {
        if (/MSIE|Trident/i.test(ua)) {
            return 'edge';
        }

        if (/Edg|Edge/i.test(ua)) {
            return 'edge';
        }

        if (/Chrome/.test(ua)) {
            return 'chrome';
        }

        // got this far without picking, now choose based on OS
        // could be Firefox/Safari/Brave/Opera/Android Browser/etc.

        if (/osx/.test(window.site.platform)) {
            return 'safari';
        }

        if (/windows/.test(window.site.platform)) {
            return 'edge';
        }

        if (/android/.test(window.site.platform)) {
            return 'chrome';
        }

        return 'chrome';
    })();

    // display chosen browser
    function show(browser) {
        // hide all comparisons
        for (var i = 0; i < cells['all'].length; ++i) {
            cells['all'][i].style.display = 'none';
        }

        // show the chosen comparison
        for (var j = 0; j < cells[browser].length; ++j) {
            cells[browser][j].style.display = 'table-cell';
        }

        // add active state to button
        for (var k = 0; k < buttons.length; ++k) {
            if (buttons[k].value === browser) {
                buttons[k].setAttribute('aria-pressed', true);
            } else {
                buttons[k].setAttribute('aria-pressed', false);
            }
        }
    }

    // match user's browser to start
    show(compareTo);

    // listen to buttons
    for (var l = 0; l < buttons.length; ++l) {
        buttons[l].addEventListener('click', function (event) {
            show(event.target.value);
        });
    }
})();

/*
    system requirements
    - add target to link so they go to their system's requirements
*/
(function () {
    'use strict';

    var sys = document.getElementById('system-requirements');
    var href = sys.getAttribute('href');

    if (/windows/.test(window.site.platform)) {
        sys.href = href + '#windows';
    } else if (/osx/.test(window.site.platform)) {
        sys.href = href + '#mac';
    } else if (/linux/.test(window.site.platform)) {
        sys.href = href + '#linux';
    }
})();

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

        // UA
        window.dataLayer.push({
            event: 'in-page-interaction',
            eAction: 'link click',
            eLabel: 'See your protection report'
        });
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
