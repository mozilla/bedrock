/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// needs to execute on DOM ready to sync with core-data-layer.init.js in GA.
$(function() {
    'use strict';

    var client = window.Mozilla.Client;

    var _clickCallback = function() {
        Mozilla.Modal.createModal(this, $('.notification-modal-content'));
    };

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
            'confirmClick': _clickCallback,
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
            'confirmClick': _clickCallback,
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
            'confirmClick': _clickCallback,
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
            'confirmClick': _clickCallback,
            'url': '/firefox/new/?scene=2',
            'close': 'Close',
            'closeLabel': 'Close'
        }
    ];

    /**
     * Determine if Firefox cliient is out of date.
     * @return {Boolean} - Returns true if client is at least 2 major versions out of date.
     */
    var _isClientOutOfDate = function() {
        var clientVersion = client.FirefoxMajorVersion;
        var latestVersion = parseInt($('html').attr('data-latest-firefox'), 10);

        if (!latestVersion || !clientVersion) {
            return false;
        }

        return clientVersion < latestVersion - 1;
    };

    // Set a unique cookie ID for fx-out-of-date notification.
    Mozilla.NotificationBanner.COOKIE_CODE_ID = 'moz-notification-fx-out-of-date';

    // Rate limit notification to 5%;
    Mozilla.NotificationBanner.setSampleRate(0.05);

    // Notification should only be shown to Firefox desktop users more than 2 major versions out of date.
    if (client.isFirefoxDesktop && _isClientOutOfDate()) {
        client.getFirefoxDetails(function(details) {

            // User must be on release channel and have cookies enabled.
            if (details.channel === 'release' && typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled()) {

                var choice = Mozilla.NotificationBanner.getOptions(options);

                if (choice) {
                    Mozilla.NotificationBanner.init(choice);
                }
            }
        });
    }
});
