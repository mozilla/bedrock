/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    // Add class to indicate Windows 8 and later
    if (window.site.platform === 'windows' && window.site.platformVersion >= 6.2) {
        document.documentElement.classList.add('win8up');
    }

    var beginAnimation = function (syncConfig) {
        var redirectDest = 'about:newtab';
        var scene = document.getElementById('scene');
        var skipbutton = document.getElementById('skip-button');

        var hideOrShowSkipButton = function (data) {
            switch(data.data.url) {
            case '':
            case 'signin':
            case 'signup':
            case 'reset_password':
                skipbutton.disabled = false;
                skipbutton.classList.remove('skipbutton-hidden');
                break;
            default:
                skipbutton.classList.add('skipbutton-hidden');
                break;
            }
        };

        var disableSkipButton = function () {
            skipbutton.disabled = true;
        };

        var onVerificationComplete = function () {
            scene.dataset.signIn = 'true';
            // Specially navigate to about:newtab and focus address bar
            if (redirectDest === 'about:newtab') {
                Mozilla.UITour.showNewTab();
            } else {
                window.location.href = redirectDest;
            }
        };

        skipbutton.onclick = onVerificationComplete;

        if (syncConfig) {
            window.setTimeout(function() {
                onVerificationComplete();
            }, 1000);
        } else {
            scene.dataset.content = 'true';
        }

        Mozilla.Client.getFirefoxDetails(function(data) {
            Mozilla.FxaIframe.init({
                distribution: data.distribution,
                gaEventName: 'firstrun-fxa',
                onVerificationComplete: onVerificationComplete,
                onLogin: onVerificationComplete,
                onFormEngaged: disableSkipButton,
                onNavigated: hideOrShowSkipButton
            });

            if (data.distribution && data.distribution.toLowerCase() === 'mozillaonline') {
                redirectDest = 'https://start.firefoxchina.cn/';
            }
        });
    };

    document.onreadystatechange = function() {
        if (document.readyState === 'complete') {
            var syncConfig;
            Mozilla.UITour.getConfiguration('sync', function(config) {
                syncConfig = config.setup;
                beginAnimation(syncConfig);
            });
        }
    };

})(window.Mozilla);
