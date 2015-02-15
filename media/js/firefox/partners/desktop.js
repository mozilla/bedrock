/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, TweenMax) {
    'use strict';

    w.ga_track('');

    var $body = $('body');
    var $article_wrapper = $('#article-wrapper');
    var article_height = 820;
    var header_height = 130; // leave room for the Fx family nav
    var parallax_offset = 0;
    var phone_offset = 200; // distance from top of article to top of phone
    var phone_speed = 0.7; // seconds phone movement speed between articles

    var $os_giantfox = $('#os .giantfox');
    var $os_giantfox_tail = $('#os .giantfox .giantfox-foreground');
    var $os_article_header = $('#os .article-header');
    var $os_article_content = $('#os .article-content');
    var $marketplace_giantfox_bg = $('.marketplacegiantfox.giantfox-background');
    var $marketplace_giantfox_fg = $('.marketplacegiantfox.giantfox-foreground');
    var $android_tablet = $('#android .android-tablet');
    var $phone = $('#phone-common');
    var $phone_android = $('#phone-android');
    var $phone_shadows = $('.phone-shadow');
    var $overview = $('#overview');
    var $os = $('#os');
    var $marketplace = $('#marketplace');
    var $marketplace_article_header = $('#marketplace .article-header');
    var $marketplace_article_content = $('#marketplace .article-content');
    var $android = $('#android');
    var $partner_menu = $('#partner-menu li');

    var virtual_page;
    var scroll_tracking = true;
    var phone_visible = true;

    var scroll_track = function(url) {
        if (scroll_tracking) {
            // bit of a hack to standardize tracking
            if (url === 'overview/') {
                url = '';
            }

            w.ga_track(url);
        }
    };

    // set up foxtail sprite animation
    $('#foxtail').sprite({fps: 12, no_of_frames: 44, rewind: true});

    var activate_nav_item = function(active_id) {
        $partner_menu.removeClass('active');
        $('#menu-' + active_id).addClass('active');
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
                destination = (
                    article_height - parallax_offset + header_height
                );
                break;
            case '#marketplace':
                destination = (
                    (article_height * 2) - (parallax_offset * 2) + header_height
                );
                break;
            case '#android':
                destination = (
                    (article_height * 3) - (parallax_offset * 3) + header_height
                );
                break;
        }

        // reset phone & giantfox
        TweenMax.to($phone, phone_speed, { x: 0 });
        TweenMax.to($phone_android, phone_speed, { x: 0 });
        $os_giantfox.css('margin-left', '-70px');
        $marketplace_giantfox_bg.css('margin-left', '-30px');
        $marketplace_giantfox_fg.css('margin-left', '86px');
        $android_tablet.css('margin-left', '-40px');

        // force all first sections to be current
        $('.partner-article').each(function(i, article) {
            var $article = $(article);
            $article.attr('data-section', $article.find('section:first').attr('id'));
            $article.find('section').each(function(j, section) {
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
                if (w.location.hash === '#map' || w.location.hash === '#schedule') {
                    $('a.modal[href="' + w.location.hash + '"]:first').trigger('click');
                } else {
                    $('#partner-nav a[href="' + w.location.hash + '"]').trigger('click');
                    w.location.hash = '';
                }
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
        var $pageslide = $('#pageslide');

        if ($pageslide.is(':visible')) {
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
    var $overview_news_links = $('#overview-news-links').detach();
    $('#overview .partner-logos').after($overview_news_links);
    $overview_news_links.fadeIn('fast');

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
        var cur_phone = (article.attr('id') === 'android') ? 'android' : 'phone';

        // slide phone?
        if (dest_pos > 1) {
            if (cur_phone === 'android') {
                TweenMax.set($phone_android, { x: '-1200px' });
            } else {
                TweenMax.to($phone, phone_speed, { x: '-1200px' });
                phone_visible = false;
            }
        } else {
            if (cur_phone === 'android') {
                TweenMax.set($phone_android, { x: 0});
                $phone_android.removeAttr("style");
            } else {
                TweenMax.to($phone, phone_speed, { x: 0});
                phone_visible = true;
            }
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
        $marketplace_giantfox_bg.css('margin-left', '-1110px');
        $marketplace_giantfox_fg.css('margin-left', '-994px');
    });

    $('a[data-section="marketplace-overview"]').on('click', function() {
        $marketplace_giantfox_bg.css('margin-left', '-30px');
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
            $visible.css('z-index', 1);
            var $screen = $('#screen-' + to_slide.attr('id'));
            $screen.stop().css('z-index', 0).show();
            $visible.stop().fadeOut();
        }
    };

    // pretty complex function to move phone with scrolling/click nav
    var _move_phone = function(factor, slide, new_z) {

        var slide_id = slide.attr('id');
        var $first_section = slide.find('section:first');

        var onAndroidComplete = function () {
            virtual_page = 'android/';

            if ($first_section.attr('data-current') !== '1') {
                virtual_page += slide.find('section[data-current="1"]:first').attr('id') + '/';
            }

            scroll_track(virtual_page);
        };

        var onAnimateInFromLeft = function () {
            $phone.attr('data-showing', 0);
            scroll_track(slide.attr('id') + '/');
            _refresh_phone(slide, 'in');
        };

        var onAnimateOutToLeft = function () {
            $phone.attr('data-hiding', 0);

            if (new_z) {
                $phone.css('z-index', new_z);
            }
            TweenMax.set($phone, {y: top_pos + 'px'});

            scroll_track(virtual_page);
            _refresh_phone(slide, 'out');
        };

        var onAnimateTop = function () {
            if (new_z) {
                $phone.css('z-index', new_z);
            }

            scroll_track(slide.attr('id') + '/');
            _refresh_phone(slide, 'in');
        };

        // fade out all phone shadows
        $phone_shadows.removeClass('visible');

        // set current article for inherited body styles
        $body.attr('data-article', slide_id);

        // set active left menu item
        activate_nav_item(slide_id);

        // calculate new top position for phone
        var top_pos = ((article_height * factor) - (parallax_offset * factor));

        // scrolling to android slide should never affect standard phone's left or z-index
        if (slide_id === 'android') {

            TweenMax.to($phone, phone_speed, {
                y: top_pos + 'px',
                onComplete: onAndroidComplete,
                onReverseComplete: onAndroidComplete
            });
        } else {
            // would like to abstract this more, but each scenario requires specific sequencing

            // if going to the first section in an article, phone should end up in viewport
            // only need to track root article
            if ($first_section.attr('data-current') === '1') {
                // if phone is not visible, quickly change top position, then nicely
                // animate in from left

                if (!phone_visible) {
                    if (new_z) {
                        $phone.css('z-index', new_z);
                    }

                    $phone.attr('data-showing', 1);

                    TweenMax.set($phone, {y: top_pos + 'px'});
                    TweenMax.to($phone, phone_speed, {
                        x: 0,
                        // after current screen has slid off to the left, move it back to 'ready' position off to the right
                        onComplete: onAnimateInFromLeft,
                        onReverseComplete: onAnimateInFromLeft
                    });
                    phone_visible = true;

                // if phone is visible, animate top position only
                } else {

                    TweenMax.to($phone, phone_speed, {
                        y: top_pos + 'px',
                        onComplete: onAnimateTop,
                        onReverseComplete: onAnimateTop
                    });
                }
            // if moving to a sub-section of article, phone should end up off
            // screen to the left. track article and sub-section
            } else {
                // if phone is visible, animate nicely off to the left, then
                // change top position
                virtual_page = slide_id + '/' + slide.find('section[data-current="1"]:first').attr('id') + '/';

                if (phone_visible) {
                    $phone.attr('data-hiding', 1);

                    TweenMax.to($phone, phone_speed, {
                        x: '-1200px',
                        // after current screen has slid off to the left, move it back to 'ready' position off to the right
                        onComplete: onAnimateOutToLeft,
                        onReverseComplete: onAnimateOutToLeft
                    });
                    phone_visible = false;

                // if phone is not visible, just change top position
                } else {
                    if (new_z) {
                        $phone.css('z-index', new_z);
                    }

                    _refresh_phone(slide, 'out');

                    TweenMax.set($phone, {y: top_pos + 'px'});

                    scroll_track(virtual_page);
                }
            }
        }
    };

    $('#os').waypoint(function(direction) {
        if (direction === 'down') {
            $phone.css('z-index', 110);
            $os_giantfox.addClass('up');
            _move_phone(1, $os, 110);

        } else {
            $os_giantfox.removeClass('up');
            _move_phone(0, $overview);
        }
    }, {
        offset: '50%'
    });

    $('#marketplace').waypoint(function(direction) {
        if (direction === 'down') {
            // force z index immediately to avoid sliding behind
            // the marketplace slide
            $phone.css('z-index', 120);
            _move_phone(2, $marketplace, 120);
        } else {
            // force z index immediately to avoid sliding behind
            // the marketplace slide
            $phone.css('z-index', 120);
            _move_phone(1, $os, 110);
        }
    }, {
        offset: '50%'
    });

    $('#android').waypoint(function(direction) {
        if (direction === 'down') {
            $phone_android.addClass('android-phone-visible');
            _move_phone(3, $android);
        } else {
            $phone_android.removeClass('android-phone-visible');
            _move_phone(2, $marketplace);
        }
    }, {
        offset: '50%'
    });

})(window, window.jQuery, window.TweenMax);
