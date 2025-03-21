/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function initBanner() {
    // if platform is ios or android
    if (
        /ios/.test(window.site.platform) ||
        /android/.test(window.site.platform)
    ) {
        // move the banner up to the top of main
        const mobileBanner = document.getElementById('mobile-banner');
        const desktopBanner = document.getElementById('desktop-banner');
        const container = desktopBanner.parentNode;
        container.insertBefore(mobileBanner, desktopBanner);
    }
}

function initScrollAnimations() {
    const supportsInsersectionObserver = (function () {
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
            const observer = new IntersectionObserver(function (entries) {
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
                    const rect = element.getBoundingClientRect();
                    const viewHeight = window.innerHeight;
                    // check element isn't above user's current position on the page
                    if (rect.top > viewHeight) {
                        element.classList.add('has-animate');
                        observer.observe(element);
                    }
                });
        }, 200);
    }
}

initBanner();
initScrollAnimations();
