/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var syncTimeout = setTimeout(showMobilePromo, 1500); // fallback for if UITour should fail.
    var mainContent = document.querySelector('.main-content');

    function showAccountsForm() {
        mainContent.classList.add('signed-out');

        Mozilla.Client.getFirefoxDetails(function(data) {
            Mozilla.FxaIframe.init({
                distribution: data.distribution,
                gaEventName: 'whatsnew-fxa'
            });
        });
    }

    function showMobilePromo() {
        mainContent.classList.add('signed-in');
    }

    Mozilla.UITour.getConfiguration('sync', function(config) {
        // clear UITour fallback timeout.
        clearTimeout(syncTimeout);

        // if timeout has already fired and mobile promo is visible, do nothing.
        if (mainContent.classList.contains('signed-in')) {
            return;
        }

        if (config.setup) {
            showMobilePromo();
        } else {
            showAccountsForm();
        }
    });

})(window.Mozilla);
