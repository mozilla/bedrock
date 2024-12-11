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
                if (entry.target.dataset.animation === 'pop-in') {
                    // chain promises with a 200ms delay in between each one
                    chain = chain.then(() => popIn(entry.target));
                    // remove target observer after triggering animation
                    observer.unobserve(entry.target);
                } else if (entry.target.dataset.animation === 'slide-in') {
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
        observer = createObserver();

        document
            .querySelectorAll("[data-animation='pop-in']")
            .forEach(function (element) {
                observer.observe(element);
            });

        document
            .querySelectorAll("[data-animation='slide-in']")
            .forEach(function (element) {
                observer.observe(element);
            });
    }
}

function popIn(element) {
    const dependents = element.querySelectorAll(
        "[data-animation='dependent-pop-in']"
    );

    // After main pop-in finishes, add delayed dependent pop-ins
    if (dependents.length !== 0) {
        element.addEventListener('animationend', () => {
            let chain = Promise.resolve();
            dependents.forEach((dependent) => {
                chain = chain.then(() => popIn(dependent));
            });
        });
    }

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
