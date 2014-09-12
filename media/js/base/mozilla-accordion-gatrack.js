/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// If accordion is present, set up global GA functions
if (typeof Mozilla.Accordion === 'function') {
    Mozilla.Accordion.GLOBAL_ONEXPAND = function(section) {
        // Google Analytics event tracking
        gaTrack([
            '_trackEvent',
            location.pathname + ' Accordion Interactions',
            'Expand',
            section.$header.text()
        ]);
    };

    Mozilla.Accordion.GLOBAL_ONCOLLAPSE = function(section) {
        // Google Analytics event tracking
        gaTrack([
            '_trackEvent',
            location.pathname + ' Accordion Interactions',
            'Collapse',
            section.$header.text()
        ]);
    };
}
