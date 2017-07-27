/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/*
Dearest future developer - This file currently serves both /features/sync and
/features/send-tabs because they are practically identical. If/when divergence
occurs, send-tabs should get its own .js file.

Thank you for your hard work.
*/

(function() {
    'use strict';

    Mozilla.SyncPage.init({
        client: window.Mozilla.Client
    });
})();
