/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var buttons = document.querySelectorAll('.wn64-benefit-link');
    var content = document.getElementById('wn64-modal');
    var client = Mozilla.Client;

    for (var i = 0, len = buttons.length; i < len; i++) {
        var button = buttons[i];
        button.addEventListener('click', openModal);
        button.setAttribute('aria-role', 'button');
    }

    function openModal(e) {
        e.preventDefault();
        var trigger = e.target;
        var title = trigger.textContent;
        var app = 'mzp-t-firefox app-' + trigger.dataset.app;
        Mzp.Modal.createModal(e.target, content, {
            title: title,
            className: app,
            closeText: window.Mozilla.Utils.trans('global-close')
        });
    }

    function checkUpToDate() {
        // bug 1419573 - only show "Your Firefox is up to date" if it's the latest version.
        if (client.isFirefoxDesktop) {
            client.getFirefoxDetails(function(data) {
                if (data.isUpToDate) {
                    document.querySelector('.c-page-header').classList.add('is-up-to-date');
                }
            });
        }
    }

    Mozilla.UITour.ping(function() {
        checkUpToDate();
    });

})();
