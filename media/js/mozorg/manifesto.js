/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
    'use strict';

    var ltr = document.dir === 'ltr';

    // Set up the modal navigation
    var nav_modal = function (direction) {
        var $origin = $('.modal-origin').removeClass('modal-origin');
        var section_id = $origin.attr('id');
        var action;

        if (direction === 1) {
            action = 'modal next';
            $origin = $origin.next().length ? $origin.next()
                                            : $origin.siblings(':first');
        } else {
            action = 'modal prev';
            $origin = $origin.prev().length ? $origin.prev()
                                            : $origin.siblings(':last');
        }

        $('#modal').attr('aria-labelledby', section_id).focus();
        $('#modal .inner').attr('id', section_id + '-overlay');
        $('#modal .overlay-contents').replaceWith($origin.clone()
            .attr('tabindex', '0').addClass('overlay-contents'));

        $origin.addClass('modal-origin');

        gaTrack(['_trackEvent', '/about/manifesto/ Interactions',
                 action, section_id.match(/\d+/)[0]]);
    };

    // Set up the modal
    $('[id^="principle-"]').each(function () {
        var $this = $(this);
        var section_id = $this.attr('id');

        $this.attr({
            'tabindex': '0'
        }).on('click', function () {
            Mozilla.Modal.createModal(this, $this.clone().removeAttr('id'), {
                'title': '',
                'onCreate': function () {
                    var $inner = $('#modal .inner').attr('id', section_id + '-overlay');
                    var $nav = $('<nav role="presentation"></nav>').insertBefore('#modal-close');

                    $('<button class="next" aria-controls="modal"></button>')
                        .text(window.trans('principle-nav-next')).appendTo($nav);
                    $('<button class="prev" aria-controls="modal"></button>')
                        .text(window.trans('principle-nav-prev')).appendTo($nav);

                    $nav.on('click', 'button', function () {
                        nav_modal($(this).hasClass('prev') ? -1 : 1);
                    });

                    gaTrack(['_trackEvent', '/about/manifesto/ Interactions',
                             'modal open', section_id.match(/\d+/)[0]]);
                }
            });
        }).on('keydown', function (event) {
            if (event.keyCode === 13) {
                $this.trigger('click');
            }
        });

        $('<p class="more"></p>').text(window.trans('principle-read-more').replace('…', ''))
            .appendTo($this.find('header'));
    });

    // Set up keyboard shortcuts for the modal
    $(document).on('keydown', '#modal', function (event) {
        var direction = 0;

        switch (event.keyCode) {
            case 37: // Left arrow
                direction = ltr ? -1 : 1;
                break;
            case 38: // Up arrow
                direction = -1;
                break;
            case 39: // Right arrow
                direction = ltr ? 1 : -1;
                break;
            case 40: // Down arrow
                direction = 1;
                break;
        }

        if (direction) {
            event.preventDefault();
            nav_modal(direction);
        }
    });

    // Open Twitter in a sub window
    // https://dev.twitter.com/docs/intents
    var open_twitter_subwin = function (section, url) {
        gaTrack(['_trackEvent', '/about/manifesto/ Interactions',
                 'tweet', section]);

        // Check if the official Twitter widget is activated. If so, we don't
        // have to open a popup window ourselves as it will be opened by the
        // widget code.
        if (window.__twitterIntentHandler) {
            return;
        }

        var width = 550;
        var height = 420;
        var options = {
            'scrollbars': 'yes',
            'resizable': 'yes',
            'toolbar': 'no',
            'location': 'yes',
            'width': width,
            'height': height,
            'top': screen.height > height ? Math.round((screen.height / 2) - (height / 2)) : 0,
            'left': Math.round((screen.width / 2) - (width / 2))
        };

        window.open(url, 'twitter_share', $.param(options).replace(/&/g, ',')).focus();
    };

    // Set up modal link handler
    $(document).on('click', '#modal .principle a', function (event) {
        var $this = $(this);
        var section = $('#modal .inner').attr('id').match(/\d+/)[0];
        var href = $this.attr('href');
        var action;

        if ($this.hasClass('tweet')) {
            // Open Twitter in a sub window
            event.preventDefault();
            open_twitter_subwin(section, href);
        } else {
            // Open the link in a new tab
            $this.attr('target', '_blank');
            action = href.match(/youtube/) ? 'modal video link click'
                                           : 'modal link click';
            gaTrack(['_trackEvent', '/about/manifesto/ Interactions',
                     action, section + ': ' + $this.text()]);
        }
    });

    var tell_link = $('#sec-tell .share .tweet');

    // Update the tweet link when the custom text is modifled
    $('#sec-tell textarea').on('input', function () {
        tell_link.attr('href', tell_link.attr('href')
            .replace(/&text=.*/, '&text=' + encodeURIComponent($(this).val())));
    });

    // Set up content link handler
    $('#main-content a').on('click', function (event) {
        var $this = $(this);
        var href = $this.attr('href');

        event.preventDefault();

        if ($this.hasClass('tweet')) {
            // Open Twitter in a sub window
            open_twitter_subwin('custom', href);
        } else if (!$this.hasClass('share-button')) {
            // Open the link in the current tab
            gaTrack(['_trackEvent', '/about/manifesto/ Interactions',
                     'content link click ', $this.text()],
                    function () { location.href = href; });
        }
    });

    var grid_loaded = false;

    // Show the background picture grid
    var show_grid = function (mql) {
        if (!mql.matches || grid_loaded) {
            return;
        }

        $('.ri-grid img').each(function () {
            $(this).attr('src', $(this).data('src'));
        });

        $('.ri-grid').gridrotator({
            rows: 18,
            columns: 2,
            animType: 'fadeInOut',
            animSpeed: 1000,
            interval: 1000,
            step: 1,
            w480: {
                rows: 18,
                columns: 2
            }
        }).addClass('loaded');

        grid_loaded = true;
    };

    // Hide the grid on mobile to reduce the bandwidth
    if (window.matchMedia) {
        var mql = window.matchMedia('(min-width: 761px)');

        mql.addListener(show_grid);
        show_grid(mql);
    } else if ($(window).width() >= 761) {
        show_grid({ matches: true });
    }
});
