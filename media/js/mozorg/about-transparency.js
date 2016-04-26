/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla) {
    'use strict';

    var reportSections = $('#report-sections');

    if (reportSections.length) {
        if (typeof matchMedia !== 'undefined') {

            var queryWide = matchMedia('(min-width: 760px)');

            if (queryWide.matches) {
                Mozilla.Accordion.destroyAccordionById('report-sections');
            } else {
                new Mozilla.Accordion(reportSections);
            }

            queryWide.addListener(function(mq) {
                if (mq.matches) {
                    Mozilla.Accordion.destroyAccordionById('report-sections');
                } else {
                    new Mozilla.Accordion(reportSections);
                }
            });
        }
    }

})(window.jQuery, window.Mozilla);
