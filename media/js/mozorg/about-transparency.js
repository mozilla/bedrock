/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla) {
    'use strict';

    var reportSections = $('#report-sections');
    var $faq = $('#faq .accordion-auto-init');
    var _retries = 0;

    function initReportSections(matches) {
        if (matches) {
            Mozilla.Accordion.destroyAccordionById('report-sections');
        } else {
            new Mozilla.Accordion(reportSections);
        }
    }

    if (reportSections.length && typeof matchMedia !== 'undefined') {
        var queryWide = matchMedia('(min-width: 760px)');
        initReportSections(queryWide.matches);

        queryWide.addListener(function(mq) {
            initReportSections(mq.matches);
        });
    }

    function scrollToAnchor() {
        var hash = window.location.hash.replace('#', '');

        if (hash) {
            var element = document.getElementById(hash);

            if (element && typeof element.scrollIntoView === 'function') {
                element.scrollIntoView(true);
            }
        }
    }

    function checkForAccordionInit() {
        var delay = 300;

        if ($faq.hasClass('accordion-initialized')) {
            setTimeout(scrollToAnchor, delay);
        } else if (_retries < 3) {
            _retries += 1;
            setTimeout(checkForAccordionInit, delay);
        }
    }

    // Bug 1299943 scroll hash/element into view after faq accordion has initialized.
    if ($faq.length) {
        checkForAccordionInit();
    }

})(window.jQuery, window.Mozilla);
