/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla) {
    'use strict';

    var variant = document.querySelector('.main-download').getAttribute('data-variant');

    var params = {
        /* eslint-disable camelcase */
        utm_source: 'www.mozilla.org',
        utm_medium: 'download_button',
        utm_campaign: 'download_thanks_page',
        utm_content: 'download_thanks_install_experiment-v-' + variant
        /* eslint-enable camelcase */
    };

    function trackGAEvent() {
        window.dataLayer.push({
            'data-ex-name': 'download_thanks_install_experiment',
            'data-ex-variant': 'v-' + variant
        });
    }

    if (variant) {
        Mozilla.CustomStubAttribution.init(params, trackGAEvent);
    }

})(window.Mozilla);
