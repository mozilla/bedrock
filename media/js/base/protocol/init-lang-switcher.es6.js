/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Initialize Protocol language switcher.
 */
import MzpLangSwitcher from '@mozilla-protocol/core/protocol/js/lang-switcher';

MzpLangSwitcher.init(function (previousLanguage, newLanguage) {
    // UA
    window.dataLayer.push({
        event: 'change-language',
        languageSelected: newLanguage,
        previousLanguage: previousLanguage
    });
    //GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'language selector',
        action: 'change to: ' + newLanguage
    });
});
