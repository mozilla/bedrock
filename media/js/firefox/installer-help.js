/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $surveyContent = $('#survey-wrapper').show().detach();

    if ($surveyContent.length > 0) {
        $('aside.survey').show();
        $('#launch-survey').on('click', function(e) {
            e.preventDefault();
            Mozilla.Modal.createModal(this, $surveyContent);
        });
    }

})(window.jQuery);
