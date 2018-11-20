/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var client = Mozilla.Client;
    var survey = document.getElementById('fffy-survey-link');
    if (survey && !client.isMobile && Math.random() < 0.5) {
        var link = survey.querySelector('a');
        var linkHref = link.getAttribute('href');

        // show survey
        survey.style.display = 'block';
        window.dataLayer.push({
            'eLabel': 'Banner Impression',
            'data-banner-name': 'FFFY Survey Link',
            'data-banner-impression': '1',
            'event': 'non-interaction'
        });

        // survey tracking
        link.setAttribute('href', linkHref + window.location.search);
        link.addEventListener('click', function() {
            window.dataLayer.push({
                'eLabel': 'Banner Clickthrough',
                'data-banner-name': 'FFFY Survey Link',
                'data-banner-click': '1',
                'event': 'in-page-interaction'
            });
        });
    }
})();
