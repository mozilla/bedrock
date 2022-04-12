/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const stickySideMenu = document.querySelector('.webvision-sidebar');
const globalFooter = document.querySelector('.c-footer');
// const footerStyle = window.getComputedStyle(globalFooter);
// console.log(footerStyle.getPropertyValue('height'))

// const { scrollTop } = stickySideMenu;

function checkOffSet() {
    // function getRectTop(el) {
    //     const rect = el.getBoundingClientRect();
    //     return rect.top;
    // }

    function isFooterInView(element) {
        const elementTop = element.offsetTop;
        const elementBottom = elementTop + element.offsetHeight;
        const viewportTop = window.scrollY || window.pageYOffset;
        const viewportBottom = viewportTop + window.screen.height;
        // console.log(elementBottom > viewportTop && elementTop < viewportBottom);
        // console.log(
        //     'element bottom:',
        //     elementBottom,
        //     'viewport top:',
        //     viewportTop,
        //     'element top:',
        //     elementTop,
        //     'viewport bottom:',
        //     viewportBottom
        // );
        return (
            (elementBottom > viewportTop) + element.offsetHeight &&
            elementTop < viewportBottom
        );
    }

    if (isFooterInView(globalFooter)) {
        // stickySideMenu.style.bottom = '540px';
        stickySideMenu.style.overflowY = 'auto';
        stickySideMenu.style.overflowX = 'hidden';
    } else {
        stickySideMenu.style.removeProperty('bottom');
        stickySideMenu.style.removeProperty('overflow-y');
        stickySideMenu.style.removeProperty('overflow-x');
    }

    // console.log(stickySideMenu.getBoundingClientRect().bottom, globalFooter.getBoundingClientRect().top, scrollTop)

    // stickySideMenu.getBoundingClientRect().bottom == globalFooter.getBoundingClientRect().top ? console.log(true) : console.log(false)

    // console.log(stickySideMenu.offsetHeight, stickySideMenu.getBoundingClientRect().top)

    // if (
    //     // getRectTop(stickySideMenu) + scrollTop + stickySideMenu.offsetHeight >=
    //     // getRectTop(globalFooter) + scrollTop
    //     stickySideMenu.getBoundingClientRect().bottom + scrollTop >=globalFooter.getBoundingClientRect().top
    // ) {
    //     stickySideMenu.style.bottom = globalFooter.offsetHeight;
    //     stickySideMenu.style.overflowY = "auto";
    //     stickySideMenu.style.overflowX = "hidden";
    //     // const positionAbs = document.querySelector('.mzp-c-sidemenu-absolute');
    // }

    // if (
    //     stickySideMenu.getBoundingClientRect().bottom < globalFooter.getBoundingClientRect().top
    // ) {
    //     // stickySideMenu.classList.remove('mzp-c-sidemenu-absolute');
    //     stickySideMenu.style.removeProperty('bottom');
    //     stickySideMenu.style.removeProperty('overflow-y');
    //     stickySideMenu.style.removeProperty('overflow-x');
    // }
}

document.addEventListener('scroll', function () {
    checkOffSet();
});
