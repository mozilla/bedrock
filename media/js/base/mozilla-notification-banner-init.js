/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// needs to execute on DOM ready to sync with core-data-layer.init.js in GA.
$(function() {
    'use strict';

    var client = window.Mozilla.Client;

    var options = [
        {
            'id': 'fx-out-of-date-banner-copy1-direct-1',
            'name': 'fx-out-of-date',
            'experimentName': 'fx-out-of-date-banner-copy1',
            'experimentVariant': 'direct-1',
            'heading': 'Your browser security is at risk.',
            'message': 'Update Firefox now to protect yourself from the latest malware.',
            'confirm': 'Update now',
            'confirmAction': 'Update Firefox',
            'confirmLabel': 'Firefox for Desktop',
            'url': '/firefox/new/?scene=2',
            'close': 'Close',
            'closeLabel': 'Close'
        },
        {
            'id': 'fx-out-of-date-banner-copy1-direct-2',
            'name': 'fx-out-of-date',
            'experimentName': 'fx-out-of-date-banner-copy1',
            'experimentVariant': 'direct-2',
            'heading': 'Your Firefox is out-of-date.',
            'message': 'Get the most recent version to keep browsing securely.',
            'confirm': 'Update Firefox',
            'confirmAction': 'Update Firefox',
            'confirmLabel': 'Firefox for Desktop',
            'url': '/firefox/new/?scene=2',
            'close': 'Close',
            'closeLabel': 'Close'
        },
        {
            'id': 'fx-out-of-date-banner-copy1-foxy-1',
            'name': 'fx-out-of-date',
            'experimentName': 'fx-out-of-date-banner-copy1',
            'experimentVariant': 'foxy-1',
            'heading': 'Psst… it’s time for a tune up',
            'message': 'Stay safe and fast with a quick update.',
            'confirm': 'Update Firefox',
            'confirmAction': 'Update Firefox',
            'confirmLabel': 'Firefox for Desktop',
            'url': '/firefox/new/?scene=2',
            'close': 'Close',
            'closeLabel': 'Close'
        },
        {
            'id': 'fx-out-of-date-banner-copy1-foxy-2',
            'name': 'fx-out-of-date',
            'experimentName': 'fx-out-of-date-banner-copy1',
            'experimentVariant': 'foxy-2',
            'heading': 'Time to browse better!',
            'message': 'Get the latest version of Firefox for extra speed and safety.',
            'confirm': 'Update now',
            'confirmAction': 'Update Firefox',
            'confirmLabel': 'Firefox for Desktop',
            'url': '/firefox/new/?scene=2',
            'close': 'Close',
            'closeLabel': 'Close'
        }
    ];

    // Set a unique cookie ID for fx-out-of-date notification.
    Mozilla.NotificationBanner.COOKIE_CODE_ID = 'moz-notification-fx-out-of-date';

    // Notification should only be shown to users on Firefox for desktop.
    if (client.isFirefoxDesktop) {
        client.getFirefoxDetails(function(details) {
            // User must be out of date and on release channel.
            if (!details.isUpToDate && details.channel === 'release') {

                // Check that cookies are enabled before seeing if one already exists.
                if (typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled()) {
                    var cookie = Mozilla.NotificationBanner.getCookie();

                    if (cookie) {
                        for (var i in options) {
                            if (options[i].id === cookie) {
                                Mozilla.NotificationBanner.init(options[i]);
                                break;
                            }
                        }
                    } else {
                        var choice = Math.floor(Math.random() * 4); // choose one of 4 variations.
                        Mozilla.NotificationBanner.init(options[choice]);
                    }
                }
            }
        });
    }
});
