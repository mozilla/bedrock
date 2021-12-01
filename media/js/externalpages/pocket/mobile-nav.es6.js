/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const hamburgerBtn = document.querySelector('.global-nav-mobile-menu-btn');

const mobileNav = document.querySelector('.mobile-nav-wrapper');

function handleMenuOpen() {
    mobileNav.classList.add('.active');
}

hamburgerBtn.addEventListener('click', handleMenuOpen, false);
