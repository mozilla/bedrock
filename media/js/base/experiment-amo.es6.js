/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function getAMOExperiment(params) {
    const allowedExperiment = /^\d{8}_amo_.[\w/.%-]{1,50}$/; // should match the format YYYYMMDD_amo_experiment_name.
    const allowedVariation = /^[\w/.%-]{1,50}$/; // allow alpha numeric & common URL encoded chars.

    if (
        Object.prototype.hasOwnProperty.call(params, 'experiment') &&
        Object.prototype.hasOwnProperty.call(params, 'variation')
    ) {
        const experiment = decodeURIComponent(params['experiment']);
        const variation = decodeURIComponent(params['variation']);

        if (
            allowedExperiment.test(experiment) &&
            allowedVariation.test(variation)
        ) {
            return {
                experiment: experiment,
                variation: variation
            };
        }
    }

    return null;
}

export { getAMOExperiment };
