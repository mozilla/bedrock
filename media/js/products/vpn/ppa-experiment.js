/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

if (/\sFirefox/.test(navigator.userAgent)) {
    const links = document.getElementsByClassName('js-fxa-product-button');
    Array.from(links).forEach(link => {
        "use strict";

        link.addEventListener('click', () => {
            navigator.privateAttribution.measureConversion({
                task: "task_id",            // Unique task ID. Supplied by Mozilla.
                histogramSize: 5,           // Supplied by Mozilla
                lookbackDays: 7,           // Number of days to look back for attribution
                impression: "click",         // Attribution model to use
                ads: ["ad_id"],             // List Ad IDs. Supplied by Mozilla.
                sources: ["mozilla.org"]  // List of publisher domains
            });
        });
    });
}
