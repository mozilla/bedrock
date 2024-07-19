/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let observer;
let browser;
let stickyNote;

function createObserver() {
    return new IntersectionObserver(function (entries) {
        let chain = Promise.resolve();
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                if (entry.target.classList.contains('c-browser')) {
                    // chain promises with a 200ms delay in between each one
                    chain = chain.then(() => popIn(entry.target));
                    // remove target observer after triggering animation
                    observer.unobserve(entry.target);
                } else if (entry.target.classList.contains('c-attached')) {
                    slideIn(entry.target);
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
        browser = document.querySelector('.c-browser');
        stickyNote = document.querySelector('.c-attached');
        observer = createObserver();

        document.querySelectorAll('.c-browser').forEach(function (element) {
            observer.observe(element);
        });

        observer.observe(browser);
        observer.observe(stickyNote);
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

function slideIn(element) {
    return new Promise((res) => {
        setTimeout(() => {
            element.classList.add('animate-slide-in');
            res();
        }, 800);
    });
}

init();
