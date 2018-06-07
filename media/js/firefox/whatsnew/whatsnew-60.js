/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/*
This iteration of /whatsnew has multiple states:

1. User is not logged in to FxA (or UITour JS fails/times out):
    Display the FxA iframe

2. User is logged in to FxA, but does not have any mobile devices set up:
    Display App/Play store badges for Firefox Mobile

    i. Send to Device widget is available in the user's locale:
        Display the Send to Device widget
    ii. Send to Device widget is *not* available in the user's locale:
        Display a QR code for Firefox Mobile

3. User is logged in to FxA, and *does* have a mobile device set up:
    Display a QR code for Firefox Focus
    Display App/Play store badges for Focus
*/

(function(Mozilla) {
    'use strict';

    var client = Mozilla.Client;
    var sendTo = document.getElementById('send-to-device');
    var mainContent = document.querySelector('.main-content');

    function showFxa() {
        mainContent.classList.add('show-fxa');

        // initialize the FxA iframe
        Mozilla.Client.getFirefoxDetails(function(data) {
            Mozilla.FxaIframe.init({
                distribution: data.distribution,
                gaEventName: 'whatsnew-fxa'
            });
        });
    }

    function showFirefoxMobile() {
        mainContent.classList.add('show-fxa-mobile');

        // initialize Send to Device widget if present/available
        if (sendTo) {
            var form = new Mozilla.SendToDevice();
            form.init();
        }
    }

    function showFocus() {
        var logoFx = document.getElementById('logo-fx');
        var logoFocus = document.getElementById('logo-focus');

        // swap out Firefox logo for Focus logo
        logoFx.classList.replace('showing', 'hiding');

        setTimeout(function() {
            logoFocus.classList.replace('hiding', 'showing');
        }, 150);

        mainContent.classList.add('show-focus');
    }

    // bug 1419573 - only show "Your Firefox is up to date" if it's the latest version.
    if (client.isFirefoxDesktop) {
        client.getFirefoxDetails(function(data) {
            if (data.isUpToDate) {
                document.querySelector('.main-header').classList.add('show-up-to-date-message');
            }
        });
    }

    client.getFxaDetails(function(details) {
        // if user is not signed in to FxA, show the FxA form
        if (!details.setup) {
            showFxa();
        // if the user is signed in to FxA but doesn't have any mobile devices set up, show Fx mobile content
        } else if (details.mobileDevices === 'unknown' || details.mobileDevices === 0) {
            showFirefoxMobile();
        // if user is signed in to FxA and has mobile devices set up, show Focus content
        } else {
            showFocus();
        }
    });
})(window.Mozilla);
