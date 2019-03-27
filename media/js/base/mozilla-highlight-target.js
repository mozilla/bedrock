/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

/**
 * UITour widget for highlighting a Firefox icon via an in-page CTA link.
 * The widget highlights a target if available, else falls back to a regular link.
 */

/**
 * Dependencies:
 * js/firefox/australis/australis-uitour.js
 *
 * Example Usage:
 * --------------
 * HTML:
 *
 * <a href="https://www.mozilla.org" class="cta-button" data-highlight="privateWindow" role="button">
 *   Try Private Browsing
 * </a>
 *
 * JavaScript:
 *
 * Mozilla.HighlightTarget.init('.cta-button');
 *
 */

(function() {
    'use strict';

    var HighlightTarget = {};
    var _$document = $(document);
    var _$window = $(window);

    /**
     * Checks for target availability in the users pallet
     * @param {target} UITour target identifier.
     * @param {callback} function passed a boolean value based on target availability.
     */
    HighlightTarget.isTargetAvailable = function(target, callback) {

        if (typeof target !== 'string') {
            throw new Error('isTargetAvailable: first argument is not a string');
        }

        if (typeof callback !== 'function') {
            throw new Error('isTargetAvailable: second argument is not a function');
        }

        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            if (config.targets && $.inArray(target, config.targets) !== -1) {
                callback(true);
            } else {
                callback(false);
            }
        });
    };

    HighlightTarget.bindEvents = function() {
        HighlightTarget.unbindEvents();
        _$document.one('click.highlight-target', HighlightTarget.hideHighlight);
        _$document.one('visibilitychange.highlight-target', HighlightTarget.handleVisibilityChange);
        _$window.one('resize.highlight-target', HighlightTarget.hideHighlight);
    };

    HighlightTarget.unbindEvents = function() {
        _$document.off('click.highlight-target');
        _$document.off('visibilitychange.highlight-target');
        _$window.off('resize.highlight-target');
    };

    /**
     * Hide highlight if the tab becomes hidden
     * @param {docHidden} optional boolean value for testing purposes.
     */
    HighlightTarget.handleVisibilityChange = function(docHidden) {
        var hidden = docHidden !== 'undefined' ? docHidden : document.hidden;
        if (hidden) {
            HighlightTarget.hideHighlight();
        }
    };

    HighlightTarget.hideHighlight = function() {
        Mozilla.UITour.hideHighlight();
        HighlightTarget.unbindEvents();
    };

    /**
     * Highlight UITour target and bind hide events
     * @param {target} UITour target identifier.
     */
    HighlightTarget.showHighlight = function(target) {
        // call twice to correctly position highlight
        // https://bugzilla.mozilla.org/show_bug.cgi?id=1049130
        Mozilla.UITour.showHighlight(target, 'wobble');
        Mozilla.UITour.showHighlight(target, 'wobble');
        HighlightTarget.bindEvents();
    };

    HighlightTarget.doRedirect = function(href) {
        window.location = href;
    };

    HighlightTarget.handleCTAClick = function(e) {
        e.preventDefault();
        HighlightTarget.tryHighlight(e.target, e.target.dataset.highlight, e.target.href);
    };

    /**
     * Trigger a custom jQuery event on an element with supplied data object.
     * @param {target} DOM element.
     * @param {data} Array of a plain object.
     */
    HighlightTarget.fireCustomEvent = function(target, data) {
        $(target).trigger('highlight-target', data);
    };

    /**
     * Check to see if a target is available before highlighting,
     * else fall back to a regular link click.
     * @param {target} DOM element.
     * @param {target} UITour highlight identifier.
     * @param {href} Fallback link.
     */
    HighlightTarget.tryHighlight = function(target, id, href) {

        if (typeof target === 'undefined') {
            throw new Error('tryHighlight: first argument target should be a DOM element');
        }

        if (typeof id !== 'string') {
            throw new Error('tryHighlight: second argument target should be a string');
        }

        if (typeof href !== 'string') {
            throw new Error('tryHighlight: third argument href should be a string');
        }

        HighlightTarget.isTargetAvailable(id, function(available) {
            if (available) {
                HighlightTarget.showHighlight(id);
                HighlightTarget.fireCustomEvent(target, id);
            } else {
                HighlightTarget.doRedirect(href);
            }
        });
    };

    /**
     * Bind link click to highlight target.
     * @param {selector} CSS selector for CTA link(s).
     */
    HighlightTarget.bindCTA = function(selector) {
        $(selector).on('click.highlight-target', HighlightTarget.handleCTAClick);
    };

    /**
     * Unbind link click to highlight target.
     * @param {selector} CSS selector for CTA link(s).
     */
    HighlightTarget.unbindCTA = function(selector) {
        $(selector).off('click.highlight-target');
    };

    /**
     * Initialize UITour widget.
     * @param {selector} CSS selector for CTA link(s).
     */
    HighlightTarget.init = function(selector) {

        if (typeof selector === 'undefined') {
            throw new Error('init: first argument selector is undefined');
        }

        Mozilla.UITour.ping(function() {
            Mozilla.HighlightTarget.bindCTA(selector);
        });
    };

    window.Mozilla.HighlightTarget = HighlightTarget;

})();
