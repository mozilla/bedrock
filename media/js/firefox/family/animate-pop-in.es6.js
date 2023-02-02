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
let _bullyingSection;

const createObserver = () => {
    return new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                // trigger animation by adding relevant class with animation styles
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-pop-in');
                    if (_heroSection.contains(entry.target)) {
                        const _lockupBox =
                            entry.target.querySelector('.lockup-white-box');
                        const _ctaBlurb =
                            _heroSection.querySelector('.c-blurb-container');
                        // pop-in "The" box
                        _lockupBox.classList.add('animate-pop-in');
                        // pop-in CTA blurb AFTER box animation ends
                        _lockupBox.addEventListener('animationend', () => {
                            _ctaBlurb.classList.add('animate-pop-in');
                        });
                    } else if (_privateModeSection.contains(entry.target)) {
                        // change background color and pop-in mask
                        entry.target
                            .querySelector('.c-browser-content')
                            .classList.add('mzp-t-dark');
                        entry.target
                            .querySelector('.c-private-mode-mask')
                            .classList.add('animate-pop-in');
                    } else if (_bullyingSection.contains(entry.target)) {
                        // animate the hearts
                        entry.target
                            .querySelector('.c-browser-content')
                            .classList.add('animate-hearts');
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
        _bullyingSection = document.querySelector('.c-bullying');
        // add hero observer
        const heroLockup = document.querySelector('.c-hero h1');
        _observer.observe(heroLockup);
        // add parental pro-tip
        document
            .querySelectorAll('.c-pro-tip h2, .c-pro-tip p')
            .forEach(function (element) {
                _observer.observe(element);
            });
        // add browser observers
        document.querySelectorAll('.c-browser').forEach(function (element) {
            _observer.observe(element);
        });
        // add bullying observer
        const heartsImage = document.querySelector('.hearts-image');
        _observer.observe(heartsImage);
    }
};
