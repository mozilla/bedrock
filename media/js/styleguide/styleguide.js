/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {

    $('#sidebar')
        .focusin(function(e) { $('#sidebar').toggleClass('child-focus'); })
        .focusout(function(e) { $('#sidebar').toggleClass('child-focus'); });

    $('#sidebar nav ul li.has-children > a').click(function(e) {
        e.preventDefault();

        var $li = $(this).parent('li');

        if ($li.hasClass('active')) {
            // close ul
            $(this).next()
                .slideUp('fast', function() {
                    $li.removeClass('active');
                })
        } else {
            $li.addClass('active');

            // open ul
            $(this).next('ul')
                .css('display', 'none')
                .slideDown('fast');

            // close siblings
            $li
                .siblings('li.has-children')
                .find('ul')
                .slideUp(
                    'fast',
                    function() {
                        $(this)
                            .parent('li')
                            .removeClass('active');
                    }
                );
        }

    });

});
