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
        const downloadButtons = document.querySelectorAll('.download-link');
        const partialTarget = document.getElementById('partial-target');

        function showHelpModal(modalContent, modalTitle, eventLabel) {
            MzpModal.createModal(this, modalContent, {
                title: modalTitle,
                className: 'help-modal'
            });

            // GA4
            window.dataLayer.push({
                event: 'widget_action',
                type: 'modal',
                action: 'open',
                name: eventLabel
            });
        }

        // Browser help modal.
        if (browserHelpIcon) {
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
        }

        // Installer help modal.
        if (installerHelpIcon) {
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
        }

        // event tracking for GA4
        if (downloadButtons) {
            for (let i = 0; i < downloadButtons.length; ++i) {
                const downloadButton = downloadButtons[i];
                downloadButton.addEventListener(
                    'click',
                    function (event) {
                        TrackProductDownload.handleLink(event);
                    },
                    false
                );
            }
        }

        // A fetch helper since we use this in both the on click and popstate.
        // pushState is a boolean so we avoid pushing state if triggered from popstate.
        function fetchContent(url, pushState = false) {
            fetch(url, {
                // Signifies to backend to return partial HTML.
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                // Ignore what's cached and also don't cache this response.
                // This is so we don't get full html pages when we expect partial html, or vice versa.
                cache: 'no-store'
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then((html) => {
                    partialTarget.innerHTML = html;
                    if (pushState) {
                        history.pushState({ path: url }, '', url);
                    }
                })
                .catch((error) => {
                    throw new Error(
                        'There was a problem with the fetch operation:',
                        error
                    );
                });
        }

        // Override click events for drill-down links.
        partialTarget.addEventListener('click', function (event) {
            const anchor = event.target.closest('a');
            if (anchor && anchor.matches('.load-content-partial')) {
                event.preventDefault();
                fetchContent(anchor.href, true);
            }
        });

        // Add popstate listener so we return partial HTML with browser back button.
        window.addEventListener('popstate', function (event) {
            if (!event.state) {
                return;
            }

            fetchContent(event.state.path, false);
        });

        // Ensure initial state is set up when the page loads so root page is in popstate.
        window.addEventListener('DOMContentLoaded', () => {
            const url = window.location.href;
            history.replaceState({ path: url }, '', url);
        });
    }

    Mozilla.run(onLoad);
})(window.Mozilla);
