/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// needs to execute on DOM ready to sync with core-data-layer.init.js in GA.
$(function() {
    'use strict';

    var client = window.Mozilla.Client;
    var utils = window.Mozilla.Utils;

    var headingText;
    var messageText;
    var confirmText;
    var closeText;

    if (typeof utils === 'undefined' || typeof client === 'undefined') {
        return;
    }

    headingText = utils.trans('global-fx-out-of-date-banner-heading');
    messageText = utils.trans('global-fx-out-of-date-banner-message');
    confirmText = utils.trans('global-fx-out-of-date-banner-confirm');
    closeText = utils.trans('global-close');

    var config = {
        'id': 'fx-out-of-date-banner',
        'name': 'fx-out-of-date',
        'heading': headingText,
        'message': messageText,
        'confirm': confirmText,
        'url': '/firefox/download/thanks/',
        'close': closeText,
        'gaConfirmAction': 'Update Firefox', // GA - English only
        'gaConfirmLabel': 'Firefox for Desktop', // GA - English only
        'gaCloseLabel': 'Close' // GA - English only
    };

    // Set a unique cookie ID for fx-out-of-date notification.
    Mozilla.NotificationBanner.COOKIE_CODE_ID = 'moz-notification-fx-out-of-date';

    // Notification should only be shown to users on Firefox for desktop.
    if (client.isFirefoxDesktop) {
        client.getFirefoxDetails(function(details) {
            // Don't rely on UA strings as they can be altered by extensions, so use UITour instead (Bug 1406299).
            // User must be at least 2 major versions out of date and on release channel.
            if (client.isFirefoxOutOfDate(details.version, 2) && details.channel === 'release') {

                // Check that cookies are enabled before seeing if one already exists.
                if (typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled()) {
                    Mozilla.NotificationBanner.init(config);
                }
            }
        });
    }
});
