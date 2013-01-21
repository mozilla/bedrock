/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

jQuery(document).ready(function ()
{
    // Smooth scroll-to for left menu navigation
    $('#partner-nav a, #nav-main-menu a').click(function() {
        var elementClicked = $(this).attr("href");
        var destination = $(elementClicked).offset().top;
        $("html:not(:animated),body:not(:animated)").animate({ scrollTop: destination-20}, 500 );
        return false;
    });
});
