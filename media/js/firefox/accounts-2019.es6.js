/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FxaForm from '../base/fxa-form.es6.js';
import FxaProductButton from '../base/fxa-product-button.es6.js';

// Prevent double-requesting Flow IDs, inits FxaForm even on non-firefox browsers.
if (window.Mozilla.Client.isFirefoxDesktop) {
    window.Mozilla.Client.getFxaDetails(function (details) {
        if (details.setup) {
            FxaProductButton.init();
        } else {
            FxaForm.init();
        }
    });
} else {
    FxaForm.init();
}
