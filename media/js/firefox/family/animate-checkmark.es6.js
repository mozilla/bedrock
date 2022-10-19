/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import isSupported from './supports-intersection-observer.es6';
import isAllowed from './allows-motion.es6';

let _observer;
let _agreementChecklist;

const createObserver = () => {
    return new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target
                        .querySelectorAll('.has-animation')
                        .forEach(popInTab);
                    _observer.unobserve(entry.target);
                }
            });
        },
        { threshold: '0.4' }
    );
};

const popInTab = (tab) => {
    tab.classList.add('animate-pop-in');
    tab.addEventListener('animationend', (e) => drawCheckmark(e));
};

const drawCheckmark = (e) => {
    if (e.animationName === 'pop-in') {
        const checkbox = e.target.querySelector('[class^="checkmark"]');
        checkbox.classList.add('animate-checkmark');
    }
};

export const init = () => {
    if (isAllowed() && isSupported()) {
        _observer = createObserver();
        // add agreement observer
        _agreementChecklist = document.querySelector('.c-agreement svg');
        _observer.observe(_agreementChecklist);
    }
};
