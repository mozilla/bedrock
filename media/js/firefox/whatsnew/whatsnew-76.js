/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    function handleOpenProtectionReport(e) {
        e.preventDefault();

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'View your protection report'
        });

        Mozilla.UITour.showProtectionReport();
    }

    Mozilla.UITour.ping(function() {
        document.querySelector('.protection-report').addEventListener('click', handleOpenProtectionReport, false);
    });

    var fcShown = document.querySelector('.facebook-container') !== null;

    if (fcShown) {
        document.querySelector('.columns').classList.add('l-columns-three');
    } else {
        document.querySelector('.columns').classList.add('l-columns-two');
    }

})();
