;(function($) {
    'use strict';

    var $fxaFrame = $('#fxa');
    var fxaIframeSrc = $('#intro').data('fxa-iframe-src');
    var fxaFrameTarget = ($fxaFrame.length) ? $('#fxa')[0].contentWindow : null;
    var resizeTimer;
    var fxaHandshake = false;

    // remove trailing slash from iframe src (if present)
    fxaIframeSrc = (fxaIframeSrc[fxaIframeSrc.length - 1] === '/') ? fxaIframeSrc.substr(0, fxaIframeSrc.length - 1) : fxaIframeSrc;

    // set up communication with FxA iframe
    window.addEventListener('message', function (e) {
        var data;
        // make sure origin is as expected
        if (e.origin === fxaIframeSrc) {
            data = JSON.parse(e.data);

            switch (data.command) {
            // tell iframe we are expecting it
            case 'ping':
                fxaFrameTarget.postMessage(e.data, fxaIframeSrc);
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

                window.location.href = fxaIframeSrc + '/settings';

                break;
            }
        }
    }, true);

    // load FxA iframe only after postMessage communication is configured
    $fxaFrame.attr('src', $fxaFrame.data('src'));

    // set a timeout to show FxA (error page, most likely) should the ping event
    // above fail for some reason
    setTimeout(function() {
        if (!fxaHandshake) {
            $fxaFrame.css('height', '400px').addClass('visible');
        }
    }, 2500);
})(window.jQuery);
