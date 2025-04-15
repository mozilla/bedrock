/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Trap keyboard focus on mobile navigation.
 * Issue #16090
 * @param {Boolean} isFocusTrapped - determine if keyboard focus trap is active.
 * @param {String} element - element to trap keyboard focus within.
 * @param {Function} focusableClassList - a function that returns a string of class names of focusable elements.
 * @returns {Function} - an arrow function that removes the same event listener that is added to the element
 */
function trapKeyboardFocus(isFocusTrapped, element, focusableClassList) {
    const listener = function (e) {
        if (!isFocusTrapped()) {
            return;
        }

        const isTabPressed = e.key === 'Tab' || e.keyCode === 9;

        if (!isTabPressed) {
            return;
        }

        const focusableEles = element.querySelectorAll(focusableClassList());
        const firstFocusableEle = focusableEles[0];
        const lastFocusableEle = focusableEles[focusableEles.length - 1];

        if (e.shiftKey) {
            // shift + tab
            if (document.activeElement === firstFocusableEle) {
                lastFocusableEle.focus();
                e.preventDefault();
            }
        } else {
            // tab
            if (document.activeElement === lastFocusableEle) {
                firstFocusableEle.focus();
                e.preventDefault();
            }
        }
    };

    element.addEventListener('keydown', listener);

    return () => element.removeEventListener('keydown', listener);
}

export { trapKeyboardFocus };
