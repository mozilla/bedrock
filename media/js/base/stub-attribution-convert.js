/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    Mozilla.Convert.onLoaded(function(convert) {
        if (convert) {
            var data = Mozilla.Convert.getCurrentExperiment(convert);
            if (data && data.experimentName && data.experimentVariation) {
                Mozilla.StubAttribution.experimentName = data.experimentName;
                Mozilla.StubAttribution.experimentVariation = data.experimentVariation;
            }
        }

        Mozilla.StubAttribution.init();
    });

})();
