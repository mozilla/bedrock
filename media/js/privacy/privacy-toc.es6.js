/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

window.addEventListener('DOMContentLoaded', () => {
    // bail out if they don't support what we need
    if (
        window.MzpSupports === 'undefined' ||
        !window.MzpSupports.classList ||
        !window.MzpSupports.intersectionObserver
    ) {
        return false;
    }

    // define the observer
    const entryObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                const id = entry.target.querySelector('h2').getAttribute('id');
                if (entry.intersectionRatio > 0) {
                    try {
                        document
                            .querySelector(`.c-toc li a[href="#${id}"]`)
                            .parentElement.classList.add('active');
                        return true;
                    } catch (e) {
                        return false;
                    }
                } else {
                    try {
                        document
                            .querySelector(`.c-toc li a[href="#${id}"]`)
                            .parentElement.classList.remove('active');
                        return true;
                    } catch (e) {
                        return false;
                    }
                }
            });
        },
        {
            rootMargin: '-120px 0px'
        }
    );

    // get toc
    const viewport = document.getElementsByTagName('html')[0];
    const sidebar = document.querySelector('.mzp-l-sidebar');

    if (sidebar.offsetHeight < viewport.offsetHeight) {
        sidebar.classList.add('toc-is-sticky');

        // Track all sections
        document
            .querySelectorAll('.mzp-c-article .section1 .section2')
            .forEach((section) => {
                entryObserver.observe(section);
            });
    }
});
