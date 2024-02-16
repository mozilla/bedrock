/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { init } from '../../../../media/js/pocket/mobile-nav.es6';

describe('mobile-nav.js', () => {
    const mobileNav = `<div class="mobile-nav-wrapper" tabindex="-1">
        <nav class="mobile-nav">
            <div>
                <button class="mobile-nav-close-btn"></button>
            </div>
            <ul>
                <li>
                    <a href="#first">1</a>
                </li>
                <li>
                    <a href="#last">2</a>
                </li>
            </ul>
        </nav>
    </div>
    <button class="global-nav-mobile-menu-btn"></button>`;

    const TAB = 9;
    const ESC = 27;

    beforeEach(function () {
        jasmine.clock().install();
        document.body.insertAdjacentHTML('afterbegin', mobileNav);
        init();
        const navOpenBtn = document.querySelector(
            '.global-nav-mobile-menu-btn'
        );
        navOpenBtn.click();
        // need to move past timeout in handleOpenMenu before testing focused element
        jasmine.clock().tick(500);
    });

    afterEach(function () {
        document.querySelector('.mobile-nav-wrapper').remove();
        document.querySelector('.global-nav-mobile-menu-btn').remove();
        jasmine.clock().uninstall();
    });

    it('should move focus onto close button inside the mobile menu when opened', function () {
        const mobileMenuWrapper = document.querySelector('.mobile-nav-wrapper');
        expect(document.activeElement).toBe(
            mobileMenuWrapper.querySelector('.mobile-nav-close-btn')
        );
    });

    it('should keep focus in mobile menu while open', function () {
        const keydownForward = new KeyboardEvent('keydown', {
            keyCode: TAB
        });
        const keydownBackward = new KeyboardEvent('keydown', {
            keyCode: TAB,
            shiftKey: true
        });

        // tab around
        expect(document.activeElement).toBe(
            document.querySelector('.mobile-nav-close-btn')
        );
        dispatchEvent(keydownBackward);
        expect(document.activeElement).toBe(
            document.querySelector('.mobile-nav-wrapper li:last-of-type a')
        );
        dispatchEvent(keydownForward);
        expect(document.activeElement).toBe(
            document.querySelector('.mobile-nav-close-btn')
        );
        dispatchEvent(keydownForward);
        expect(document.activeElement).toBe(
            document.querySelector('.mobile-nav-wrapper a')
        );
    });

    describe('closing mobile menu', () => {
        const openButtonClass = 'global-nav-mobile-menu-btn';
        it('should return focus to open button on close button click', function () {
            document.querySelector('.mobile-nav-close-btn').click();
            // need to move past timeout in handleCloseMenu before testing focused element
            jasmine.clock().tick(500);
            expect(document.activeElement).toHaveClass(openButtonClass);
        });

        it('should return focus to open button on ESC keypress', function () {
            dispatchEvent(
                new KeyboardEvent('keydown', {
                    keyCode: ESC
                })
            );
            // need to move past timeout in handleCloseMenu before testing focused element
            jasmine.clock().tick(500);
            expect(document.activeElement).toHaveClass(openButtonClass);
        });

        it('should return focus to open button on outside menu click', function () {
            document.body.insertAdjacentHTML(
                'afterbegin',
                `<div id="test">Just somewhere to click outside the mobile menu</div>`
            );
            document.getElementById('test').click();
            // need to move past timeout in handleCloseMenu before testing focused element
            jasmine.clock().tick(500);
            expect(document.activeElement).toHaveClass(openButtonClass);
            document.getElementById('test').remove();
        });
    });
});
