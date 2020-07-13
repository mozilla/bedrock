/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    /* update dataLayer with experiment info */
    var href = window.location.href;

    var initTrafficCop = function () {
        if (href.indexOf('v=') !== -1) {
            var fbContainerLink = document.getElementById('fb-container-link');
            var monitorLink =  document.getElementById('monitor-link');
            var utmSource = '';
            if (href.indexOf('v=text') !== -1) {
                utmSource = 'mozilla.org-firefox-welcome-8-text';
                // default, no special class needed
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-text',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            } else if (href.indexOf('v=image') !== -1) {
                utmSource = 'mozilla.org-firefox-welcome-8-image';
                document.body.classList.add('variation-2-image');
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-image',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            } else if (href.indexOf('v=animation') !== -1) {
                utmSource = 'mozilla.org-firefox-welcome-8-animation';
                document.body.classList.add('variation-3-animation');
                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-animation',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            } else if (href.indexOf('v=header-text') !== -1) {
                utmSource = 'mozilla.org-firefox-welcome-8-header-text';
                var autopilotString = 'Your privacy is on <strong>autopilot</strong>';
                if (navigator.language.startsWith('fr-')) {
                    autopilotString = 'Votre vie privée est activée <strong>automatiquement</strong> par défaut.';
                } else if (navigator.language.startsWith('de-')) {
                    autopilotString = 'The same string in  <strong>DE</strong>';
                }
                document.getElementsByClassName('mzp-c-hero-title')[0].innerHTML = autopilotString;

                window.dataLayer.push({
                    'data-ex-variant': 'experiment-hvt-visual-header-text',
                    'data-ex-name': 'experiment-hvt-visual'
                });
            }

            monitorLink.href = 'https://monitor.firefox.com/?utm_source=' + utmSource + '&utm_medium=referral&utm_campaign=hvt-welcome-8';
            fbContainerLink.href = 'https://addons.mozilla.org/firefox/addon/facebook-container/?utm_source=' + utmSource + '&utm_medium=referral&utm_campaign=hvt-welcome-8';
        } else if (Mozilla.TrafficCop) {
            var cop = new Mozilla.TrafficCop({
                id: 'experiment_hvt_visual',
                cookieExpires: 0,
                variations: {
                    'v=text': 1,
                    'v=image': 20,
                    'v=animation': 20,
                    'v=header-text': 20,
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
