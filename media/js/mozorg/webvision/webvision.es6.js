/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const stickySideMenu = document.querySelector('.mzp-c-sidemenu-main');
const globalFooter = document.querySelector('.c-footer');

// const mainArticleWrapper = document.querySelector('.c-webvision-article-full');

const sideBarWrapper = document.querySelector('.mzp-l-sidebar');

function checkOffSet() {
    function getRectTop(el) {
        const rect = el.getBoundingClientRect();
        return rect.top;
    }
    if (
        getRectTop(stickySideMenu) +
            document.body.scrollTop +
            stickySideMenu.offsetHeight >=
        getRectTop(globalFooter) + document.body.scrollTop - 100
    ) {
        stickySideMenu.style.position = 'absolute';
    }

    if (
        document.body.scrollTop + window.innerHeight <
        getRectTop(globalFooter) + document.body.scrollTop
    ) {
        stickySideMenu.style.position = 'fixed';
    }
}

document.addEventListener('scroll', function () {
    checkOffSet();
});

const output = document.querySelector('#output');

sideBarWrapper.addEventListener('scroll', function () {
    output.textContent = `scrollTop: ${sideBarWrapper.scrollTop}`;
});
