/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function () {
    'use strict';

    var animateSunrise = function () {
        var scene = document.getElementById('scene');
        var skipbutton = document.getElementById('skip-button');

        var onVerificationComplete = function () {
            scene.dataset.signIn = 'true';
            document.getElementById('sunrise').addEventListener('transitionend', function(event) {
                if (event.propertyName === 'transform') {
                    window.setTimeout(function () {
                        // Bug 1381051 sign in should redirect to about:home instead of about:newtab.
                        window.location.href = 'about:home';
                    }, 200);
                }
            }, false);
        };

        skipbutton.onclick = onVerificationComplete;

        scene.dataset.sunrise = 'true';

        document.getElementById('sky').addEventListener('transitionend', function(event) {
            if (event.propertyName === 'opacity') {
                scene.dataset.modal = 'true';
            }
        }, false);
    };

    document.onreadystatechange = function () {
        if (document.readyState === 'complete') {
            animateSunrise();
        }
    };
})();
