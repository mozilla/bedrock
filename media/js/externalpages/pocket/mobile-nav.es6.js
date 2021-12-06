/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const navOpenBtn = document.querySelector('.global-nav-mobile-menu-btn');
const mobileNavWrapper = document.querySelector('.mobile-nav-wrapper');
const mobileNav = document.querySelector('.mobile-nav');
const navCloseBtn = document.querySelector('.mobile-nav-close-btn');
const contentWrapper = document.querySelector('body');

const TAB = 9;
const ESC = 27;

function detectClickOutside(event) {
    if (!mobileNav.contains(event.target) && event.target !== navOpenBtn) {
        handleMenuClose();
    }
}

function handleMenuOpen() {
    mobileNavWrapper.classList.add('active');
    mobileNav.setAttribute('aria-expanded', true);
    contentWrapper.classList.add('mobile-nav-open');
    document.addEventListener('click', detectClickOutside);
    window.addEventListener('keydown', handleKeyDown);

    // move focus to close button when modal is opened, need to use setTimeout to get the animation working correctly
    setTimeout(function () {
        mobileNavWrapper.style.opacity = 1;
        mobileNav.classList.add('active');
        navCloseBtn.focus();
    }, 10);
}

function handleMenuClose() {
    mobileNav.classList.remove('active');
    mobileNav.setAttribute('aria-expanded', false);
    mobileNavWrapper.style.opacity = 0;
    document.removeEventListener('click', detectClickOutside);
    window.removeEventListener('keydown', handleKeyDown);

    // move focus to close button when modal is closed need to use setTimeout to get the animation working correctly
    setTimeout(function () {
        mobileNavWrapper.classList.remove('active');
        contentWrapper.classList.remove('mobile-nav-open');
        navCloseBtn.focus();
    }, 250);
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

    // function handleForwardTab(){}
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

navOpenBtn.addEventListener('click', handleMenuOpen, false);
navCloseBtn.addEventListener('click', handleMenuClose, false);
