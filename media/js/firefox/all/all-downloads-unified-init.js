/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla){
    'use strict';

    var browserHelpContent = document.getElementById('browser-help');
    var downloadList = document.getElementById('all-downloads');
    var form = document.getElementById('product-select-form');
    var helpIcon = document.getElementById('icon-browser-help');

    if (!Mozilla.FirefoxDownloader.isSupported()) {
        downloadList.style.display = 'block';
        return;
    } else {
        form.classList.add('is-supported');
    }

    Mozilla.FirefoxDownloader.init();

    helpIcon.addEventListener('click', function(e) {
        e.preventDefault();

        Mzp.Modal.createModal(this, browserHelpContent, {
            title: helpIcon.textContent,
            className: 'browser-help-modal'
        });

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'Get Help'
        });
    }, false);

})(window.Mozilla);
