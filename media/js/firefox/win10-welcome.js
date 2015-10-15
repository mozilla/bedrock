/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function($, Mozilla) {
    'use strict';

    var Win10Welcome = {};

    var _checkDefaultTimeout;
    var $document = $(document);
    var $defaultCta = $('.firefox-default-cta');
    var $learnMoreLinks = $('.firefox-learn-links');

    Win10Welcome.pollRetry = 0;

    // Checks if the default browser has been set and updates content.
    Win10Welcome.checkForDefaultSwitch = function() {
        Mozilla.FirefoxDefault.isDefaultBrowser(function(isDefault) {
            // Page will poll for default browser switch roughly once every 2 seconds
            // for a maximum of 1000 tries before going idle. This is in the edge case
            // event when a user might leave the tab open and forget about it.
            Win10Welcome.pollRetry += 1;

            if (Win10Welcome.pollRetry >= 1000) {
                Win10Welcome.clearDefaultCheck();
                return;
            }

            if (isDefault === 'yes') {
                Win10Welcome.onDefaultSwitch();
            }
        });
    };

    // Changes page content when user has set their default browser to Firefox.
    Win10Welcome.onDefaultSwitch = function() {
        Win10Welcome.clearDefaultCheck();
        $defaultCta.addClass('hidden');
        $learnMoreLinks.addClass('show');

        // Track in GA that the default switch was made

        window.dataLayer.push({
            'event': 'windows-10-welcome',
            'interaction': 'default-set',
        });
    };

    // Poll to see if default browser has been set by the user.
    // @param {interval} ms defaults to 2000
    Win10Welcome.setDefaultCheck = function() {
        clearInterval(_checkDefaultTimeout);
        _checkDefaultTimeout = setInterval(Win10Welcome.checkForDefaultSwitch, 2000);
    };

    // Clear polling for default browser switch
    Win10Welcome.clearDefaultCheck = function() {
        clearInterval(_checkDefaultTimeout);
        Win10Welcome.pollRetry = 0;
    };

    // Triggers "Set Firefox as your default browser" dialog and polls for confirmation.
    Win10Welcome.setFirefoxAsDefault = function() {
        Mozilla.FirefoxDefault.setDefaultBrowser();
        Win10Welcome.clearDefaultCheck();
        Win10Welcome.setDefaultCheck();

        // Track button click in GA

        window.dataLayer.push({
            'event': 'windows-10-welcome',
            'interaction': 'set-default-cta-click',
        });
    };

    // Shows "Make Firefox your default in 3 easy steps" CTA.
    Win10Welcome.showNonDefaultContent = function() {
        $('main').addClass('firefox-not-default');
        $defaultCta.removeClass('hidden');
        // bind "Let's do it!" CTA button.
        $('#set-default').on('click', Win10Welcome.setFirefoxAsDefault);
    };

    // Shows the 3 Learn more about Firefox links.
    Win10Welcome.showDefaultContent = function() {
        $('main').addClass('firefox-default');
    };

    // Track tab visible in GA and unbind events.
    Win10Welcome.trackTabVisibility = function() {

        window.dataLayer.push({
            'event': 'windows-10-welcome',
            'interaction': 'tab-visible',
        });
    };

    /**
     * Track the first time Welcome page tab is made visible in GA
     * @param {docHidden} boolean value for testing purposes only.
     */
    Win10Welcome.checkTabVisibility = function(docHidden) {
        var hidden = docHidden !== undefined ? docHidden : document.hidden;
        if (hidden) {
            $document.one('visibilitychange.win10', Win10Welcome.trackTabVisibility);
        } else {
            Win10Welcome.trackTabVisibility();
        }
    };

    /**
     * Check if Firefox is the default browser and show page content appropriately.
     * @param {tabHidden} boolean value passed for testing purposes only.
     */
    Win10Welcome.initPage = function() {
        Mozilla.FirefoxDefault.isDefaultBrowser(function(isDefault) {
            if (isDefault === 'no') {
                Win10Welcome.showNonDefaultContent();
                // start polling for default browser changes to update content when set.
                Win10Welcome.setDefaultCheck();
            } else {
                Win10Welcome.showDefaultContent();
            }

            // track page visibility in GA
            Win10Welcome.checkTabVisibility();

            // track initial browser default state on page load.

            window.dataLayer.push({
                'event': 'windows-10-welcome',
                'interaction': 'default-' + isDefault
            });
        });
    };

    Mozilla.Win10Welcome = Win10Welcome;

})(window.jQuery, window.Mozilla);
