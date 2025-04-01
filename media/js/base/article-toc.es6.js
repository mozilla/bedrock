/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let isSticky = false;
let resizeTimer;
const stickyTOC = {};
const sidebar = document.querySelector('.mzp-l-sidebar');

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
            window.MzpSupports.matchMedia &&
            CSS.supports('position', 'sticky')
        );
    } else {
        return false;
    }
};

/**
 * Add class
 */
stickyTOC.createSticky = () => {
    if (!isSticky) {
        sidebar.classList.add('toc-is-sticky');
        isSticky = true;
    }
};

/**
 * Remove class
 */
stickyTOC.destroySticky = () => {
    if (isSticky) {
        sidebar.classList.remove('toc-is-sticky');
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
    if (sidebar) {
        stickyTOC.initSticky();
    }
});
