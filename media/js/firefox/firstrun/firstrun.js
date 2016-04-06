/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $fxaFrame = $('#fxa');
    var fxaIframeHost = $('#intro').data('fxa-iframe-host');
    var fxaFrameTarget = ($fxaFrame.length) ? $('#fxa')[0].contentWindow : null;
    var fxaIframeSrc = $fxaFrame.data('src');
    var resizeTimer;
    var fxaHandshake = false;

    // remove trailing slash from iframe src (if present)
    fxaIframeHost = (fxaIframeHost[fxaIframeHost.length - 1] === '/') ? fxaIframeHost.substr(0, fxaIframeHost.length - 1) : fxaIframeHost;

    // check user's Fx version to determine FxA iframe experience
    if (Mozilla.Client.FirefoxMajorVersion >= 46) {
        fxaIframeSrc = fxaIframeSrc.replace('context=iframe', 'context=fx_firstrun_v2');
    }

    // set up communication with FxA iframe
    window.addEventListener('message', function (e) {
        var data;
        // make sure origin is as expected
        if (e.origin === fxaIframeHost) {
            data = JSON.parse(e.data);

            switch (data.command) {
            // tell iframe we are expecting it
            case 'ping':
                fxaFrameTarget.postMessage(e.data, fxaIframeHost);
                fxaHandshake = true;
                break;
            // just GA tracking when iframe loads
            case 'loaded':
                window.dataLayer.push({
                    'event': 'firstrun-fxa',
                    'interaction': 'fxa-loaded'
                });

                break;
            // resize container when iframe resizes for nicer UI
            case 'resize':
                clearTimeout(resizeTimer);
                // sometimes resizes come in bunches - only want to react to the last of a set
                resizeTimer = setTimeout(function() {
                    $fxaFrame.css('height', data.data.height + 'px').addClass('visible');
                }, 300);

                break;
            // track when user signs up successfully (but hasn't yet verified email)
            case 'signup_must_verify':
                // if emailOptIn property is present, send value to GA
                if (data.data.hasOwnProperty('emailOptIn')) {
                    window.dataLayer.push({
                        'event': 'firstrun-fxa',
                        'interaction': 'email opt-in',
                        'label': data.data.emailOptIn
                    });
                }

                window.dataLayer.push({
                    'event': 'firstrun-fxa',
                    'interaction': 'fxa-signup'
                });

                break;
            // track when user returns to page after verifying email (may never happen)
            case 'verification_complete':
                window.dataLayer.push({
                    'event': 'firstrun-fxa',
                    'interaction': 'fxa-verified'
                });

                break;
            // track & redirect user with FxA account logging in
            case 'login':
                window.dataLayer.push({
                    'event': 'firstrun-fxa',
                    'interaction': 'fxa-login'
                });

                window.location.href = fxaIframeHost + '/settings';

                break;
            }
        }
    }, true);

    // load FxA iframe only after postMessage communication is configured
    $fxaFrame.attr('src', fxaIframeSrc);

    // set a timeout to show FxA (error page, most likely) should the ping event
    // above fail for some reason
    setTimeout(function() {
        if (!fxaHandshake) {
            $fxaFrame.css('height', '400px').addClass('visible');
        }
    }, 2500);
})(window.jQuery);
