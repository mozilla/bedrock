/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * Initialize Protocol language switcher.
 */
(function() {
    if (typeof Mzp === 'undefined' || typeof Mzp.LangSwitcher === 'undefined') {
        return;
    }

    Mzp.LangSwitcher.init(function(previousLanguage, newLanguage) {
        window.dataLayer.push({
            'event': 'change-language',
            'languageSelected': newLanguage,
            'previousLanguage': previousLanguage
        });
    });
})();
