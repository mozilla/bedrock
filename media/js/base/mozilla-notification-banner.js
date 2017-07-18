/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function() {
    'use strict';

    var NotificationBanner = {};
    var _options = {};

    NotificationBanner.COOKIE_CODE_ID = 'mozilla-notification-banner';
    NotificationBanner.COOKIE_EXPIRATION_DAYS = 21; // default cookie expiry 21 days
    NotificationBanner.COOKIE_INTERACTION_VALUE = 'interacted';

    /**
     * Gets notification cookie if it exists.
     * @return {String} cookie value if it exists else null.
     */
    NotificationBanner.getCookie = function() {
        return Mozilla.Cookies.getItem(NotificationBanner.COOKIE_CODE_ID);
    };

    /**
     * Generates cookie expiry date defaulting to 21 days.
     * @return {Date}
     */
    NotificationBanner.cookieExpiresDate = function(date) {
        var d = date || new Date();
        d.setTime(d.getTime() + (NotificationBanner.COOKIE_EXPIRATION_DAYS * 24 * 60 * 60 * 1000));
        return d.toUTCString();
    };

    /**
     * Sets a cookie to register that notification has either been displayed or interacted with.
     * @param {String} value - either the unique ID for a notification or COOKIE_INTERACTION_VALUE.
     */
    NotificationBanner.setCookie = function(value) {
        Mozilla.Cookies.setItem(NotificationBanner.COOKIE_CODE_ID, value, NotificationBanner.cookieExpiresDate(), '/');
    };

    /**
     * Redirects current page to CTA link target.
     */
    NotificationBanner.doRedirect = function(target) {
        window.location.href = target;
    };

    /**
     * Tracks interaction with notification close button in GA.
     */
    NotificationBanner.trackGAClose = function() {
        window.dataLayer.push({
            'data-banner-name': _options.name,
            'data-banner-dismissal': '1',
            'eAction' : 'banner dismissal',
            'eLabel': _options.closeLabel,
            'event': 'in-page-interaction'
        });
    };

    /**
     * Handles interaction with notification close button and removes from the DOM.
     */
    NotificationBanner.close = function() {
        var notification = document.querySelector('.notification-banner');
        var close = notification.querySelector('.notification-banner-close');
        var confirm = notification.querySelector('.notification-banner-confirm');

        if (notification) {
            close.removeEventListener('click', NotificationBanner.close, false);
            confirm.removeEventListener('click', NotificationBanner.confirm, false);

            document.body.removeChild(notification);
            NotificationBanner.setCookie(NotificationBanner.COOKIE_INTERACTION_VALUE);
            NotificationBanner.trackGAClose();
        }
    };

    /**
     * Tracks interaction with notification CTA button in GA.
     */
    NotificationBanner.trackGAConfirm = function() {
        window.dataLayer.push({
            'data-banner-name': _options.name,
            'data-banner-click': '1',
            'eAction' : _options.confirmAction,
            'eLabel': _options.confirmLabel,
            'event': 'in-page-interaction'
        });
    };

    /**
     * Handles interaction with notification CTA button.
     */
    NotificationBanner.confirm = function(e) {
        // for control + click just set the cookie.
        if (e.metaKey || e.ctrlKey) {
            NotificationBanner.setCookie(NotificationBanner.COOKIE_INTERACTION_VALUE);
            NotificationBanner.trackGAConfirm();
        }
        // else redirect after setting the cookie.
        else {
            e.preventDefault();
            NotificationBanner.setCookie(NotificationBanner.COOKIE_INTERACTION_VALUE);
            NotificationBanner.trackGAConfirm();
            NotificationBanner.doRedirect(e.target);
        }
    };

    /**
     * Binds click events for notification CTA and close buttons.
     */
    NotificationBanner.bind = function() {
        var confirm = document.querySelector('.notification-banner .notification-banner-confirm');
        var close = document.querySelector('.notification-banner .notification-banner-close');

        confirm.addEventListener('click', NotificationBanner.confirm, false);
        close.addEventListener('click', NotificationBanner.close, false);
    };

    /**
     * Constructs a notification ready to be inserted into the DOM.
     * @param {Object} options - Object literal with the same format defined for init()
     * @return {HTMLNode}
     */
    NotificationBanner.create = function(options) {
        var _notification = document.createDocumentFragment();
        var _container = document.createElement('div');
        var _content = document.createElement('div');
        var _contentContainer = document.createElement('div');
        var _heading = document.createElement('h2');
        var _message = document.createElement('p');
        var _confirm = document.createElement('a');
        var _close = document.createElement('button');

        _container.className = 'notification-banner';
        _content.className = 'content';
        _contentContainer.className = 'content-container';
        _heading.innerHTML = options.heading;
        _message.innerHTML = options.message;

        _confirm.className = 'notification-banner-confirm';
        _confirm.href = options.url;
        _confirm.innerHTML = options.confirm;

        _close.className = 'notification-banner-close';
        _close.innerHTML = options.close;

        _notification.appendChild(_container);
        _container.appendChild(_content);
        _content.appendChild(_contentContainer);
        _contentContainer.appendChild(_heading);
        _contentContainer.appendChild(_message);
        _contentContainer.appendChild(_confirm);
        _content.appendChild(_close);

        return _notification;
    };

    /**
     * Tracks impression of a notification in GA
     * @param {Object} options - Object literal with the same format defined for init()
     */
    NotificationBanner.trackGAShow = function(options) {
        var data = {
            'data-banner-name': options.name,
            'data-banner-impression': '1',
            'event': 'non-interaction'
        };

        // add optional experiment specific data attributes if present.
        if (options.experimentVariant && options.experimentName) {
            data['data-ex-variant'] = options.experimentVariant;
            data['data-ex-experiment'] = options.experimentName;
            data['data-ex-present'] = 'true';
        }
        
        window.dataLayer.push(data);
    };

    /**
     * Creates, displays and tracks impression of a notification.
     * @param {Object} options - Object literal with the same format defined for init()
     */
    NotificationBanner.show = function(options) {
        var notification = NotificationBanner.create(options);

        if (notification) {
            document.body.insertBefore(notification, document.body.firstChild);
            NotificationBanner.bind();
            NotificationBanner.setCookie(options.id);
            NotificationBanner.trackGAShow(options);
        }
    };

    /**
     * Performs basic validation for options passed to a notification.
     * @return {Boolean}
     */
    NotificationBanner.validateOptions = function(options) {
        if (typeof options.name !== 'string' ||
            typeof options.id !== 'string' ||
            typeof options.heading !== 'string' ||
            typeof options.message !== 'string' ||
            typeof options.confirm !== 'string' ||
            typeof options.confirmAction !== 'string' ||
            typeof options.confirmLabel !== 'string' ||
            typeof options.url !== 'string' ||
            typeof options.close !== 'string' ||
            typeof options.closeLabel !== 'string') {
            return false;
        }

        return true;
    };

    /**
     * Generic browser feature detect required for displaying a notification.
     * @return {Boolean}
     */
    NotificationBanner.cutsTheMustard = function() {
        return 'querySelector' in document &&
               'querySelectorAll' in document &&
               'addEventListener' in window &&
               'createDocumentFragment' in document;
    };

    /**
     * Initializes a new notification banner
     * @param {Object} options - Object literal containing the following:
     * {String} id (required) - Unique identifier used to track variations a visitor has seen e.g. 'fx-out-of-date-banner-copy1-direct-1'.
     * {String} name (required) - Generic name for the notification type e.g. 'fx-out-of-date'.
     * {String} experimentName (optional) - Generic name for tracking a specific experiment in GA e.g. 'fx-out-of-date-banner-copy1'.
     * {String} experimentVariant (optional) - Identifier for experiment variation in GA e.g. 'direct-1'.
     * {String} heading (required) - Copy string for notification heading.
     * {String} message (required) - Copy string for notification message / subheading.
     * {String} confirm (required) - Copy string for main CTA button.
     * {String} confirmAction (required) - String for action of CTA button in GA (this should always be English).
     * {String} confirmLabel (required) - String for labelling CTA button in GA (this should always be English).
     * {String} url (required) - URL for main CTA link.
     * {String} close (required) - Copy string for close button.
     * {String} closeLabel (required) - String for labelling close button in GA (this should always be English).
     */
    NotificationBanner.init = function(options) {
        // Basic feature detection for showing the notification.
        if (NotificationBanner.cutsTheMustard() && typeof options === 'object') {

            for (var i in options) {
                if (options.hasOwnProperty(i)) {
                    _options[i] = options[i];
                }
            }

            // if options are not satisfied, do not show a notification.
            if (!NotificationBanner.validateOptions(_options)) {
                return;
            }

            // Only show notifications if cookies are supported.
            if (typeof Mozilla.Cookies !== 'undefined' && Mozilla.Cookies.enabled() && NotificationBanner.getCookie() !== NotificationBanner.COOKIE_INTERACTION_VALUE) {
                NotificationBanner.show(_options);
            }
        }
    };

    window.Mozilla.NotificationBanner = NotificationBanner;
})();
