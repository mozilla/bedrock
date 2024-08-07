/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { getAMOExperiment } from './experiment-amo.es6.js';

const dataLayer = (window.dataLayer = window.dataLayer || []);

// Look for AMO experiment on DOM Ready.
if (typeof Mozilla.Utils !== 'undefined') {
    Mozilla.Utils.onDocumentReady(() => {
        // Add GA custom dimension for AMO experiments (Issue 10175).
        if (typeof window._SearchParams !== 'undefined') {
            const params = new window._SearchParams().params;
            const validParams = getAMOExperiment(params);

            if (validParams) {
                // GA4
                dataLayer.push({
                    event: 'experiment_view',
                    id: validParams['experiment'],
                    variant: validParams['variation']
                });
            }
        }
    });
}
