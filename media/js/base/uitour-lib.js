/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function () {
    'use strict';

    // create namespace
    if (typeof Mozilla.UITour === 'undefined') {
        Mozilla.UITour = {};
    }

    var themeIntervalId = null;
    function _stopCyclingThemes() {
        if (themeIntervalId) {
            clearInterval(themeIntervalId);
            themeIntervalId = null;
        }
    }

    function _sendEvent(action, data) {
        var event = new CustomEvent('mozUITour', {
            bubbles: true,
            detail: {
                action: action,
                data: data || {}
            }
        });

        document.dispatchEvent(event);
    }

    function _generateCallbackID() {
        return Math.random()
            .toString(36)
            .replace(/[^a-z]+/g, '');
    }

    function _waitForCallback(callback) {
        var id = _generateCallbackID();

        function listener(event) {
            if (typeof event.detail !== 'object') {
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
    }

    Mozilla.UITour.DEFAULT_THEME_CYCLE_DELAY = 10 * 1000;

    Mozilla.UITour.registerPageID = function (pageID) {
        _sendEvent('registerPageID', {
            pageID: pageID
        });
    };

    Mozilla.UITour.showHighlight = function (target, effect) {
        _sendEvent('showHighlight', {
            target: target,
            effect: effect
        });
    };

    Mozilla.UITour.hideHighlight = function () {
        _sendEvent('hideHighlight');
    };

    Mozilla.UITour.showInfo = function (
        target,
        title,
        text,
        icon,
        buttons,
        options
    ) {
        var buttonData = [];
        if (Array.isArray(buttons)) {
            for (var i = 0; i < buttons.length; i++) {
                buttonData.push({
                    label: buttons[i].label,
                    icon: buttons[i].icon,
                    style: buttons[i].style,
                    callbackID: _waitForCallback(buttons[i].callback)
                });
            }
        }

        var closeButtonCallbackID;
        var targetCallbackID;
        if (options && options.closeButtonCallback) {
            closeButtonCallbackID = _waitForCallback(
                options.closeButtonCallback
            );
        }
        if (options && options.targetCallback) {
            targetCallbackID = _waitForCallback(options.targetCallback);
        }

        _sendEvent('showInfo', {
            target: target,
            title: title,
            text: text,
            icon: icon,
            buttons: buttonData,
            closeButtonCallbackID: closeButtonCallbackID,
            targetCallbackID: targetCallbackID
        });
    };

    Mozilla.UITour.hideInfo = function () {
        _sendEvent('hideInfo');
    };

    Mozilla.UITour.previewTheme = function (theme) {
        _stopCyclingThemes();

        _sendEvent('previewTheme', {
            theme: JSON.stringify(theme)
        });
    };

    Mozilla.UITour.resetTheme = function () {
        _stopCyclingThemes();

        _sendEvent('resetTheme');
    };

    Mozilla.UITour.cycleThemes = function (themes, delay, callback) {
        _stopCyclingThemes();

        if (!delay) {
            delay = Mozilla.UITour.DEFAULT_THEME_CYCLE_DELAY;
        }

        function nextTheme() {
            var theme = themes.shift();
            themes.push(theme);

            _sendEvent('previewTheme', {
                theme: JSON.stringify(theme),
                state: true
            });

            callback(theme);
        }

        themeIntervalId = setInterval(nextTheme, delay);
        nextTheme();
    };

    Mozilla.UITour.showMenu = function (name, callback) {
        var showCallbackID;
        if (callback) {
            showCallbackID = _waitForCallback(callback);
        }
        _sendEvent('showMenu', {
            name: name,
            showCallbackID: showCallbackID
        });
    };

    Mozilla.UITour.hideMenu = function (name) {
        _sendEvent('hideMenu', {
            name: name
        });
    };

    Mozilla.UITour.showNewTab = function () {
        _sendEvent('showNewTab');
    };

    /**
     * Loads about:protections in the tour tab.
     * @since 70
     */
    Mozilla.UITour.showProtectionReport = function () {
        _sendEvent('showProtectionReport');
    };

    Mozilla.UITour.getConfiguration = function (configName, callback) {
        _sendEvent('getConfiguration', {
            callbackID: _waitForCallback(callback),
            configuration: configName
        });
    };

    Mozilla.UITour.setConfiguration = function (configName, configValue) {
        _sendEvent('setConfiguration', {
            configuration: configName,
            value: configValue
        });
    };

    /**
     * Request the browser open the Mozilla accounts page.
     *
     * @param {Object} [extraURLParams] - An optional object containing additional
     * parameters for the URL opened by the browser for reasons of promotional
     * campaign tracking. Each attribute of the object must have a name that
     * is a string, is "flow_id", "flow_begin_time", "device_id", "entrypoint_experiment",
     * "entrypoint_variation" or begins with `utm_` and contains only only alphanumeric
     * characters, dashes or underscores. The values may be any string and will automatically be encoded.
     * For Flow metrics, see details at https://mozilla.github.io/ecosystem-platform/docs/fxa-engineering/fxa-metrics#content-server
     * @since 79 renamed from `extraURLCampaignParams` to `extraURLParams`
     * @param {String} [email] - the optional FxA email value.
     * @param {String} [entrypoint] - the optional FxA entrypoint value. If not set, the browser will report `uitour`.
     * @since 80 added the "entrypoint" option.
     */
    Mozilla.UITour.showFirefoxAccounts = function (
        extraURLParams,
        entrypoint,
        email
    ) {
        _sendEvent('showFirefoxAccounts', {
            email: email,
            entrypoint: entrypoint,
            extraURLParams: JSON.stringify(extraURLParams)
        });
    };

    Mozilla.UITour.resetFirefox = function () {
        _sendEvent('resetFirefox');
    };

    Mozilla.UITour.addNavBarWidget = function (name, callback) {
        _sendEvent('addNavBarWidget', {
            name: name,
            callbackID: _waitForCallback(callback)
        });
    };

    Mozilla.UITour.setDefaultSearchEngine = function (identifier) {
        _sendEvent('setDefaultSearchEngine', {
            identifier: identifier
        });
    };

    Mozilla.UITour.setTreatmentTag = function (name, value) {
        _sendEvent('setTreatmentTag', {
            name: name,
            value: value
        });
    };

    Mozilla.UITour.getTreatmentTag = function (name, callback) {
        _sendEvent('getTreatmentTag', {
            name: name,
            callbackID: _waitForCallback(callback)
        });
    };

    Mozilla.UITour.setSearchTerm = function (term) {
        _sendEvent('setSearchTerm', {
            term: term
        });
    };

    Mozilla.UITour.openSearchPanel = function (callback) {
        _sendEvent('openSearchPanel', {
            callbackID: _waitForCallback(callback)
        });
    };

    Mozilla.UITour.toggleReaderMode = function () {
        _sendEvent('toggleReaderMode');
    };

    Mozilla.UITour.forceShowReaderIcon = function () {
        _sendEvent('forceShowReaderIcon');
    };

    Mozilla.UITour.ping = function (callback) {
        var data = {};
        if (callback) {
            data.callbackID = _waitForCallback(callback);
        }
        _sendEvent('ping', data);
    };

    var notificationListener = null;
    function _notificationListener(event) {
        if (typeof event.detail !== 'object') {
            return;
        }
        if (typeof notificationListener !== 'function') {
            return;
        }
        notificationListener(event.detail.event, event.detail.params);
    }

    Mozilla.UITour.observe = function (listener, callback) {
        notificationListener = listener;

        if (listener) {
            document.addEventListener(
                'mozUITourNotification',
                _notificationListener
            );
            Mozilla.UITour.ping(callback);
        } else {
            document.removeEventListener(
                'mozUITourNotification',
                _notificationListener
            );
        }
    };

    Mozilla.UITour.openPreferences = function (pane) {
        _sendEvent('openPreferences', {
            pane: pane
        });
    };

    Mozilla.UITour.closeTab = function () {
        _sendEvent('closeTab');
    };
})();
