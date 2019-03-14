/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $html = $(document.documentElement);
    var client = window.Mozilla.Client;
    var $otherPlatformsModalLink = $('#other-platforms-modal-link');
    var $otherPlatformsLanguagesWrapper = $('#other-platforms-languages-wrapper');

    var getFirefoxStatus = function() {
        var userMajorVersion = client._getFirefoxMajorVersion();
        var latestMajorVersion = parseInt($html.attr('data-latest-firefox'), 10);

        // Detect whether the Firefox is up-to-date in a non-strict way. The minor version and channel are not
        // considered. This can/should be strict, once the UX especially for ESR users is decided. (Bug 939470)
        if (userMajorVersion === latestMajorVersion) {
            // the firefox-latest class prevents the download button from displaying
            return 'firefox-latest';
        } else if (userMajorVersion > latestMajorVersion) {
            // the firefox-pre-release class still shows the download button
            return 'firefox-pre-release';
        }
        return 'firefox-old';
    };

    var setFirefoxStatus = function() {
        // Windows XP/Vista warning overrides the Firefox status message
        if ($html.hasClass('xpvista')) {
            return;
        }

        var status = getFirefoxStatus();
        $html.addClass(status);
    };

    var initOtherPlatformsModal = function() {
        // show the modal cta button
        $otherPlatformsLanguagesWrapper.removeClass('hidden');

        $otherPlatformsModalLink.on('click', function(e) {
            e.preventDefault();
            Mozilla.Modal.createModal(this, $('#other-platforms'), {
                title: $(this).text(),
                className: 'other-platforms-modal'
            });

            window.dataLayer.push({
                'event': 'in-page-interaction',
                'eAction': 'link click',
                'eLabel': 'Download Firefox for another platform'
            });
        });
    };

    /**
     * Firefox for Desktop and Android have different page states
     * for latest, out-of-date, pre-release etc. For iOS there is
     * only a single state that shows the download button.
     */
    if (client.isFirefoxDesktop || client.isFirefoxAndroid) {
        setFirefoxStatus();
    }

    /**
     * Enable modal to optionally download Firefox for other platforms.
     * Don't show the modal for iOS or Android.
     */
    if ($otherPlatformsModalLink.length && client.isDesktop) {
        initOtherPlatformsModal();
    }

})(window.jQuery);
