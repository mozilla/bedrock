/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    // Hide the section title when the thank you message displays upon a successful signup
    $(document).ajaxSuccess(function(evt, xhr, settings, response) {
        // Check that it's the correct form and the response was a non-error
        if ((settings.url.indexOf('/newsletter/') > -1) && response.success) {
            //adjust min-height on thankyou message to compensate before removing the heading
            var sectionHeight = parseInt($('.section-subscribe > .content').height(), 10);
            $('#newsletter-form-thankyou').css('min-height', sectionHeight + 'px');
            $('.header-main').hide();
        }
    });
});
