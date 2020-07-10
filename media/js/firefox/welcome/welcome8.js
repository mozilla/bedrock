/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    /* update dataLayer with experiment info */
    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('server-variation=') !== -1) {
            if (href.indexOf('server-variation=1') !== -1) {
              // default, no special class needed
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-v1',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            } else if (href.indexOf('server-variation=2') !== -1) {
              document.body.classList.add("variation-2-image");
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-v2',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            } else if (href.indexOf('server-variation=3') !== -1) {
              document.body.classList.add("variation-3-animation");
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-v3',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            } else if (href.indexOf('server-variation=4') !== -1) {
              document.body.classList.add("variation-4-text");
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-v4',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            }

          } else {
            var cop = new Mozilla.TrafficCop({
                id: 'experiment_hvt_visual',
                cookieExpires: 0,
                variations: {
                    'server-variation=1': 1,
                    'server-variation=2': 20,
                    'server-variation=3': 20,
                    'server-variation=4': 20,
                }
            });

            cop.init();
        }
    };
    initTrafficCop();

    function handleOpenProtectionReport(e) {
        e.preventDefault();
        Mozilla.UITour.showProtectionReport();

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'View your protection report'
        });
    }

    Mozilla.UITour.ping(function() {
        document.querySelectorAll('.protection-report').forEach(
            function(button) {
                button.addEventListener('click', handleOpenProtectionReport, false);
            }
        );
    });

})(window.Mozilla);
