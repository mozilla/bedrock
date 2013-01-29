/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function($, TweenMax, TimelineLite, Quad) {
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

        var $giantfox = $('#giantfox');

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

        $('a[data-section="os-partners"]').on('click', function() {
            $giantfox.css('left', '-48%');
        });

        $('a[data-section="os-overview"]').on('click', function() {
            $giantfox.css('left', '52%');
        });

        var controller = $.superscrollorama();

        var tweens = {};

        tweens.slide_down = {
            from: { css: { top: -80, opacity: 0 }, immediateRender: true },
            to: { css: { top: 0, opacity: 1 } }
        };

        tweens.article_down = {
            from: { css: { top: -80 }, immediateRender: true },
            to: { css: { top: 0 } }
        };

        tweens.giantfox = {
            from: { css: { left: '60%', opacity: 0 }, immediateRender: true },
            to: { css: { left: '52%', opacity: 1 } }
        };

        $('.partner-article').each(function(i, article) {
            var $article = $(article);

            var my_tweens = [], tween, $tweener;

            if ($article.attr('id') !== 'overview') {
                tween = TweenMax.fromTo(
                    $article,
                    1,
                    tweens.article_down.from,
                    tweens.article_down.to
                );

                my_tweens.push(tween);
            }

            // build tween for each element in $article with class of tween
            $article.find('.tween').each(function(i, tweener) {
                $tweener = $(tweener);

                tween = TweenMax.fromTo(
                    $tweener,
                    0.5,
                    tweens.slide_down.from,
                    tweens.slide_down.to
                );

                my_tweens.push(tween);
            });

            if (my_tweens.length > 0) {
                controller.addTween(
                    '#' + $article.attr('id'),
                    (new TimelineLite()).append(my_tweens),
                    400, // scroll duration
                    0 // start offset
                );
            }
        });

        controller.addTween(
            '#giantfox',
            TweenMax.fromTo(
                $('#giantfox'),
                0.4,
                tweens.giantfox.from,
                tweens.giantfox.to
            ),
            100,
            -70
        );
    //});
})(window.jQuery, window.TweenMax, window.TimelineLite, window.Quad);
