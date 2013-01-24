/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function($, TweenMax, Quad) {
    'use strict';

    // i heard document.ready isn't necessary anymore. just trying it out...
    //$(document).ready(function () {
        // Smooth scroll-to for left menu navigation
        $('#partner-nav a, #nav-main-menu a').click(function() {
            var elementClicked = $(this).attr("href");
            var destination = $(elementClicked).offset().top;
            $("html:not(:animated),body:not(:animated)").animate({ scrollTop: destination-20}, 500 );
            return false;
        });

        $('.view-section').on('click', function(e) {
            e.preventDefault();

            // needed to calculate percentage offsets?
            var doc_width = $(document).width();

            var link = $(this);

            var article = link.parents('article:first');

            // which section are we in?
            var orig = link.parents('section:first');
            var orig_pos = Number(orig.data('pos'));

            // which section are we going to?
            var dest = $('#' + link.data('section'));
            var dest_pos = Number(dest.data('pos'));

            // what's the difference in position? multiply by 100 to get percentage
            var delta = (dest_pos - orig_pos) * 100;

            article.find('section').each(function(i, el) {
                var section = $(el);

                // percentage position of this section
                // (left will be in px and will be multiple of doc_width)
                var el_left = (section.position().left/doc_width) * 100;

                var new_left = el_left - delta;

                section.css('left', new_left + '%');
            });
        });

        var controller = $.superscrollorama();

        var tweens = {};

        tweens.slide_up = {
            from: { css: { top: 50, opacity: 0.2 }, immediateRender: true },
            to: { css: { top: 0, opacity: 1 } }
        };

        tweens.slide_right = {
            from: { css: { left: 150, opacity: 0 }, immediateRender: true },
            to: { css: { left: 0, opacity: 1 } }
        };

        tweens.slide_left = {
            from: { css: { right: 150, opacity: 0 }, immediateRender: true },
            to: { css: { right: 0, opacity: 1 } }
        };

        $('.tween').each(function(i, el) {
            var $el = $(el);

            var el_tween = $el.data('tween') || 'slide_up';

            if (el_tween) {
                controller.addTween(
                    '#' + $el.attr('id'), // scroll target
                    TweenMax.fromTo(
                        $el, // element to tween
                        0.4, // tween duration
                        tweens[el_tween].from,
                        tweens[el_tween].to
                    ),
                    100, // scroll length of tween
                    -250 // animation offset. begin 200px above scroll target
                );
            }
        });

        /*
        controller.addTween(
            '#os-overview-headline', // scroll target
            TweenMax.fromTo(
                $('#os-overview-headline'), // element to tween
                0.4, // tween duration
                tweens.slide_up.from,
                tweens.slide_up.to
            ),
            100, // scroll length of animation
            -250 // animation offset. begin animation 200px *above* target
        );

        controller.addTween(
            '#os-overview-intro',
            TweenMax.fromTo(
                $('#os-overview-intro'),
                0.4,
                parallax_from,
                parallax_to
            ),
            100,
            -250
        );

        controller.addTween(
            '#os-overview-logos',
            TweenMax.fromTo(
                $('#os-overview-logos'),
                0.4,
                parallax_from,
                parallax_to
            ),
            100,
            -250
        );
        */
    //});
})(window.jQuery, window.TweenMax, window.Quad);
