/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/*
This iteration of /whatsnew has multiple states:

1. User is not logged in to Sync (or UITour JS fails/times out):
    Display the FxA iframe

2. User is logged in to Sync, but does not have any mobile devices set up:
    Display App/Play store badges for Firefox Mobile

    i. Send to Device widget is available in the user's locale:
        Display the Send to Device widget, configured for Firefox Mobile
    ii. Send to Device widget is *not* available in the user's locale:
        Display a QR code for Firefox Mobile

3. User is logged in to Sync, and *does* have a mobile device set up:

    i. If they're in Germany, Austria, or Switzerland:
        a. Send to Device widget is available in the user's locale:
            Display the Send to Device widget, configured for Klar
        b. Send to Device widget is *not* available in the user's locale:
            Display a QR code for Klar
    ii. If they're in any other country *or* geolocation fails
        a. Send to Device widget is available in the user's locale:
            Display the Send to Device widget, configured for Focus
        b. Send to Device widget is *not* available in the user's locale:
            Display a QR code for Focus

*/

(function(Mozilla, $) {
    'use strict';

    Mozilla.WNP62 = {
        client: Mozilla.Client,
        klarCountryCodes: ['at', 'ch', 'de'],
        pageHead: document.getElementById('page-header'),
        logoMoz: document.getElementById('logo-moz'),
        logoPocket: document.getElementById('logo-pocket'),
        mainContent: document.getElementById('main-content'),
        $strings: $('#strings'),
        locale: document.documentElement.getAttribute('lang')
    };

    Mozilla.WNP62.showPocket = function() {
        // Show the content
        this.mainContent.classList.add('show-pocket');

        // swap out Mozilla logo for Pocket logo
        this.pageHead.classList.add('show-pocket');

        // Set the title
        document.title = this.$strings.data('pocket-title');
    };

    Mozilla.WNP62.showFxa = function() {
        // Show the content
        this.mainContent.classList.add('show-fxa');

        // Set the title
        document.title = this.$strings.data('fxaccount-title');

        // initialize the FxA iframe
        this.client.getFirefoxDetails(function(data) {
            Mozilla.FxaIframe.init({
                distribution: data.distribution,
                gaEventName: 'whatsnew-fxa'
            });
        });
    };

    Mozilla.WNP62.showFirefoxMobile = function() {
        // Show the content
        this.mainContent.classList.add('show-fx-mobile');

        // Set the title
        document.title = this.$strings.data('fxmobile-title');

        var form = new Mozilla.SendYourself('send-firefox');
        form.init();
    };

    Mozilla.WNP62.geolocate = function(callback) {
        $.get('/country-code.json')
            .done(function(data) {
                if (data && data.country_code) {
                    callback(data.country_code.toLowerCase());
                } else {
                    callback();
                }
            })
            .fail(function() {
                callback();
            });
    };

    Mozilla.WNP62.showFocusOrKlar = function(countryCode, product) {
        // Show the content
        this.mainContent.classList.add('show-' + product);

        // Set the title
        document.title = this.$strings.data('fxfocus-title');

        var form = new Mozilla.SendYourself('send-' + product);
        form.init(countryCode);
    };

    Mozilla.WNP62.chooseFocusOrKlar = function(countryCode) {
        var product = 'focus';

        if (countryCode && this.klarCountryCodes.includes(countryCode)) {
            product = 'klar';
        }

        this.showFocusOrKlar(countryCode, product);
    };

    Mozilla.WNP62.checkUpToDate = function() {
        // bug 1419573 - only show "Your Firefox is up to date" if it's the latest version.
        if (this.client.isFirefoxDesktop) {
            this.client.getFirefoxDetails(function(data) {
                if (data.isUpToDate) {
                    document.querySelector('.page-header').classList.add('show-up-to-date-message');
                }
            });
        }
    };

    Mozilla.WNP62.init = function(fxaDetails) {
        this.checkUpToDate();

        // if user is not signed in to FxA...
        if (!fxaDetails.setup) {
            // Show Pocket for English locales
            if (['en', 'en-US', 'en-CA', 'en-GB', 'en-ZA'].indexOf(this.locale) >= 0) {
                this.showPocket();
            // Show FxA for everyone else
            } else {
                this.showFxa();
            }
        // if the user is signed in to FxA but doesn't have any mobile devices set up, show Fx mobile content
        } else if (fxaDetails.mobileDevices === 'unknown' || fxaDetails.mobileDevices === 0) {
            this.showFirefoxMobile();
        // if user is signed in to FxA and has mobile devices set up, perform geo lookup
        // to determine whether to show Focus or Klar content
        } else {
            this.geolocate(this.chooseFocusOrKlar.bind(this));
        }

    };
})(window.Mozilla, window.jQuery);
