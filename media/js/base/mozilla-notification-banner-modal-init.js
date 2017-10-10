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

    var _clickCallback = function() {
        Mozilla.Modal.createModal(this, $('.notification-modal-content'));
    };

    // try to get localized copy
    // if any of the below fail, the banner will detect missing strings and
    // will not initialize
    if (typeof utils !== 'undefined') {
        headingText = utils.trans('global-fx-out-of-date-banner-heading');
        messageText = utils.trans('global-fx-out-of-date-banner-message');
        confirmText = utils.trans('global-fx-out-of-date-banner-confirm');
        closeText = utils.trans('global-close');
    }

    var config = {
        'id': 'fx-out-of-date-banner',
        'name': 'fx-out-of-date',
        'heading': headingText,
        'message': messageText,
        'confirm': confirmText,
        'confirmClick': _clickCallback,
        'url': '/firefox/new/?scene=2',
        'close': closeText,
        'gaConfirmAction': 'Update Firefox', // GA - English only
        'gaConfirmLabel': 'Firefox for Desktop', // GA - English only
        'gaCloseLabel': 'Close' // GA - English only
    };

    /**
     * Determine if Firefox client is out of date.
     * @param {String} - Client version provided by UITour e.g. "58.0a1", "56.0".
     * @return {Boolean} - Returns true if client is at least 2 major versions out of date.
     */
    var _isClientOutOfDate = function(version) {
        var clientVersion = parseInt(version, 10);
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
    if (client.isFirefoxDesktop) {
        client.getFirefoxDetails(function(details) {
            // Don't rely on UA strings as they can be altered by extensions, so use UITour instead (Bug 1406299).
            if (_isClientOutOfDate(details.version) && details.channel === 'release') {
                // Check that cookies are enabled.
                if (typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled()) {
                    Mozilla.NotificationBanner.init(config);
                }
            }
        });
    }
});
