/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var featuresVarA = document.querySelectorAll('.features ul > li');
    var featuresVarC = document.querySelectorAll('.c-card-feature');

    function trackFeatureClick(e) {
        if (e.currentTarget) {
            var label = e.currentTarget.getAttribute('data-id');

            window.dataLayer.push({
                'event': 'in-page-interaction',
                'eAction': 'feature click',
                'eLabel': label
            });
        }
    }

    for (var i = 0; i < featuresVarC.length; i++) {
        featuresVarC[i].addEventListener('click', trackFeatureClick, false);
    }

    for (var j = 0; j < featuresVarA.length; j++) {
        featuresVarA[j].addEventListener('click', trackFeatureClick, false);
    }

    function getLocale() {
        var lang = document.getElementsByTagName('html')[0].getAttribute('lang');
        var locale;

        switch(lang) {
        case 'en-GB':
            locale = 'gb';
            break;
        case 'de':
            locale = 'de';
            break;
        }

        return locale;
    }

    function setAttribution(variation, locale) {
        var params = {
            /* eslint-disable camelcase */
            utm_source: 'www.mozilla.org',
            utm_medium: 'experiment',
            utm_campaign: 'descriptive_features_new_page',
            utm_content: 'eu_exp02_' + locale + '_' + variation
            /* eslint-enable camelcase */
        };

        function trackGAEvent() {
            window.dataLayer.push({
                'data-ex-name': 'eu_exp02_' + locale,
                'data-ex-variant': 'v_' + variation
            });
        }

        Mozilla.CustomStubAttribution.init(params, trackGAEvent);
    }

    var variation = document.querySelector('.main-download').getAttribute('data-variant');
    var locale = getLocale();

    if (variation && locale) {
        setAttribution(variation, locale);
    }

})(window.Mozilla);
