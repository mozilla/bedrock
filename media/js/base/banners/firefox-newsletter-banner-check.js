/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

var cookiesEnabled =
    typeof window.Mozilla.Cookies !== 'undefined' &&
    window.Mozilla.Cookies.enabled();

if (
    cookiesEnabled &&
    window.Mozilla.Cookies.hasItem('firefox-newsletter-banner')
) {
    document.documentElement.setAttribute(
        'data-firefox-newsletter-banner-closed',
        'true'
    );
}
