/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    function getVariantName() {
        var v = window.location.search.match(new RegExp('[?&]v=([^&#]*)'));
        var variant = v && v[1];
        var variantName;

        switch (variant) {
        case '1':
            variantName = 'control';
            break;
        case '2':
            variantName = 'quick install copy';
            break;
        case '3':
            variantName = 'switch page';
            break;
        }

        return variantName;
    }

    var variantName = getVariantName();

    if (variantName) {
        window.dataLayer = [{
            'data-ex-variant': getVariantName(),
            'data-ex-experiment': 'switch'
        }];
    }
})();
