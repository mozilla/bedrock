/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    function getLocale() {
        var lang = document.getElementsByTagName('html')[0].getAttribute('lang');
        var locale;

        switch(lang) {
        case 'en-CA':
            locale = 'ca';
            break;
        case 'en-GB':
            locale = 'gb';
            break;
        default:
            locale = 'us';
        }

        return locale;
    }

    function setCohorts(locale) {
        var cohorts;

        switch(locale) {
        case 'ca':
            cohorts = {
                '1': 55,
                '2': 15,
                '3': 15,
                '4': 15
            };
            break;
        case 'gb':
            cohorts = {
                '1': 46,
                '2': 18,
                '3': 18,
                '4': 18
            };
            break;
        default:
            cohorts = {
                '1': 94,
                '2': 2,
                '3': 2,
                '4': 2
            };
        }

        return cohorts;
    }

    function getCopy(variation) {
        var data;

        switch(variation) {
        case '2':
            data = {
                title: 'Protect your privacy with Firefox',
                subtitle: '2X faster than before, with more control over your privacy than ever.'
            };
            break;
        case '3':
            data = {
                title: 'Fly faster on Firefox',
                subtitle: '2X faster than before, with more control over your privacy than ever.'
            };
            break;
        case '4':
            data = {
                title: 'Live your life, own your life with Firefox',
                subtitle: 'Your life is your business. Making a faster, more secure browser is ours.'
            };
            break;
        }

        return data;
    }

    function updateCopy(copy) {
        document.querySelector('.header-content h1').textContent = copy.title;
        document.querySelector('.header-content h2').textContent = copy.subtitle;
    }

    function setAttribution(variation) {
        var params = {
            /* eslint-disable camelcase */
            utm_source: 'www.mozilla.org',
            utm_medium: 'download_button',
            utm_campaign: 'firefox_new_page',
            utm_content: 'na_exp01_' + locale + '_' + variation
            /* eslint-enable camelcase */
        };

        function trackGAEvent() {
            window.dataLayer.push({
                'data-ex-name': 'na_exp01_' + locale,
                'data-ex-variant': 'v_' + variation
            });
        }

        Mozilla.CustomStubAttribution.init(params, trackGAEvent);
    }

    function handleCallback(variation) {
        var copy = getCopy(variation);

        if (copy) {
            updateCopy(copy);
        }

        setAttribution(variation);
    }

    if (window.site.platform !== 'windows') {
        return;
    }

    var locale = getLocale();
    var cohorts = setCohorts(locale);

    var lou = new Mozilla.TrafficCop({
        id: 'experiment-firefox-new-headline-' + locale,
        customCallback: handleCallback,
        variations: {
            '1': cohorts['1'], // control
            '2': cohorts['2'], // privacy
            '3': cohorts['3'], // speed
            '4': cohorts['4']  // purpose
        }
    });

    lou.init();

})(window.Mozilla);
