/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $html = $(document.documentElement);
    var client = window.Mozilla.Client;
    var $modalLink = $('#other-platforms-modal-link');

    var uiTourSendEvent = function(action, data) {
        var event = new CustomEvent('mozUITour', {
            bubbles: true,
            detail: {
                action: action,
                data: data || {}
            }
        });

        document.dispatchEvent(event);
    };

    var uiTourWaitForCallback = function(callback) {
        var id = Math.random().toString(36).replace(/[^a-z]+/g, '');

        function listener(event) {
            if (typeof event.detail != 'object') {
                return;
            }
            if (event.detail.callbackID !== id) {
                return;
            }

            document.removeEventListener('mozUITourResponse', listener);
            callback(event.detail.data);
        }
        document.addEventListener('mozUITourResponse', listener);

        return id;
    };

    var showRefreshButton = function(canReset) {
        if (canReset) {
            $html.addClass('show-refresh');

            $('#refresh-firefox').on('click', function() {
                uiTourSendEvent('resetFirefox');
            });
        }
    };

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
        var status = getFirefoxStatus();
        $html.addClass(status);

        if (status === 'firefox-latest' && client.isFirefoxDesktop) {
            // if user is on desktop release channel and has latest version, offer refresh button
            client.getFirefoxDetails(function(data) {
                // data.accurate will only be true if UITour API is working.
                if (data.channel === 'release' && data.accurate) {
                    // Bug 1274207 only show reset button if user profile supports it.
                    uiTourSendEvent('getConfiguration', {
                        callbackID: uiTourWaitForCallback(showRefreshButton),
                        configuration: 'canReset'
                    });
                }
            });
        }
    };

    var initOtherPlatformsModal = function() {
        // show the modal cta button
        $modalLink.removeClass('hidden');

        $modalLink.on('click', function(e) {
            e.preventDefault();
            Mozilla.Modal.createModal(this, $('#other-platforms'), {
                title: $(this).text()
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
    if (client.isFirefoxDesktop ||client.isFirefoxAndroid) {
        setFirefoxStatus();
    }

    /**
     * Enable modal to optionally download Firefox for other platforms.
     * Don't show the modal for iOS or Android.
     */
    if ($modalLink.length && client.isDesktop) {
        initOtherPlatformsModal();
    }

})(window.jQuery);
