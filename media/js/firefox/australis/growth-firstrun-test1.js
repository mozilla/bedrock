;(function($, Mozilla) {
    'use strict';

    // declare vars (might as well be here because hoisting)
    var $body;
    var $ghosteryIframe;
    var $outerWrapper = $('#outer-wrapper');

    // determines if tour opens or not
    var showDoorhanger;

    var gaVariation;

    // reference FxA elements
    var $fxaOverlay;
    var $fxaIframe;
    var $fxaExtra;
    var $fxaValueProp;
    var $fxaDelayedCTAs;

    // store client ID for FxA integration
    var fxaClient;
    var fxaRelier;
    var csrf;

    // function expression vars
    var initFxA;
    var enableIframe;
    var showFxA;
    var trackSyncClick;
    var randomStringMaker;

    var toggleDefaultContent = function(show) {
        // show default #outer-wrapper
        if (show) {
            $outerWrapper.show();

            Mozilla.syncAnimation();
        } else {
            $outerWrapper.hide();
        }
    };

    // fallback in case UITour doesn't load
    $outerWrapper.show();

    // Only run experiment content if user is on Firefox 35 for desktop and has not just submitted email form
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 35 && window.location.hash !== '#footer-email-form') {
        // initialize vars
        $body = $('body');
        $ghosteryIframe = $('iframe.addon');

        // grab FxA settings from data-* attributes
        $fxaExtra = $('#fxa-extra');

        fxaRelier = {
            clientId: $fxaExtra.data('fxa-client-id'),
            contentHost: $fxaExtra.data('fxa-content-host'),
            contentOauth: $fxaExtra.data('fxa-content-oauth'),
            redirectUri: $fxaExtra.data('fxa-redirect-uri')
        };

        // determine whether or not to show doorhanger (50% of users)
        showDoorhanger = Math.random() >= 0.5;

        // GA
        gaVariation = (showDoorhanger) ? 'a' : 'b';

        enableIframe = function() {
            $ghosteryIframe.attr('src', $ghosteryIframe.attr('data-src'));
        };

        showFxA = function() {
            $fxaOverlay.addClass('visible');

            // display heading with timeout (so transition happens)
            setTimeout(function() {
                $fxaValueProp.addClass('visible');
            }, 500);

            // display sub-CTAs 40s later
            // temporary until FxA client supports broadcast of 'Signup' click
            setTimeout(function() {
                $fxaDelayedCTAs.addClass('visible');

            }, 40000);
        };

        initFxA = function() {
            csrf = randomStringMaker();

            // set up FxA client
            fxaClient = new window.FxaRelierClient(fxaRelier.clientId, {
                contentHost: fxaRelier.contentHost,
                oauthHost: fxaRelier.contentOauth
            });

            // conjure FxA lightbox
            fxaClient.auth.signUp({
                redirectUri: fxaRelier.redirectUri,
                scope: 'profile',
                state: csrf,
                ui: 'lightbox',
                background: '#fff',
                zIndex: 99,
                keepOverlay: true // customized build of fxa-relier-client.js to support this option
            }).then(function(result) {
                // make sure CSRF/state matches
                if (result.state === csrf) {
                    // change header
                    $('#fxa-value-prop-intro').fadeOut('fast', function() {
                        $('#fxa-value-prop-verified').fadeIn('fast');
                    });

                    // wipe out iframe and reposition delayed CTAs
                    $fxaIframe.slideUp('normal', function() {
                        $fxaIframe.remove();
                    });

                    $fxaDelayedCTAs.addClass('visible noiframe');
                }
            }, function(err) {
                // on error (or click of X in iframe), get rid of overlay and fall back to default content
                $fxaOverlay.remove();

                // link directly to Firefox Accounts when clicking the Sync CTA button
                Mozilla.UITour.getConfiguration('sync', function() {
                    $('.sync-cta').on('click', '.button', trackSyncClick);
                });

                toggleDefaultContent(true);
            });
        };

        // track Sync CTA click and link to about:accounts where posiible
        trackSyncClick = function(e) {
            e.preventDefault();

            var goToAccounts = function () {
                // available on Firefox 31 and greater
                Mozilla.UITour.showFirefoxAccounts();
            };

        };

        randomStringMaker = function() {
            var text = '';
            var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

            for(var i = 0; i < 15; i++) {
                text += possible.charAt(Math.floor(Math.random() * possible.length));
            }

            return text;
        };

        // listen for postMessage from iframes
        window.addEventListener('message', function(event) {
            // listen for fxa communiques
            if (typeof event.data === 'string') {
                // 'ping' sent when lightbox created
                if (event.data.indexOf('ping') > -1) {
                    // initialize reference to fxa overlay & iframe
                    $fxaOverlay = $('#fxa-background');
                    $fxaIframe = $('#fxa');

                    // move content into FxA overlay
                    $fxaValueProp = $('#fxa-value-prop').detach();
                    $fxaDelayedCTAs = $('#fxa-delayed-ctas').detach();

                    $fxaOverlay.prepend($fxaValueProp).append($fxaDelayedCTAs);

                    showFxA();
                }
            } 
        });

        // if chosen to show doorhanger, get tour setup
        if (showDoorhanger) {
            // Query if the UITour API is working before we start the tour
            Mozilla.UITour.getConfiguration('sync', function() {
                // hide default content
                toggleDefaultContent(false);

                // wire up sync click in default content
                $('.sync-cta').on('click', '.button', trackSyncClick);

                // id is used for Telemetry
                var tour = new Mozilla.BrowserTour({
                    id: $('#tour-page').data('telemetry'),
                    startTour: function(buttonCopy) {
                        // prepare FxA stuff
                        initFxA();

                        // enable AMO iframe
                        enableIframe();

                        // give FxA a moment to initialize before getting rid of mask
                        setTimeout(function() {
                            tour.doCloseTour();
                        }, 600);

                    },
                    cancelTour: function(buttonCopy) {
                        tour.doCloseTour();

                        toggleDefaultContent(true);

                        if ($fxaOverlay) {
                            $fxaOverlay.fadeOut('fast');
                        }

                    }
                });

                tour.init();
            });
        // if not showing tour, just get to FxA UI
        } else {
            toggleDefaultContent(false);

            // prepare FxA stuff
            initFxA();

            // initialize Ghostery iframe
            enableIframe();
        }

        // wire up CTAs
        $('#highlight-sync').on('click', function(e) {
            e.preventDefault();

            // call twice two correctly position highlight
            // https://bugzilla.mozilla.org/show_bug.cgi?id=1049130
            Mozilla.UITour.showHighlight('accountStatus', 'wobble');
            Mozilla.UITour.showHighlight('accountStatus', 'wobble');

            // timeout so event isn't captured with *this* click
            setTimeout(function() {
                $(document).one('click', function() {
                    Mozilla.UITour.hideMenu('appMenu');
                });
            }, 50);

        });
    }
})(window.jQuery, window.Mozilla);
