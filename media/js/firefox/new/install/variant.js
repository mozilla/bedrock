/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    function setAttributionValues(variant) {
        // preserve any existing utm params except for utm_content.
        var params = new window._SearchParams().utmParams();

        /* eslint-disable camelcase */
        return {
            utm_source: params.utm_source || 'www.mozilla.org',
            utm_medium: params.utm_medium || 'download_button',
            utm_campaign: params.utm_campaign || 'download_thanks_page',
            utm_content: 'download_thanks_install_experiment-v-' + variant,
            referrer: document.referrer
        };
        /* eslint-enable camelcase */
    }

    function init() {
        if (!Mozilla.StubAttribution.meetsRequirements()) {
            return;
        }

        var variant = document.querySelector('.main-download').getAttribute('data-variant');

        if (variant) {
            var data = setAttributionValues(variant);
            Mozilla.StubAttribution.requestAuthentication(data);

            window.dataLayer.push({
                'data-ex-name': 'download_thanks_install_experiment',
                'data-ex-variant': 'v-' + variant
            });
        }
    }

    init();

})(window.Mozilla);
