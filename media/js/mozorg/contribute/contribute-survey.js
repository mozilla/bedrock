/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    $(document).ready(function() {
        var $survey = $('#survey-message');
        $survey.addClass('show');
        setTimeout(function() {
            $survey.addClass('animate');
        }, 500);
    });

})(window.jQuery);