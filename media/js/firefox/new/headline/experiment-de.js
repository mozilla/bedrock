/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    function getCopy(variation) {
        var data;

        switch(variation) {
        case '2':
            data = {
                title: 'Schütze deine Privatsphäre mit Firefox',
                subtitle: 'Läuft 2x schneller als vorher. Gibt dir noch mehr Kontrolle über deine Daten.'
            };
            break;
        case '3':
            data = {
                title: 'Mit Firefox schneller durchs Web',
                subtitle: 'Läuft 2x schneller als vorher. Gibt dir noch mehr Kontrolle über deine Daten.'
            };
            break;
        case '4':
            data = {
                title: 'Firefox. Dein Leben. Deine Daten.',
                subtitle: 'Was du machst, ist deine Sache. Ein schneller, sicherer Browser ist unsere.'
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
            utm_content: 'na_exp01_de_' + variation
            /* eslint-enable camelcase */
        };

        function trackGAEvent() {
            window.dataLayer.push({
                'data-ex-name': 'na_exp01_de',
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

    var lou = new Mozilla.TrafficCop({
        id: 'experiment-firefox-new-headline-de',
        customCallback: handleCallback,
        variations: {
            '1': 70, // control
            '2': 10, // privacy
            '3': 10, // speed
            '4': 10  // purpose
        }
    });

    lou.init();

})(window.Mozilla);
