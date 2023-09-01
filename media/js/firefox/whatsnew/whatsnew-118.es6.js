/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const FirefoxDefault = {
    isDefaultBrowser: () => {
        return new window.Promise((resolve, reject) => {
            FirefoxDefault.tourTimeout = setTimeout(function () {
                // UITour was too slow to reply
                FirefoxDefault.showAltCTAButton();
                resolve();
            }, 1000);
            Mozilla.UITour.getConfiguration('appinfo', (details) => {
                if (details.defaultBrowser) {
                    // UITour reports Firefox is default browser
                    FirefoxDefault.showAltCTAButton();
                    resolve();
                } else {
                    // UITour reports Firefox is not default browser
                    FirefoxDefault.showSetDefaultButton();
                    reject();
                }
            });
        });
    },

    isSupported: () => {
        return Mozilla.Client._isFirefoxDesktop() && 'Promise' in window;
    },

    showSetDefaultButton: () => {
        clearTimeout(FirefoxDefault.tourTimeout);
        document.querySelector('main').classList.add('fx-not-default');

        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-118',
            eLabel: 'firefox-not-default'
        });
    },

    showAltCTAButton: () => {
        clearTimeout(FirefoxDefault.tourTimeout);
        document.querySelector('main').classList.add('is-firefox-default');

        window.dataLayer.push({
            event: 'non-interaction',
            eAction: 'whatsnew-118',
            eLabel: 'firefox-default'
        });
    },

    init: () => {
        if (!FirefoxDefault.isSupported()) {
            // not firefox
            document.querySelector('main').classList.add('fx-not-default');
            return;
        }
        return new window.Promise(function (resolve, reject) {
            FirefoxDefault.isDefaultBrowser()
                .then(
                    function () {
                        FirefoxDefault.showAltCTAButton();
                        resolve();
                    },
                    function () {
                        document;
                        FirefoxDefault.showSetDefaultButton();
                        resolve();
                    }
                )
                .catch(() => reject());
        });
    }
};

FirefoxDefault.init();
