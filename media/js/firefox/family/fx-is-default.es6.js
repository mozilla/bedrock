/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const FirefoxDefault = {
    isDefaultBrowser: () => {
        return new window.Promise((resolve, reject) => {
            Mozilla.UITour.getConfiguration('appinfo', (details) => {
                if (details.defaultBrowser) {
                    resolve();
                } else {
                    reject();
                }
            });
        });
    },

    isSupported: () => {
        return Mozilla.Client._isFirefoxDesktop() && 'Promise' in window;
    },

    init: () => {
        const main = document.querySelector('main');

        if (!FirefoxDefault.isSupported()) {
            return;
        }

        return new window.Promise(function (resolve) {
            Mozilla.UITour.ping(() => {
                main.classList.add('set-default-supported');
                FirefoxDefault.isDefaultBrowser()
                    .then(function () {
                        main.classList.add('is-firefox-default');
                        resolve();
                    })
                    .catch(() => resolve());
            });
        });
    }
};

export default FirefoxDefault;
