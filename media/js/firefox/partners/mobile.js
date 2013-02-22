/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $) {
    'use strict';

    w.ga_track('');

    // mobile functionality
    w.attach_mobile = function() {
        setTimeout(function() {
            if (w.location.hash) {
                _show_scene(w.location.hash);
                w.location.hash = '';
            }
        }, 60);

        // hide back to top arrows
        $('.top').hide();

        // hide all articles except the first
        $('.partner-article[id!="overview"]').hide();

        // set overview as active
        $('a[href="#overview"]').parent('li').addClass('active');

        // hook up article nav
        $('#partner-menu a, #nav-main-menu a').on('click.mobile', function(e) {
            e.preventDefault();

            var $that = $(this);
            var $li = $that.parent('li');

            if (!$li.hasClass('active')) {
                _show_scene($that.attr('href'));
            }
        });
    };

    var _show_scene = function(anchor) {
        if (anchor === '#overview' || anchor === '#os' || anchor === '#marketplace' || anchor === '#android') {
            $('.partner-article:visible').fadeOut('fast', function() {
                $(anchor).fadeIn('fast');

                // #partner-menu
                $('a[href!="' + anchor + '"]').parent('li').removeClass('active');
                $('a[href="' + anchor + '"]').parent('li').addClass('active');

                var virtual_page = (anchor !== '#overview') ? anchor + '/' : '';
                w.ga_track(virtual_page);
            });
        } else if (anchor === '#location' || anchor === '#schedule') {
            $('a.modal[href="' + anchor + '"]:first').trigger('click');
        }
    };

    $('.toggle-form').off().on('click', function(e) {
        e.preventDefault();

        w.show_overlay('#form');

        w.ga_track('form/');

        return false;
    });

    // remove mobile functionality
    w.detach_mobile = function() {
        $('.partner-article').show();
        $('#partner-nav a, #nav-main-menu a').off('click.mobile');
    };
})(window, window.jQuery);
