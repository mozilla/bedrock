/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrackProductDownload from '../../base/datalayer-productdownload.es6';
import MzpModal from '@mozilla-protocol/core/protocol/js/modal';

(function (Mozilla) {
    function onLoad() {
        const browserHelpContent = document.getElementById('browser-help');
        const browserHelpIcon = document.getElementById('icon-browser-help');
        const installerHelpContent = document.getElementById('installer-help');
        const installerHelpIcon = document.querySelectorAll(
            '.icon-installer-help'
        );
        const downloadButton = document.getElementById(
            'download-button-primary'
        );

        function showHelpModal(modalContent, modalTitle, eventLabel) {
            MzpModal.createModal(this, modalContent, {
                title: modalTitle,
                className: 'help-modal'
            });

            // UA
            window.dataLayer.push({
                event: 'in-page-interaction',
                eAction: 'link click',
                eLabel: eventLabel
            });
            // GA4
            window.dataLayer.push({
                event: 'widget_action',
                type: 'modal',
                action: 'open',
                name: eventLabel
            });
        }

        Mozilla.FirefoxDownloader.init();

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
        for (let i = 0; i < installerHelpIcon.length; i++) {
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

        // event tracking for GA4
        downloadButton.addEventListener(
            'click',
            function (event) {
                TrackProductDownload.handleLink(event);
            },
            false
        );
    }

    Mozilla.run(onLoad);
})(window.Mozilla);
