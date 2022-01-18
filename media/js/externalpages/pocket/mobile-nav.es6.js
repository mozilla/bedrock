/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

let navOpenBtn;
let mobileNavWrapper;
let mobileNav;
let navCloseBtn;
let contentWrapper;

const TAB = 9;
const ESC = 27;

function detectClickOutside(event) {
    if (!mobileNav.contains(event.target) && event.target !== navOpenBtn) {
        handleMenuClose();
    }
}

function toggleContentWrapperClass(e) {
    if (e.target === mobileNavWrapper) {
        contentWrapper.classList.toggle('mobile-nav-open');
    }
}

function handleMenuOpen() {
    mobileNavWrapper.classList.add('active');
    mobileNavWrapper.style.opacity = 1;
    mobileNav.classList.add('active');
    navOpenBtn.setAttribute('aria-expanded', true);

    document.addEventListener('click', detectClickOutside);
    window.addEventListener('keydown', handleKeyDown);

    navCloseBtn.focus();
}

function handleMenuClose() {
    mobileNav.classList.remove('active');
    mobileNavWrapper.classList.remove('active');
    mobileNavWrapper.style.opacity = 0;
    navOpenBtn.setAttribute('aria-expanded', false);

    document.removeEventListener('click', detectClickOutside);
    window.removeEventListener('keydown', handleKeyDown);

    navOpenBtn.focus();
}

function handleKeyDown(e) {
    const focusableElements = Array.prototype.slice.call(
        mobileNav.querySelectorAll(
            'a[href], button:not([disabled]), [tabindex="0"]'
        )
    );

    function handleBackwardTab() {
        if (document.activeElement === focusableElements[0]) {
            e.preventDefault();
            focusableElements[focusableElements.length - 1].focus();
        } else {
            e.preventDefault();
            focusableElements[
                focusableElements.indexOf(document.activeElement) - 1
            ].focus();
        }
    }
    function handleForwardTab() {
        if (
            document.activeElement ===
            focusableElements[focusableElements.length - 1]
        ) {
            e.preventDefault();
            focusableElements[0].focus();
        } else {
            e.preventDefault();
            focusableElements[
                focusableElements.indexOf(document.activeElement) + 1
            ].focus();
        }
    }

    switch (e.keyCode) {
        case TAB:
            if (e.shiftKey) {
                handleBackwardTab();
            } else {
                handleForwardTab();
            }
            break;
        case ESC:
            handleMenuClose();
            break;
        default:
            break;
    }
}

const init = function () {
    // set element references
    navOpenBtn = document.querySelector('.global-nav-mobile-menu-btn');
    mobileNavWrapper = document.querySelector('.mobile-nav-wrapper');
    mobileNav = document.querySelector('.mobile-nav');
    navCloseBtn = document.querySelector('.mobile-nav-close-btn');
    contentWrapper = document.querySelector('body');

    // add event listeners
    navOpenBtn.addEventListener('click', handleMenuOpen, false);
    navCloseBtn.addEventListener('click', handleMenuClose, false);
    // this event is used both for styling and as a test condition
    mobileNavWrapper.addEventListener(
        'transitionend',
        toggleContentWrapperClass,
        { capture: true }
    );
};

export default init;
