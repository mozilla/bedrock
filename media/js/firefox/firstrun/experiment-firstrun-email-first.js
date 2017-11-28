/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    /**
     * An experiment to show FxA's "email-first" flow where
     * the user first enters their email and then /signin
     * or /signup is displayed depending on whether the
     * account exists.
     *
     * 5% go to each bucket, 10% total.
     */
    var cop = new Mozilla.TrafficCop({
        id: 'experiment_firstrun_email_first',
        variations: {
            'v=a': 5,  // control
            'v=b': 5   // treatment - email first
        }
    });

    cop.init();
})(window.Mozilla);
