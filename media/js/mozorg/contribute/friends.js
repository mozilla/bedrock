/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla) {
    'use strict';

    var $newsletters = $('#id_newsletters');
    var $chkFxAndYou = $('#id_fx-and-you');

    $chkFxAndYou.on('change', function() {
        if ($chkFxAndYou.prop('checked')) {
            $newsletters.val($newsletters.val() + ',mozilla-and-you');
        } else {
            $newsletters.val($newsletters.val().replace(',mozilla-and-you', ''));
        }
    });

    Mozilla.SVGImage.fallback();
})(window.jQuery, window.Mozilla);
