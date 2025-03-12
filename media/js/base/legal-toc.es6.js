/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let isSticky = false;
let resizeTimer;
const stickyTOC = {};
const sidebar = document.querySelector('.mzp-l-sidebar');
const sections = document.querySelectorAll(
    '.mzp-c-article .section1 .section2'
);
const sectionObserver = new IntersectionObserver(
    (sections) => {
        sections.forEach((section) => {
            const id = section.target.querySelector('h2').getAttribute('id');
            if (section.intersectionRatio > 0) {
                // try/catch because it errors if there's no matching selector
                try {
                    document
                        .querySelector(`.c-toc li a[href="#${id}"]`)
                        .parentElement.classList.add('active');
                    return true;
                } catch (e) {
                    return false;
                }
            } else {
                // try/catch because it errors if there's no matching selector
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

/**
 * Is the layout large enough to be 2 column?
 * @returns {Boolean}
 */
stickyTOC.isTwoColumn = () => {
    return getComputedStyle(sidebar).getPropertyValue('float') !== 'none';
};

/**
 * Is there enough vertical space for sticky behavior?
 * @returns {Boolean}
 */
stickyTOC.isTallEnough = () => {
    return sidebar.offsetHeight < window.innerHeight;
};

/**
 * Feature detect for sticky navigation
 * @returns {Boolean}
 */
stickyTOC.supportsSticky = () => {
    if (typeof window.MzpSupports !== 'undefined') {
        return (
            window.MzpSupports.classList &&
            window.MzpSupports.intersectionObserver &&
            window.MzpSupports.matchMedia &&
            CSS.supports('position', 'sticky')
        );
    } else {
        return false;
    }
};

/**
 * Add intersection observer & classes
 */
stickyTOC.createSticky = () => {
    if (!isSticky) {
        sidebar.classList.add('toc-is-sticky');
        sections.forEach((section) => {
            sectionObserver.observe(section);
        });
        isSticky = true;
    }
};

/**
 * Remove intersection observer & classes
 */
stickyTOC.destroySticky = () => {
    if (isSticky) {
        sidebar.classList.remove('toc-is-sticky');
        sidebar.querySelectorAll('.active').forEach((active) => {
            active.classList.remove('active');
        });
        sections.forEach((section) => {
            sectionObserver.unobserve(section);
        });
        isSticky = false;
    }
};

/**
 * Init sticky TOC if conditions are satisfied
 */
stickyTOC.initSticky = () => {
    const makeSticky = () => {
        if (
            stickyTOC.isTallEnough() &&
            stickyTOC.isTwoColumn() &&
            !matchMedia('(prefers-reduced-motion: reduce)').matches
        ) {
            stickyTOC.createSticky();
        } else {
            stickyTOC.destroySticky();
            return false;
        }
    };

    // react to window resizing
    if (stickyTOC.supportsSticky()) {
        makeSticky();
        window.addEventListener(
            'resize',
            function () {
                clearTimeout(resizeTimer);
                resizeTimer = setTimeout(makeSticky, 250);
            },
            true
        );
    }
};

window.addEventListener('DOMContentLoaded', () => {
    stickyTOC.initSticky();
});
