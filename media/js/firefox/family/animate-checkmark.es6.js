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

const createObserver = () => {
    return new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                // trigger animation by adding relevant class with animation styles
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-checkmark');
                    // remove target observer after triggering animation
                    _observer.unobserve(entry.target);
                }
            });
        },
        { threshold: '0.4' }
    );
};

export const init = () => {
    if (isSupported()) {
        _observer = createObserver();
        // add agreement observer
        const agreementChecklist = document.querySelector('.c-agreement svg');
        _observer.observe(agreementChecklist);
    }
};
