/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function($) {
    'use strict';

    Mozilla.Survey = function(config) {
        'use strict';

        // make sure we have necessary info to display the survey
        if (config.copyIntro && config.copyLink && config.surveyURL) {
            // default to displaying survey at the top of the page
            var $container = config.container ? $(config.container) : $('#strings');

            var $message = $('<div id="survey-message"><span class="survey-invite">' + config.copyIntro + '</span><a class="survey-button" href="' + config.surveyURL + '">' + config.copyLink + '</a></div>');

            $message.insertBefore($container);
        }
    };
})(window.jQuery);
