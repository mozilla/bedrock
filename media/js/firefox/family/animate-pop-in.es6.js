/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let _observer;

const isSupported = () => {
    return (
        'IntersectionObserver' in window &&
        'IntersectionObserverEntry' in window &&
        'intersectionRatio' in window.IntersectionObserverEntry.prototype &&
        window.NodeList &&
        NodeList.prototype.forEach
    );
};

const isAllowed = () => {
    return (
        window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: no-preference)').matches
    );
};

const createObserver = () => {
    return new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                // trigger animation by adding relevant class with animation styles
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-pop-in');
                    // remove target observer after triggering animation
                    _observer.unobserve(entry.target);
                }
            });
        },
        { threshold: '0.4' }
    );
};

export const init = () => {
    if (isAllowed && isSupported()) {
        _observer = createObserver();
        // add observers
        document.querySelectorAll('.c-browser').forEach(function (element) {
            _observer.observe(element);
        });
    }
};
