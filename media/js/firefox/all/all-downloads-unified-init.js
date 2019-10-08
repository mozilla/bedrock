/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla){
    'use strict';

    function onLoad() {
        var browserHelpContent = document.getElementById('browser-help');
        var browserHelpIcon = document.getElementById('icon-browser-help');
        var installerHelpContent = document.getElementById('installer-help');
        var installerHelpIcon = document.querySelectorAll('.icon-installer-help');

        function showHelpModal(modalContent, modalTitle, eventLabel) {
            Mzp.Modal.createModal(this, modalContent, {
                title: modalTitle,
                className: 'help-modal'
            });

            window.dataLayer.push({
                'event': 'in-page-interaction',
                'eAction': 'link click',
                'eLabel': eventLabel
            });
        }

        Mozilla.FirefoxDownloader.init();

        // Browser help modal.
        browserHelpIcon.addEventListener('click', function(e) {
            e.preventDefault();
            showHelpModal.call(this, browserHelpContent, browserHelpIcon.textContent, 'Get Browser Help');
        }, false);

        // Installer help modal.
        for (var i = 0; i < installerHelpIcon.length; i++) {
            installerHelpIcon[i].addEventListener('click', function(e) {
                e.preventDefault();
                showHelpModal.call(this, installerHelpContent, e.target.textContent, 'Get Installer Help');
            }, false);
        }
    }

    Mozilla.run(onLoad);

})(window.Mozilla);
