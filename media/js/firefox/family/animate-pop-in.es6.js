/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import isSupported from './supports-intersection-observer.es6';
import isAllowed from './allows-motion.es6';

let _observer;
let _heroSection;
let _privateModeSection;

const createObserver = () => {
    return new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                // trigger animation by adding relevant class with animation styles
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-pop-in');
                    if (_heroSection.contains(entry.target)) {
                        // pop-in "The" box
                        entry.target
                            .querySelector('.lockup-white-box')
                            .classList.add('animate-pop-in');
                    } else if (_privateModeSection.contains(entry.target)) {
                        // change background color and pop-in mask
                        entry.target
                            .querySelector('.c-browser-content')
                            .classList.add('mzp-t-dark');
                        entry.target
                            .querySelector('.c-private-mode-mask')
                            .classList.add('animate-pop-in');
                    }
                    // remove target observer after triggering animation
                    _observer.unobserve(entry.target);
                }
            });
        },
        { threshold: '0.4' }
    );
};

export const init = () => {
    if (isAllowed() && isSupported()) {
        _observer = createObserver();
        // sections with extra behaviour
        _heroSection = document.querySelector('.c-hero');
        _privateModeSection = document.querySelector('.c-private-mode');
        // add hero observer
        const heroLockup = document.querySelector('.c-hero h1');
        _observer.observe(heroLockup);
        // add browser observers
        document.querySelectorAll('.c-browser').forEach(function (element) {
            _observer.observe(element);
        });
    }
};
