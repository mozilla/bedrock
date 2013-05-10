/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, TweenMax, TimelineLite, Power2, Quad) {
    'use strict';

    w.ga_track('');

    var $article_wrapper = $('#article-wrapper');
    var article_height = 820;
    var parallax_offset = 142;
    var phone_offset = 200; // distance from top of article to top of phone
    var phone_speed = 400; // ms phone movement speed between articles

    var $os_giantfox = $('#os .giantfox');
    var $os_giantfox_tail = $('#os .giantfox .giantfox-foreground');
    var $marketplace_giantfox_bg = $('.marketplacegiantfox.giantfox-background');
    var $marketplace_giantfox_fg = $('.marketplacegiantfox.giantfox-foreground');
    var $android_tablet = $('#android .android-tablet');
    var $phone = $('#phone-common');
    var $phone_android = $('#phone-android');
    var $phone_shadows = $('.phone-shadow');
    var $overview = $('#overview');
    var $os = $('#os');
    var $marketplace = $('#marketplace');
    var $android = $('#android');

    var virtual_page;
    var scroll_tracking = true;

    var scroll_track = function(url) {
        if (scroll_tracking) {
            // bit of a hack to standardize tracking
            if (url === 'overview/') {
                url = '';
            }

            w.ga_track(url);
        }
    };

    // set phone position (needs to be in inline style object for retrieval later)
    $phone.css('left', '50%');

    // set up foxtail sprite animation
    $('#foxtail').sprite({fps: 12, no_of_frames: 44, rewind: true});

    var activate_nav_item = function(active_id) {
        $('#partner-menu li').removeClass('active');
        $('#partner-menu li[id="menu-' + active_id + '"]').addClass('active');
    };

    activate_nav_item('overview');

    // Smooth scroll-to for left menu navigation
    $('#partner-menu a, #nav-main-menu a, a.nav').click(function(e) {
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

        // reset phone & giantfox
        $phone.animate({ 'left': '50%' }, phone_speed);
        $phone_android.animate({ 'left': '50%' }, phone_speed);
        $os_giantfox.css('margin-left', '-70px');
        $marketplace_giantfox_bg.css('margin-left', '-40px');
        $marketplace_giantfox_fg.css('margin-left', '86px');
        $android_tablet.css('margin-left', '-40px');

        // force all first sections to be current
        $('.partner-article').each(function(i, article) {
            $(article).attr('data-section', $(article).find('section:first').attr('id'));
            $(article).find('section').each(function(j, section) {
                $(section).css('left', (j * 100) + '%').attr('data-current', ((j === 0) ? 1 : 0));
            });
        });

        // make sure scroll tracking doesn't happen while animating scroll position with buttons
        scroll_tracking = false;

        // slow-ish scrolling to make scroll animation life easier
        $("html:not(:animated),body:not(:animated)").animate({ scrollTop: destination }, 1000, function() {
            scroll_tracking = true;
        });

        virtual_page = (elementClicked !== '#overview') ? elementClicked.replace(/#/, '') + '/' : '';

        w.ga_track(virtual_page);

        return false;
    });

    // if hash changes, make sure parallax doesn't go haywire
    var _handle_hash = function() {
        if (w.location.hash !== '') {
            $article_wrapper.animate({ scrollTop: 0 }, 50, function() {
                if (w.location.hash === 'location' || w.location.hash === 'schedule') {
                    $('a.modal[href="#' + w.location.hash + '"]:first').trigger('click');
                } else {
                    $('#partner-nav a[href="' + w.location.hash + '"]').trigger('click');
                }

                w.location.hash = '';
            });
        }
    };

    // fix for loading page with anchor in URL
    $(function() {
        setTimeout(function() {
            _handle_hash();
        }, 60); // may need to increase timeout?
        // ease flicker when loading hash/content
        setTimeout(function() {
            $article_wrapper.animate({ opacity: 1}, 'fast');
            $phone.show();
        }, 150);
    });

    $(w).on('hashchange', function() {
        _handle_hash();
    });

    var _toggle_form = function() {
        var $menu = $('#overlay-menu');

        $menu.toggleClass('form-open');

        if (!$menu.hasClass('form-open')) {
            $.pageslide.close();
        } else {
            w.ga_track('form/');
            setTimeout(function () {
                $("#pageslide form").attr('tabindex', '-1')[0].focus();
            }, 300);
        }
    };

    // move form out of overlay and into its own container for side slider
    var $form = $('#form').detach();
    $form.hide();
    $article_wrapper.after($form);

    $form.find('.close').click(function() {
        _toggle_form();
    });

    // re-arrange news, partner button, & links if #overview
    var $overview_news = $('#overview-news').detach();
    $('#more-partners').after($overview_news);
    $overview_news.fadeIn('fast');

    var $overview_actions= $('#overview .overview-actions').detach();
    $('#overview-news').after($overview_actions);
    $overview_actions.fadeIn('fast');

    var $overview_partner= $('#overview .partner-button').detach();
    $('#overview .partner-logos').after($overview_partner);
    $overview_partner.fadeIn('fast');

    // activate form drawer
    $('.toggle-form').off().on('click', function() {
        _toggle_form();
    }).pageslide({
        direction: 'left',
        modal: true,
        speed: 300
    });

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

            // make sure we round to the nearest 100
            var new_left = Math.round((el_left - delta)/100)*100;

            section.css('left', new_left + '%').attr('data-current', 0);
        });

        // update current section
        dest.attr('data-current', 1);

        // update parent article selector
        article.attr('data-section', dest.attr('id'));

        // which phone should we move?
        var $cur_phone = (article.attr('id') === 'android') ? $phone_android : $phone;

        // slide phone?
        if (dest_pos > 1) {
            $cur_phone.stop().animate({ 'left': '-50%' }, phone_speed);
        } else {
            $cur_phone.stop().animate({ 'left': '50%' }, phone_speed);
        }

        // track section view
        virtual_page = article.attr('id') + '/';

        // only add sub-section id if not in first position
        if (dest_pos > 1) {
            virtual_page += dest.attr('id') + '/';
        }

        w.ga_track(virtual_page);
    });

    // custom horizontal movement of large background graphics
    $('a[data-section="os-operators"]').on('click', function() {
        $os_giantfox.css('margin-left', '-1380px');
    });

    $('a[data-section="os-overview"]').on('click', function() {
        $os_giantfox.css('margin-left', '-70px');
    });

    $('a[data-section="marketplace-developers"]').on('click', function() {
        $marketplace_giantfox_bg.css('margin-left', '-2120px');
        $marketplace_giantfox_fg.css('margin-left', '-1994px');
    });

    $('a[data-section="marketplace-operators"]').on('click', function() {
        $marketplace_giantfox_bg.css('margin-left', '-1120px');
        $marketplace_giantfox_fg.css('margin-left', '-994px');
    });

    $('a[data-section="marketplace-overview"]').on('click', function() {
        $marketplace_giantfox_bg.css('margin-left', '-40px');
        $marketplace_giantfox_fg.css('margin-left', '86px');
    });

    $('a[data-section="android-partner"]').on('click', function() {
        $android_tablet.css('margin-left', '-1520px');
    });

    $('a[data-section="android-overview"]').on('click', function() {
        $android_tablet.css('margin-left', '-40px');
    });

    // show/hide phone shade and set phone screen contents
    var _refresh_phone = function(to_slide, shadowinout) {
        var shadow = to_slide.find('.phone-shadow');
        if (shadowinout === 'in') {
            shadow.addClass('visible');
        } else {
            shadow.removeClass('visible');
        }

        var $visible = $('.screen:visible:first');

        if ($visible.attr('id') !== ('screen-' + to_slide.attr('id'))) {
            // make sure from/to screens are not currently animating
            $visible.stop();

            var $screen = $('#screen-' + to_slide.attr('id'));
            
            $screen.stop().fadeIn('fast', function() {
                // make sure from/to screens are properly shown/hidden
                $screen.css('opacity', 1).show();
                $visible.css('opacity', 0).hide();
            });
        }
    };

    // pretty complex function to move phone with scrolling/click nav
    var _move_phone = function(factor, slide, new_z) {
        // fade out all phone shadows
        $phone_shadows.removeClass('visible');

        // chaining animations gets too crazy
        // make sure only one animation is running/queued at one time
        if ($phone.is(':animated')) {
            $phone.stop();

            // if phone is in between hiding/showing, force that to finish immediately
            if (Number($phone.attr('data-hiding')) === 1) {
                $phone.css('left', '-50%');
                $phone.attr('data-hiding', 0);
            } else if (Number($phone.attr('data-showing')) === 1) {
                $phone.css('left', '50%');
                $phone.attr('data-showing', 0);
            }
        }

        // set current article for inherited body styles
        $('body').attr('data-article', slide.attr('id'));

        // set active left menu item
        activate_nav_item(slide.attr('id'));

        // phone is visible if at 50% left
        var cur_left = $phone[0].style.left;
        var visible = (cur_left === '50%');

        // calculate new top position for phone
        var top_pos = ((article_height * factor) - (parallax_offset * factor)) + phone_offset;

        // scrolling to android slide should never affect standard phone's left or z-index
        if (slide.attr('id') === 'android') {
            $phone.animate({ 'top': top_pos + 'px' }, phone_speed, function() {
                virtual_page = 'android/';

                if (slide.find('section:first').attr('data-current') !== '1') {
                    virtual_page += slide.find('section[data-current="1"]:first').attr('id') + '/';
                }

                scroll_track(virtual_page);
            });
        } else {
            // would like to abstract this more, but each scenario requires specific sequencing

            // if going to the first section in an article, phone should end up in viewport
            // only need to track root article
            if (Number(slide.find('section:first').attr('data-current')) === 1) {
                // if phone is not visible, quickly change top position, then nicely
                // animate in from left
                if (!visible) {
                    if (new_z) {
                        $phone.css('z-index', new_z);
                    }

                    $phone.animate({
                        top: top_pos
                    }, 50, function() {
                        $phone.attr('data-showing', 1);

                        _refresh_phone(slide, 'in');

                        $phone.animate({ 'left': '50%' }, phone_speed, function() {
                            $phone.attr('data-showing', 0);

                            scroll_track(slide.attr('id') + '/');
                        });
                    });
                // if phone is visible, animate top position only
                } else {
                    _refresh_phone(slide, 'in');

                    $phone.animate({ 'top': top_pos + 'px' }, phone_speed, function() {
                        if (new_z) {
                            $phone.css('z-index', new_z);
                        }

                        scroll_track(slide.attr('id') + '/');
                    });
                }
            // if moving to a sub-section of article, phone should end up off
            // screen to the left. track article and sub-section
            } else {
                // if phone is visible, animate nicely off to the left, then
                // change top position
                virtual_page = slide.attr('id') + '/' + slide.find('section[data-current="1"]:first').attr('id') + '/';

                if (visible) {
                    $phone.attr('data-hiding', 1);

                    _refresh_phone(slide, 'out');

                    $phone.animate({
                        'left': '-50%'
                    }, phone_speed, function() {
                        $phone.attr('data-hiding', 0);
                        $phone.css('top', top_pos + 'px');

                        if (new_z) {
                            $phone.css('z-index', new_z);
                        }

                        scroll_track(virtual_page);
                    });
                // if phone is not visible, just change top position
                } else {
                    if (new_z) {
                        $phone.css('z-index', new_z);
                    }

                    _refresh_phone(slide, 'out');

                    $phone.css('top', top_pos + 'px');

                    scroll_track(virtual_page);
                }
            }
        }
    };

    // set up parallax tweening
    var controller = $.superscrollorama();

    var tweens = {};

    // generic tween used for most article content
    tweens.slide_up = {
        from: {
            css: { top: (('ontouchstart' in w.document.documentElement) ? 0 : 120), opacity: (('ontouchstart' in w.document.documentElement) ? 1 : 0) },
            immediateRender: true
        },
        to: { css: { top: 0, opacity: 1 } }
    };

    // article specific tweens
    tweens.article_overview = {
        from: {
            css: { top: 0 },
            immediateRender: true
        },
        to: {
            css: { top: 0 },
            onReverseComplete: function() {
                _move_phone(0, $overview);
            }
        }
    };

    tweens.article_os = {
        from: {
            css: { top: 0, ease: Power2.easeOut },
            immediateRender: true
        },
        to: {
            css: { top: (parallax_offset*-1) },
            onStart: function() {
                // make sure phone is below giantfox tail
                $phone.css('z-index', 110);
            },
            onComplete: function() {
                _move_phone(1, $os, 110);
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
                // force z index immediately to avoid sliding behind
                // the marketplace slide
                $phone.css('z-index', 120);
            },
            onComplete: function() {
                // make sure z-index is updated
                _move_phone(2, $marketplace, 120);
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

    // set up tweens for contents of each article (except #overview)
    $('.partner-article').each(function(i, article) {
        var $article = $(article);

        var my_tweens = [], tween, $tweener;

        // #overview takes longer so it finishes last - needed to handle super
        // fast scrolling upwards
        var dur = ($article.attr('id') === 'overview') ? 1.6 : 0.5;

        tween = TweenMax.fromTo(
            $article,
            dur,
            tweens['article_' + $article.attr('id')].from,
            tweens['article_' + $article.attr('id')].to
        );

        my_tweens.push(tween);

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
            // execute tween when previous article is 600px from being out of viewport
            controller.addTween(
                prev_article,
                (new TimelineLite()).append(my_tweens),
                300, // scroll duration
                600 // start offset
            );
        }

        if ($article.attr('id') !== 'overview') {
            prev_article = '#' + $article.attr('id');
        }
    });
})(window, window.jQuery, window.TweenMax, window.TimelineLite, window.Power2, window.Quad);