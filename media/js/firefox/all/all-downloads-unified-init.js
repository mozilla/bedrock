/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function (Mozilla) {
    'use strict';

    var MzpModal = require('@mozilla-protocol/core/protocol/js/modal');
    var MzpSideMenu = require('@mozilla-protocol/core/protocol/js/sidemenu');

    function onLoad() {
        var browserHelpContent = document.getElementById('browser-help');
        var browserHelpIcon = document.getElementById('icon-browser-help');
        var installerHelpContent = document.getElementById('installer-help');
        var installerHelpIcon = document.querySelectorAll(
            '.icon-installer-help'
        );

        function showHelpModal(modalContent, modalTitle, eventLabel) {
            MzpModal.createModal(this, modalContent, {
                title: modalTitle,
                className: 'help-modal'
            });

            window.dataLayer.push({
                event: 'in-page-interaction',
                eAction: 'link click',
                eLabel: eventLabel
            });
        }

        Mozilla.FirefoxDownloader.init();
        MzpSideMenu.init();

        // Browser help modal.
        browserHelpIcon.addEventListener(
            'click',
            function (e) {
                e.preventDefault();
                showHelpModal.call(
                    this,
                    browserHelpContent,
                    browserHelpIcon.textContent,
                    'Get Browser Help'
                );
            },
            false
        );

        // Installer help modal.
        for (var i = 0; i < installerHelpIcon.length; i++) {
            installerHelpIcon[i].addEventListener(
                'click',
                function (e) {
                    e.preventDefault();
                    showHelpModal.call(
                        this,
                        installerHelpContent,
                        e.target.textContent,
                        'Get Installer Help'
                    );
                },
                false
            );
        }
    }

    Mozilla.run(onLoad);
})(window.Mozilla);
