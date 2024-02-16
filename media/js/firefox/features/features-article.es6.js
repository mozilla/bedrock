/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const client = Mozilla.Client;
const footerCta = document.querySelector('.c-feature-footer');

(function () {
    if (footerCta && client.isFirefoxDesktop) {
        footerCta.parentNode.removeChild(footerCta);
    }
})(window.Mozilla);
