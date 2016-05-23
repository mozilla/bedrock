/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// init core dataLayer object and push into dataLayer
$(function() {
    if (Mozilla && Mozilla.Analytics) {
        var dataLayer = window.dataLayer = window.dataLayer || [];

        dataLayer.push({
            'event': 'core-datalayer-loaded',
            'pageId': Mozilla.Analytics.getPageId()
        });

        Mozilla.Analytics.updateDataLayerPush();
    }
});
