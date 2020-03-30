/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    /* update dataLayer with experiment info */
    var href = window.location.href;
    if (href.indexOf('v=') !== -1) {
        if (href.indexOf('v=a') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'installer-help-control',
                'data-ex-name': 'CRO-Installer-Help-Experiment'
            });
        } else if (href.indexOf('v=b') !== -1) {
            window.dataLayer.push({
                'data-ex-variant': 'installer-help-v1',
                'data-ex-name': 'CRO-Installer-Help-Experiment'
            });
        }
    } else {
        var cop = new Mozilla.TrafficCop({
            id: 'experiment_installer_help',
            variations: {
                'v=a': 27,
                'v=b': 27
            }
        });

        cop.init();
    }

})(window.Mozilla);
