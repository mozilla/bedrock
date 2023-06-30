/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let observer;
let heroSection;

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
                    }, 600);
                } else if (heroSection.contains(entry.target)) {
                    const heroWrapper =
                        entry.target.querySelector('.hero-wrapper');
                    const ctdLogo =
                        entry.target.querySelector('.ctd-animated-logo');
                    const imageWrapper =
                        entry.target.querySelector('.c-hero-top-images');
                    heroWrapper.classList.add('animate-pop-in');
                    heroWrapper.addEventListener('animationend', function () {
                        imageWrapper.classList.add('active');
                        ctdLogo.classList.add('animate-active');
                    });
                } else if (
                    entry.target.classList.contains('ctd-animated-logo')
                ) {
                    entry.target.classList.add('animate-active');
                } else {
                    entry.target.classList.add('animate-pop-in');
                }
            } else if (
                !entry.isIntersecting &&
                entry.target.classList.contains('ctd-animated-logo')
            ) {
                entry.target.classList.remove('animate-active');
            }
        });
    });
}

function init() {
    if (
        window.MzpSupports.intersectionObserver &&
        window.Mozilla.Utils.allowsMotion()
    ) {
        heroSection = document.querySelector('.c-ctd-hero');
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

        observer.observe(heroSection);

        const logo = document.querySelector(
            '.c-animated-button .ctd-animated-logo'
        );

        const mobileLogo = document.querySelector(
            '.ctd-mobile-banner .ctd-animated-logo'
        );

        // add animated logo to only animate while in view
        observer.observe(logo);
        observer.observe(mobileLogo);
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
