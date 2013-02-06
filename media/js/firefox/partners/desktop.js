/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, TweenMax, TimelineLite, Power2, Quad) {
    'use strict';

    var article_height = 820;
    var parallax_offset = 120;
    var phone_offset = 200; // distance from top of article to top of phone

    // i heard document.ready isn't necessary anymore. just trying it out...
    //$(document).ready(function () {
        // set up foxtail sprite animation
        $('#foxtail').sprite({fps: 12, no_of_frames: 44, rewind: true});

        // Smooth scroll-to for left menu navigation
        $('#partner-nav a[class!="no-scroll"], #nav-main-menu a').click(function(e) {
            var elementClicked = $(this).attr("href");
            var destination;

            // all <article>'s have set height and position
            switch (elementClicked) {
                case '#overview':
                    destination = 0;
                    break;
                case '#os':
                    destination = (article_height - parallax_offset);
                    break;
                case '#marketplace':
                    destination = ((article_height * 2) - (parallax_offset * 2));
                    break;
                case '#android':
                    destination = ((article_height * 3) - (parallax_offset * 3));
                    break;
            }

            $("html:not(:animated),body:not(:animated)").animate({ scrollTop: destination }, 700);
            return false;
        });

        // move form out of overlay
        var $form = $('#form').detach();
        $('#article-wrapper').after($form);

        // activate form drawer
        $('#toggle-form').pageslide({
            direction: 'left'
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

        var _move_phone = function(factor, slide, new_z) {
            var cur_left = $phone.position().left;
            var doc_width = $(w.document).width();

            // when jumping more than one section with nav, phone may
            // not make it all the way to -50%
            // if phone is less than halfway across current viewport,
            // assume it's not visible
            var visible = (cur_left >= (doc_width/2));

            var top_pos = ((article_height * factor) - (parallax_offset * factor)) + phone_offset;

            // would like to abstract this more, but each scenario requires specific sequencing
            if (Number(slide.find('section:first').attr('data-current')) === 1) {
                if (!visible) {
                    if (new_z) {
                        $phone.css('z-index', new_z);
                    }

                    $phone.animate({
                        top: top_pos
                    }, 100, function() {
                        $phone.animate({ 'left': '50%' }, 500);
                    });
                } else {
                    $phone.animate({ 'top': top_pos + 'px' }, 500, function() {
                        if (new_z) {
                            $phone.css('z-index', new_z);
                        }
                    });
                }
            } else {
                if (visible) {
                    $phone.animate({
                        'left': '-50%'
                    }, 500, function() {
                        $phone.css('top', top_pos + 'px');

                        if (new_z) {
                            $phone.css('z-index', new_z);
                        }
                    });
                } else {
                    if (new_z) {
                        $phone.css('z-index', new_z);
                    }

                    $phone.animate({ 'top': top_pos + 'px' }, 500);
                }
            }
        };

        var controller = $.superscrollorama();

        var tweens = {};

        tweens.slide_up = {
            from: {
                css: { top: 120, opacity: 0 },
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
                css: { top: (parallax_offset*-1) },
                onStart: function() {
                    $phone.css('z-index', 110);
                },
                onComplete: function() {
                    _move_phone(1, $os);
                },
                onReverseComplete: function() {
                    _move_phone(0, $overview);
                }
            }
        };

        tweens.article_marketplace = {
            from: {
                css: { top: (parallax_offset*-1), ease: Power2.easeOut },
                immediateRender: true
            },
            to: {
                css: { top: (parallax_offset*-2) },
                onStart: function() {
                    $phone.css('z-index', 120);
                },
                onComplete: function() {
                    _move_phone(2, $marketplace);
                },
                onReverseComplete: function() {
                    _move_phone(1, $os, 110);
                }
            }
        };

        tweens.article_android = {
            from: {
                css: { top: (parallax_offset*-2), ease: Power2.easeOut },
                immediateRender: true
            },
            to: {
                css: { top: (parallax_offset*-3) },
                onComplete: function() {
                    _move_phone(3, $android);
                    $phone_android.addClass('android-phone-visible');
                },
                onReverseComplete: function() {
                    _move_phone(2, $marketplace);
                    $phone_android.removeClass('android-phone-visible');
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

