/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var href = window.location.href;
    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            /* update dataLayer with experiment info */
            if (href.indexOf('v=a') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'new-redesign-control',
                    'data-ex-name': 'NABrand-new-redesign-Experiment'
                });
            } else if (href.indexOf('v=b') !== -1) {
                window.dataLayer.push({
                    'data-ex-variant': 'new-redesign-vb',
                    'data-ex-name': 'NABrand-new-redesign-Experiment'
                });
            }
        } else {
            var cop = new Mozilla.TrafficCop({
                id: 'experiment_new-redesign',
                variations: {
                    'v=a&variation=a&experiment=new-redesign': 3,
                    'v=b&variation=b&experiment=new-redesign': 3
                }
            });

            cop.init();
        }
    };

    initTrafficCop();

})(window.Mozilla);
