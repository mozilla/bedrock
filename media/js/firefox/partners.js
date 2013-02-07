/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, enquire, Modernizr) {
    'use strict';

    // tablet is good enough for full experience?
    enquire.register("screen and (min-width: 760px)", {
        deferSetup: true, // don't run setup until mq matches
        setup: function() {
            Modernizr.load([{
                both: [ '/media/js/libs/jquery.pageslide.min.js', '/media/js/libs/tweenmax.min.js', '/media/js/libs/superscrollorama.js', '/media/js/libs/jquery.spritely-0.6.1.js', '/media/js/firefox/partners/desktop.js' ],
                complete: function() {
                    // no action needed?
                }
            }]);
        },
        match: function() {
            // remove mobile hooks (fires before setup above)
            _detach_mobile();
        },
        unmatch: function() {
            // no action needed?
            _attach_mobile();
            // currently no way of unbinding superscrollorama stuff (wut!?)
            // however, only desktop users should ever go from desktop to mobile, so...it's ok?
        }
    }, true).listen(); // true param here forces non-mq browsers to match this rule
    // so, i don't think we need a polyfill

    // mobile functionality
    var _attach_mobile = function() {
        // hide back to top arrows
        $('.top').hide();

        // hide all articles except the first
        $('.partner-article[id!="overview"]').hide();

        // set overview as active
        $('a[href="#overview"]').parent('li').addClass('active');

        // hook up article nav
        $('#partner-nav a, #nav-main-menu a').on('click.mobile', function(e) {
            e.preventDefault();

            var $that = $(this);
            var $li = $that.parent('li');

            if (!$li.hasClass('active')) {
                $('.partner-article:visible').fadeOut('fast', function() {
                    $($that.attr('href')).fadeIn('fast');

                    $('a[href!="' + $that.attr('href') + '"]').parent('li').removeClass('active');
                    $('a[href="' + $that.attr('href') + '"]').parent('li').addClass('active');
                });
            }
        });
    };

    // remove mobile functionality
    var _detach_mobile = function() {
        $('.partner-article').show();
        $('#partner-nav a, #nav-main-menu a').off('click.mobile');
    };

    _attach_mobile();
})(window, window.jQuery, window.enquire, window.Modernizr);
