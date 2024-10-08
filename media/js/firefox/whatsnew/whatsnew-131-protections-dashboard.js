/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function handleOpenProtectionReport(e) {
    'use strict';

    e.preventDefault();

    window.dataLayer.push({
        event: 'widget_action',
        type: 'protection report',
        action: 'open',
        label: 'See my protections dashboard'
    });

    Mozilla.UITour.showProtectionReport();
}

// Intercept link clicks to open about:protections page using UITour.
Mozilla.UITour.ping(() => {
    'use strict';

    document
        .getElementById('protections-dashboard')
        .addEventListener('click', handleOpenProtectionReport, false);
});
