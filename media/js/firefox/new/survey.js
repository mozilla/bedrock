/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var client = Mozilla.Client;
    var $survey = $('#firefox-new-survey-link');

    if (!client.isMobile && $survey.length && Math.random() < 0.05) {
        var link = $survey.attr('href');
        $survey.attr('href', link + window.location.search);
        $survey.css('display', 'block');
    }

})(window.jQuery);
