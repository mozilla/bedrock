/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// const stickySideMenu = document.querySelector('.webvision-sidebar');
// const footer = document.querySelector('.c-footer');

function checkOffSet() {
    // function getRectTop(el) {
    //     const rect = el.getBoundingClientRect();
    //     return rect.top;
    // }
    // function isFooterInView(element) {
    //     const elementTop = element.offsetTop;
    //     const elementBottom = elementTop + element.offsetHeight;
    //     const viewportTop = window.scrollY || window.pageYOffset;
    //     const viewportBottom = viewportTop + window.screen.height;
    //     return (
    //         (elementBottom > viewportTop) &&
    //         elementTop < viewportBottom
    //     );
    // }
    // if (stickySideMenu.getBoundingClientRect().bottom > footer.getBoundingClientRect().top) {
    //     stickySideMenu.style.bottom = '580px';
    //     stickySideMenu.style.overflowY = 'auto';
    //     stickySideMenu.style.overflowX = 'hidden';
    // } else if (stickySideMenu.getBoundingClientRect().bottom <= footer.getBoundingClientRect().top){
    //     stickySideMenu.style.removeProperty('bottom');
    //     stickySideMenu.style.removeProperty('overflow-y');
    //     stickySideMenu.style.removeProperty('overflow-x');
    // }
}

document.addEventListener('scroll', function () {
    checkOffSet();
});
