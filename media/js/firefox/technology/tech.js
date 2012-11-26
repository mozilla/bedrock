/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* Close Links */
$(document).ready(function () {
    var $demos = $('#wall > section > article > article.hasademo');
    $demos.each(function (index, el) {
        $(el).mouseleave(function (e) {
            $(el).removeClass('closed');
        });
    });

    var $closeLinks = $('#wall > section > article > article a.close');
    $closeLinks.each(function (index, el) {
        $(el).click(function (e) {
            var $article = $(el.parentNode);
            $article.addClass('closed')
            e.preventDefault();
        });
    });
});



// Form demo
function submitForm() {
    document.getElementById('formdemo').className = 'submited';
    return false;
}
