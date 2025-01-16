/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const MzpSideMenu = {};

MzpSideMenu.setAria = () => {
    const menu = document.querySelector('.mzp-c-sidemenu');
    const menuToggle = document.querySelector('.mzp-js-toggle');
    const menuExpanded =
        menu.classList.contains('mzp-is-active') === 'true' ? 'true' : 'false';

    menuToggle.setAttribute('tabindex', '0');
    menuToggle.setAttribute('role', 'button');
    menuToggle.setAttribute('aria-controls', 'sidebar-menu');
    menuToggle.setAttribute('aria-expanded', menuExpanded);
};

MzpSideMenu.removeAria = () => {
    const menuToggle = document.querySelector('.mzp-js-toggle');

    menuToggle.removeAttribute('tabindex');
    menuToggle.removeAttribute('role', 'button');
    menuToggle.removeAttribute('aria-controls');
    menuToggle.removeAttribute('aria-expanded');
};

MzpSideMenu.isMobileSideMenuVisible = () => {
    const mqWide = matchMedia('(max-width: 767px)');

    if (mqWide.matches) {
        MzpSideMenu.setAria();
    }

    function handleMqChange(mq) {
        if (mq.matches) {
            MzpSideMenu.setAria();
        } else {
            MzpSideMenu.removeAria();
        }
    }

    if (window.matchMedia('all').addEventListener) {
        // evergreen
        mqWide.addEventListener('change', handleMqChange, false);
    } else if (window.matchMedia('all').addListener) {
        // IE fallback
        mqWide.addListener(handleMqChange);
    }
};

MzpSideMenu.init = () => {
    const menu = document.querySelector('.mzp-c-sidemenu');
    const menuMain = document.querySelector('.mzp-c-sidemenu-main');
    const menuToggle = document.querySelector('.mzp-js-toggle');

    if (menu && menuMain && menuToggle) {
        // Add aria states for mobile side menu.
        MzpSideMenu.isMobileSideMenuVisible();

        // Toggle the sidebar menu
        menuToggle.addEventListener(
            'click',
            (e) => {
                e.preventDefault();
                menu.classList.toggle('mzp-is-active');

                const menuExpanded =
                    menuToggle.getAttribute('aria-expanded') === 'true'
                        ? 'false'
                        : 'true';
                menuToggle.setAttribute('aria-expanded', menuExpanded);
            },
            false
        );
    }
};

module.exports = MzpSideMenu;
