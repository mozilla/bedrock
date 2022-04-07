/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const stickySideMenu = document.querySelector('.webvision-sidebar');
const globalFooter = document.querySelector('.c-footer');

const { scrollTop } = document.documentElement;

function checkOffSet() {
    function getRectTop(el) {
        const rect = el.getBoundingClientRect();
        return rect.top;
    }

    if (
        getRectTop(stickySideMenu) + scrollTop + stickySideMenu.offsetHeight >=
        getRectTop(globalFooter) + scrollTop
    ) {
        stickySideMenu.style.removeProperty('position');
        stickySideMenu.classList.add('mzp-c-sidemenu-absolute');
    }

    if (
        document.body.scrollTop + window.innerHeight <
        getRectTop(globalFooter) + document.body.scrollTop
    ) {
        stickySideMenu.classList.remove('mzp-c-sidemenu-absolute');
    }
}

document.addEventListener('scroll', function () {
    checkOffSet();
});
