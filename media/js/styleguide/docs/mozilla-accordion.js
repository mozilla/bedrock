/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var accordion2;

    var accordion2Options = {
        /* eslint-disable no-console */
        onExpand: function(section) {
            console.log('Accordion "' + section.title + '" expanding...');
        },
        onCollapse: function(section) {
            console.log('Accordion "' + section.title + '" collapsing...');
        }
        /* eslint-enable no-console */
    };

    $('#accordion2-enable').on('click', function() {
        if (!accordion2) {
            accordion2 = new Mozilla.Accordion($('#example2'), accordion2Options);
        }
    });

    $('#accordion2-disable').on('click', function() {
        if (accordion2) {
            Mozilla.Accordion.destroyAccordionById(accordion2.id);
            accordion2 = null;
        }
    });
})(window.jQuery);
