/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let observer;

function createObserver() {
    return new IntersectionObserver(function (entries) {
        let chain = Promise.resolve();
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                if (entry.target.classList.contains('mzp-c-picto')) {
                    // chain promises with a 200ms delay in between each one
                    chain = chain.then(() => popIn(entry.target));
                    // remove target observer after triggering animation
                    observer.unobserve(entry.target);
                } else if (entry.target.classList.contains('toggle')) {
                    const input = entry.target.querySelector('input');
                    setTimeout(() => {
                        entry.target.classList.add('animate-slide');
                        input.checked = true;
                    }, 250);
                } else {
                    entry.target.classList.add('animate-pop-in');
                }
            }
        });
    });
}

function init() {
    if (
        window.MzpSupports.intersectionObserver &&
        window.Mozilla.Utils.allowsMotion()
    ) {
        observer = createObserver();

        //add picto observers
        document
            .querySelectorAll('.c-ctd-features .mzp-c-picto')
            .forEach(function (element) {
                observer.observe(element);
            });

        // add middle toggle
        document.querySelectorAll('.toggle.middle').forEach(function (toggle) {
            observer.observe(toggle);
        });

        // add hero section (will this work? who knows!)
        const hero = document.querySelector('.hero-wrapper');
        observer.observe(hero);
    }
}

function popIn(element) {
    return new Promise((res) => {
        setTimeout(() => {
            element.classList.add('animate-pop-in');
            res();
        }, 200);
    });
}

init();
