/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var variation = document.querySelector('.main-download').getAttribute('data-variant');

    function setAttribution(variation) {
        var params = {
            /* eslint-disable camelcase */
            utm_source: 'www.mozilla.org',
            utm_medium: 'experiment',
            utm_campaign: 'firefox_new_pre_download',
            utm_content: 'firefox_new_pre_download_v_' + variation
            /* eslint-enable camelcase */
        };

        function trackGAEvent() {
            window.dataLayer.push({
                'data-ex-name': 'firefox_new_pre_download',
                'data-ex-variant': 'v_' + variation
            });
        }

        Mozilla.CustomStubAttribution.init(params, trackGAEvent);
    }

    if (variation) {
        setAttribution(variation);
    }

})(window.Mozilla);
