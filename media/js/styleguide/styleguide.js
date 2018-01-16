/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    var $sidebar = $('#sidebar');

    $sidebar.on('focusin', function() {
        $sidebar.toggleClass('child-focus');
    }).on('focusout', function() {
        $sidebar.toggleClass('child-focus');
    });

    $('#sidebar nav ul li.has-children > a').on('click', function(e) {
        e.preventDefault();

        var $li = $(this).parent('li');

        if ($li.hasClass('active')) {
            // close ul
            $(this).next().slideUp('fast', function() {
                $li.removeClass('active');
                $li.attr('aria-expanded', 'false');
            });
        } else {
            $li.addClass('active');
            // open ul
            $(this).next('ul').css('display', 'none').slideDown('fast', function() {
                $li.attr('aria-expanded', 'true');
            });

            // close siblings
            $li.siblings('li.has-children').find('ul').slideUp('fast', function() {
                var $parent = $(this).parent('li');
                $parent.removeClass('active');
                $parent.attr('aria-expanded', 'false');
            });
        }
    });
});
