/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function (Mozilla) {
    'use strict';

    function handleOpenProtectionReport(e) {
        e.preventDefault();
        // UA
        window.dataLayer.push({
            event: 'in-page-interaction',
            eAction: 'link click',
            eLabel: 'View your protection report'
        });
        // GA4
        window.dataLayer.push({
            event: 'widget_action',
            type: 'protection report',
            action: 'open',
            label: 'View your protection report'
        });
        Mozilla.UITour.showProtectionReport();
    }

    function handleOpenProtectionReportLink(e) {
        e.preventDefault();
        // UA
        window.dataLayer.push({
            event: 'in-page-interaction',
            eAction: 'link click',
            eLabel: 'See what`s blocked'
        });
        // GA4
        window.dataLayer.push({
            event: 'widget_action',
            type: 'protection report',
            action: 'open',
            label: "See what's blocked"
        });

        Mozilla.UITour.showProtectionReport();
    }

    Mozilla.UITour.ping(function () {
        document
            .querySelectorAll('.protection-report.primary-cta')
            .forEach(function (button) {
                button.addEventListener(
                    'click',
                    handleOpenProtectionReport,
                    false
                );
            });
        document
            .querySelectorAll('.protection-report:not(.primary-cta)')
            .forEach(function (button) {
                button.addEventListener(
                    'click',
                    handleOpenProtectionReportLink,
                    false
                );
            });
    });
})(window.Mozilla);
