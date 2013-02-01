/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, TweenMax, TimelineLite, Power2, Quad) {
    'use strict';

    // i heard document.ready isn't necessary anymore. just trying it out...
    //$(document).ready(function () {
        $('#foxtail').sprite({fps: 12, no_of_frames: 44, rewind: true});

        // Smooth scroll-to for left menu navigation
        $('#partner-nav a, #nav-main-menu a').click(function() {
            var elementClicked = $(this).attr("href");
            var destination = $(elementClicked).offset().top;
            $("html:not(:animated),body:not(:animated)").animate({ scrollTop: destination-20}, 500 );
            return false;
        });

        var $giantfox = $('#giantfox');
        var $phone = $('#phone-common');
        var $phone_android = $('#phone-android');

        // side scrolling sections
        $('.view-section').on('click', function(e) {
            e.preventDefault();

            // needed to calculate percentage offsets?
            var doc_width = $(w.document).width();

            var link = $(this);

            var article = link.parents('article:first');

            // which section is currently displayed?
            var orig = article.find('section[data-current="1"]:first');
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

                section.css('left', new_left + '%').attr('data-current', 0);
            });

            // update current section
            dest.attr('data-current', 1);
        });

        $('a[data-section="os-partners"]').on('click', function() {
            $giantfox.css('left', '-720px');
        });

        $('a[data-section="os-overview"]').on('click', function() {
            $giantfox.css('left', '600px');
        });

        var controller = $.superscrollorama();

        var tweens = {};

        tweens.slide_down = {
            from: {
                css: { top: 80, opacity: 0 },
                immediateRender: true
            },
            to: { css: { top: 0, opacity: 1 } }
        };

        tweens.article_os = {
            from: {
                css: { top: 0, ease: Power2.easeOut },
                immediateRender: true
            },
            to: { css: { top: -120 } }
        };

        tweens.article_marketplace = {
            from: {
                css: { top: -120, ease: Power2.easeOut },
                immediateRender: true
            },
            to: { css: { top: -240 } }
        };

        tweens.article_android = {
            from: {
                css: { top: -240, ease: Power2.easeOut },
                immediateRender: true
            },
            to: { css: { top: -360 } }
        };

        tweens.phone_os = {
            css: { top: 944, ease: Power2.easeInOut }
        };
        tweens.phone_marketplace = {
            css: { top: 1520, ease: Power2.easeInOut },
            onStart: function() {
                $phone.css('z-index', 112);
            },
            onReverseComplete: function() {
                $phone.css('z-index', 110);
            }
        };
        tweens.phone_android = { css: { top: 2200, ease: Power2.easeInOut } };

        // only animate giantfox if on first section of #os
        var _animate_giantfox = function() {
            var left = $('#os-overview').position().left;

            return (left === 0) ? true : false;
        };

        tweens.giantfox = {
            from: {
                css: { left: 800, opacity: 0 },
                immediateRender: true
            },
            to: {
                css: { left: 500, opacity: 1 },
                onUpdateParams: ["{self}"],
                onUpdate: function(tween) {
                    /*
                    // make sure tween isn't in the middle
                    var progress = tween.progress();

                    if (progress === 0 || progress === 1) {
                        console.log('checking...');
                        var ok = _animate_giantfox();
                        console.log(ok);
                        if (ok) {
                            console.log('playing');
                            tween.play();
                        } else {
                            console.log('pausing');
                            tween.progress(1);
                            tween.pause();
                        }
                    }
                    */
                }
            }
        };

        $('.partner-article').each(function(i, article) {
            var $article = $(article);

            var my_tweens = [], tween, $tweener;

            if ($article.attr('id') !== 'overview') {
                controller.addTween(
                    '#' + $article.attr('id'),
                    TweenMax.to(
                        $phone,
                        1,
                        tweens['phone_' + $article.attr('id')]
                    ),
                    0,
                    0
                );

                tween = TweenMax.fromTo(
                    $article,
                    0.5,
                    tweens['article_' + $article.attr('id')].from,
                    tweens['article_' + $article.attr('id')].to
                );

                my_tweens.push(tween);
            }

            // build tween for each element in $article with class of tween
            $article.find('.tween').each(function(i, tweener) {
                $tweener = $(tweener);

                tween = TweenMax.fromTo(
                    $tweener,
                    0.6,
                    tweens.slide_down.from,
                    tweens.slide_down.to
                );

                my_tweens.push(tween);
            });

            if (my_tweens.length > 0) {
                controller.addTween(
                    '#' + $article.attr('id'),
                    (new TimelineLite()).append(my_tweens),
                    250, // scroll duration
                    -200 // start offset
                );
            }
        });

        controller.addTween(
            '#android',
            TweenMax.to(
                $phone_android,
                0.8,
                { css: { bottom: 0, ease: Power2.easeOut } }
            ),
            0,
            0
        );

        // BIG TAIL FIREFOX!
        controller.addTween(
            '#giantfox',
            TweenMax.fromTo(
                $giantfox,
                0.8,
                tweens.giantfox.from,
                tweens.giantfox.to
            ),
            0,
            -200
        );
    //});
})(window, window.jQuery, window.TweenMax, window.TimelineLite, window.Power2, window.Quad);
