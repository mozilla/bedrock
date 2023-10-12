/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';
    const copyArea = document.querySelector('.c-coupon-code');
    const copyButton = document.getElementById('code-copy');

    copyArea.addEventListener('click', copyCouponCode);
    copyButton.addEventListener('click', copyCouponCode);

    async function copyCouponCode() {
        let couponCode = copyButton.dataset.code;
        let successMsg = copyButton.dataset.success;

        try {
            await navigator.clipboard.writeText(couponCode);
            copyButton.textContent = successMsg;
        } catch (e) {
            //do nothing
        }
    }
})();
