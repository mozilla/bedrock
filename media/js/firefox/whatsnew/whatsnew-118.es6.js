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
                resolve();
            }, 1000);
            Mozilla.UITour.getConfiguration('appinfo', (details) => {
                if (details.defaultBrowser) {
                    // UITour reports Firefox is default browser
                    // UA
                    window.dataLayer.push({
                        event: 'non-interaction',
                        eAction: 'whatsnew-118',
                        eLabel: 'firefox-default'
                    });
                    // GA4
                    window.dataLayer.push({
                        event: 'dimension_set',
                        firefox_isDefault: true
                    });
                    resolve();
                } else {
                    // UITour reports Firefox is not default browser
                    // UA
                    window.dataLayer.push({
                        event: 'non-interaction',
                        eAction: 'whatsnew-118',
                        eLabel: 'firefox-not-default'
                    });
                    // GA4
                    window.dataLayer.push({
                        event: 'dimension_set',
                        firefox_isDefault: false
                    });
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
    },

    showAltCTAButton: () => {
        clearTimeout(FirefoxDefault.tourTimeout);
        document.querySelector('main').classList.add('is-firefox-default');
    },

    init: () => {
        if (!FirefoxDefault.isSupported()) {
            // not firefox
            document.querySelector('main').classList.add('fx-not-default');
            return;
        }

        FirefoxDefault.isDefaultBrowser()
            .then(FirefoxDefault.showAltCTAButton)
            .catch(FirefoxDefault.showSetDefaultButton);
    }
};

FirefoxDefault.init();
