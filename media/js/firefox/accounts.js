/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla, $) {
    'use strict';

    var params = new window._SearchParams();
    var testVariation = params.get('v') || false;
    var fxaEmail;

    var $fxaFrame = $('#fxa');
    var fxaIframeHost = $('main').data('fxa-iframe-host');
    var fxaIframeSrc = $fxaFrame.data('src');
    var _resizeTimer;
    var _fxaHandshake = false;
    var client = Mozilla.Client;
    var $main = $('main');

    // remove trailing slash from iframe src (if present)
    fxaIframeHost = (fxaIframeHost[fxaIframeHost.length - 1] === '/') ? fxaIframeHost.substr(0, fxaIframeHost.length - 1) : fxaIframeHost;

    // check user's Fx version to determine FxA iframe experience
    if (Mozilla.Client.FirefoxMajorVersion >= 46) {
        fxaIframeSrc = fxaIframeSrc.replace('context=iframe', 'context=fx_firstrun_v2');
    }

    // check for fxaEmail in sessionStorage or URL params
    try {
        fxaEmail = sessionStorage.getItem('fxa-email');
        sessionStorage.removeItem('fxa-email');
    } catch(ex) {
        // empty
    }

    // if email address provided, send to FxA frame
    if (fxaEmail && /(.+)@(.+)\.(.+){2,}/.test(fxaEmail)) {
        fxaIframeSrc += '&email=' + encodeURIComponent(fxaEmail);
    }

    function onFormPing(data) {
        var fxaFrameTarget = $fxaFrame[0].contentWindow;
        fxaFrameTarget.postMessage(data, fxaIframeHost);
        _fxaHandshake = true;
    }

    function onFormResize(height) {
        clearTimeout(_resizeTimer);
        // sometimes resizes come in bunches - only want to react to the last of a set
        _resizeTimer = setTimeout(function() {
            showFxAccountsForm(height);
        }, 300);
    }

    function onFormLogin() {
        sendGAEvent('sign-in');
        redirectToAccountSettings();
    }

    function redirectToAccountSettings() {
        window.location.href = fxaIframeHost + '/settings';
    }

    function showFxAccountsForm(height) {
        var formHeight = height !== undefined ? height : 450;
        $fxaFrame.css('height', formHeight + 'px').addClass('loaded');
    }

    function sendGAEvent(type, extra) {
        // we'll always have a type
        var data = {
            'event': 'accounts',
            'interaction': type
        };

        // merge additional properties if available
        if (extra) {
            $.extend(data, extra);
        }

        window.dataLayer.push(data);
    }

    // set up communication with FxA iframe
    function onMessageReceived(e) {
        // make sure origin is as expected
        if (e.origin !== fxaIframeHost) {
            return;
        }

        var data = JSON.parse(e.data);

        switch (data.command) {
        // tell iframe we are expecting it
        case 'ping':
            onFormPing(e.data);
            break;
        // just GA tracking when iframe loads
        case 'loaded':
            sendGAEvent('impression');
            break;
        // resize container when iframe resizes for nicer UI
        case 'resize':
            onFormResize(data.data.height);
            break;
        // track when user signs up successfully (but hasn't yet verified email)
        case 'signup_must_verify':
            // if emailOptIn property is present, send value to GA
            if (data.data.hasOwnProperty('emailOptIn')) {
                sendGAEvent('email opt-in', { 'label': data.data.emailOptIn });
            }

            if (testVariation) {
                sendGAEvent('success', { 'test-variation': testVariation });
            } else {
                sendGAEvent('success');
            }
            break;
        // track when user returns to page after verifying email (may never happen)
        case 'verification_complete':
            sendGAEvent('verified');
            break;
        // track & redirect user with FxA account logging in
        case 'login':
            onFormLogin();
            break;
        }
    }

    function loadFxAccountsForm() {
        // bind postMessage event listener
        window.addEventListener('message', onMessageReceived, true);

        // load FxA iframe only after postMessage communication is configured
        $fxaFrame.attr('src', fxaIframeSrc);

        // set a timeout to show FxA (error page, most likely) should the ping event
        // above fail for some reason
        setTimeout(function() {
            if (!_fxaHandshake) {
                showFxAccountsForm();
            }
        }, 2500);
    }

    function showFxAForm() {
        loadFxAccountsForm();

        // UITour is used only to show conditional messaging.
        Mozilla.UITour.getConfiguration('sync', function (config) {
            if (config.setup) {
                // Show signed-in messaging if user is already using Sync
                $('.signed-in').show();
            } else {
                // Show sign-up steps if user is not already using Sync
                $('.sign-up-instructions').show();
            }
        });
    }

    // Show FxA form for up to date Firefox desktop users.
    function showUpToDateFirefox() {
        $main.addClass('state-firefox-up-to-date');
        showFxAForm();
    }

    // Firefox iOS users get SUMO link
    function showFirefoxiOS() {
        $main.addClass('state-firefox-ios');
        sendGAEvent('firefox-ios');
    }

    // Firefox Android users get SUMO link
    function showFirefoxAndroid() {
        $main.addClass('state-firefox-android');
        sendGAEvent('firefox-android');
    }

    // Non-Firefox mobile users see app store badges
    function showMobileNonFirefox() {
        $main.addClass('state-mobile');
        sendGAEvent('mobile-non-firefox');
    }

    // Other Non-Firefox browsers get regular download button
    function showNonFirefox() {
        $main.addClass('state-non-firefox');
        sendGAEvent('non-firefox');
    }

    // Old Firefox browsers get regular download button
    function showOldFirefox() {
        $main.addClass('state-old-firefox');
        sendGAEvent('old-firefox');
    }

    function init() {
        if (client.isFirefoxDesktop) {
            // FxA iFrame supported on Firefox 39 and greater
            if (client.FirefoxMajorVersion >= 39) {
                showUpToDateFirefox();
            } else {
                showOldFirefox();
            }
        } else {
            if (client.isFirefoxiOS) {
                showFirefoxiOS();
            } else if (client.isFirefoxAndroid) {
                showFirefoxAndroid();
            } else if (client.isMobile) {
                showMobileNonFirefox();
            } else {
                showNonFirefox();
            }
        }
    }

    init();

    setTimeout(Mozilla.syncAnimation, 1000);

})(window.Mozilla, window.jQuery);
