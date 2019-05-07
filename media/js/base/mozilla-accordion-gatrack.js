/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

// If accordion is present, set up global GA functions
if (typeof Mozilla.Accordion === 'function') {
    Mozilla.Accordion.globalOnExpand = function(section) {
        'use strict';
        // Google Analytics event tracking

        window.dataLayer.push({
            'event': 'accordion-interaction',
            'interaction': 'Expand',
            'question': section.$header.text(),
            'questionNumber': section.id.split('-')[1]
        });
    };

    Mozilla.Accordion.globalOnCollapse = function(section) {
        'use strict';
        // Google Analytics event tracking

        window.dataLayer.push({
            'event': 'accordion-interaction',
            'interaction': 'Collapse',
            'question': section.$header.text(),
            'questionNumber': section.id.split('-')[1]
        });
    };
}
