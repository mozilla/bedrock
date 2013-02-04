/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, TweenMax, TimelineLite, Power2, Quad) {
    'use strict';

    // i heard document.ready isn't necessary anymore. just trying it out...
    //$(document).ready(function () {
        $('#foxtail').sprite({fps: 12, no_of_frames: 44, rewind: true});

        // Smooth scroll-to for left menu navigation
        $('#partner-nav a, #nav-main-menu a').click(function(e) {
            var elementClicked = $(this).attr("href");
            var destination;

            // all <article>'s have set height and position
            switch (elementClicked) {
                case '#overview':
                    destination = 0;
                    break;
                case '#os':
                    destination = 680;
                    break;
                case '#marketplace':
                    destination = 1360;
                    break;
                case '#android':
                    destination = 2040;
                    break;
            }

            $("html:not(:animated),body:not(:animated)").animate({ scrollTop: destination }, 700);
            return false;
        });

        var $giantfox = $('#giantfox');
        var $giantfox_tail = $('#giantfox-foreground');
        var $phone = $('#phone-common');
        var $phone_android = $('#phone-android');
        var $overview = $('#overview');
        var $os = $('#os');
        var $marketplace = $('#marketplace');
        var $android = $('#android');

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

            // slide phone?
            if (dest_pos > 1) {
                $phone.animate({ 'left': '-50%' }, 500);
            } else {
                $phone.animate({ 'left': '50%' }, 500);
            }
        });

        $('a[data-section="os-operators"]').on('click', function() {
            $giantfox.css('left', '-45%');
        });

        $('a[data-section="os-overview"]').on('click', function() {
            $giantfox.css('left', '45%');
        });

        var _transition_tail = function(z_index, opacity, top) {
            $giantfox_tail.css({
                'z-index': z_index,
                'opacity': opacity,
                'top': top
            });
        };

        var _move_phone = function(top_pos, slide) {
            if (Number(slide.find('section:first').attr('data-current')) === 1) {
                if ($phone.css('left') === '-50%') {
                    $phone.animate({
                        top: top_pos
                    }, 100, function() {
                        $phone.animate({ 'left': '50%' }, 500);
                    });
                } else {
                    $phone.animate({ 'top': top_pos + 'px' }, 500);
                }
            } else {
                if ($phone.css('left') !== '-50%') {
                    $phone.animate({
                        'left': '-50%'
                    }, 500, function() {
                        $phone.css('top', top_pos + 'px');
                    });
                } else {
                    $phone.animate({ 'top': top_pos + 'px' }, 500);
                }
            }
        };

        var controller = $.superscrollorama();

        var tweens = {};

        tweens.slide_up = {
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
            to: {
                css: { top: -120 },
                onComplete: function() {
                    _move_phone(944, $os);
                    _transition_tail(121, 1, 0);
                },
                onReverseComplete: function() {
                    _move_phone(220, $overview);
                    _transition_tail(110, 0.2, -120);
                }
            }
        };

        tweens.article_marketplace = {
            from: {
                css: { top: -120, ease: Power2.easeOut },
                immediateRender: true
            },
            to: {
                css: { top: -240 },
                onStart: function() {
                    _transition_tail(110, 0.2, -120);
                },
                onComplete: function() {
                    _move_phone(1520, $marketplace);
                },
                onReverseComplete: function() {
                    _move_phone(944, $os, 110);
                    _transition_tail(121, 1, 0);
                }
            }
        };

        tweens.article_android = {
            from: {
                css: { top: -240, ease: Power2.easeOut },
                immediateRender: true
            },
            to: {
                css: { top: -360 },
                onComplete: function() {
                    _move_phone(2200, $android);
                    $phone_android.css('bottom', '0px');
                },
                onReverseComplete: function() {
                    _move_phone(1520, $marketplace);
                    $phone_android.css('bottom', '-600px');
                }
            }
        };

        var prev_article = '#overview';

        $('.partner-article').each(function(i, article) {
            var $article = $(article);

            var my_tweens = [], tween, $tweener;

            if ($article.attr('id') !== 'overview') {
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
                    tweens.slide_up.from,
                    tweens.slide_up.to
                );

                my_tweens.push(tween);
            });

            if (my_tweens.length > 0) {
                controller.addTween(
                    prev_article,
                    (new TimelineLite()).append(my_tweens),
                    350, // scroll duration
                    500 // start offset
                );
            }

            if ($article.attr('id') !== 'overview') {
                prev_article = '#' + $article.attr('id');
            }
        });
    //});
})(window, window.jQuery, window.TweenMax, window.TimelineLite, window.Power2, window.Quad);
