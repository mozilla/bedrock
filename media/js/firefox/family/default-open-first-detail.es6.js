/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import isSupported from './supports-intersection-observer.es6';
import isAllowed from './allows-motion.es6';

let _observer;
let _faqSection;

const createObserver = () => {
    return new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    // open first details section
                    const _firstDetail = _faqSection.querySelector('details');
                    if (_firstDetail) {
                        _firstDetail.setAttribute('open', '');
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
    // run only on larger screens
    if (
        isAllowed() &&
        isSupported() &&
        matchMedia('(min-width: 768px)').matches
    ) {
        _observer = createObserver();
        // sections with extra behaviour
        _faqSection = document.getElementById('faq');
        _observer.observe(_faqSection);
    }
};
