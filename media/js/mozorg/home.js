/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $window = $(window);
    var $body = $('body');
    var wideMode = false;
    var hasMediaQueries = (typeof matchMedia !== 'undefined');

    // If the browser supports media queries, check the width onload and onresize.
    // If not, just lock it in permanent wideMode.
    if (hasMediaQueries) {
        checkWidth();
        $window.on('resize', function() {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(checkWidth, 200);
        });
    } else {
        wideMode = true;
        $body.addClass('wide');
    }

    function checkWidth() {
        if (window.matchMedia('screen and (min-width: 761px)').matches) {
            wideMode = true;
            $body.addClass('wide');
        } else {
            wideMode = false;
            $body.removeClass('wide');
        }

        // Reset all accordion panels
        $('.panel, .panel-content, .panel-title').removeAttr('style');
        $('.panel-content a').blur();

        // Adjust the news headlines
        $('.extra-news a').each(function () {
            var title = $(this).attr('title');
            if (!title) {
                title = $.trim($(this).text());
                $(this).attr('title', title);
            }
            $(this).text(title).ellipsis({ row: 3 });
        });
    }

    var accordion = {
        // Expand the accordion horizontally
        expandHorz: function(panel) {
            $('.panel-title').stop(true,true).fadeOut(200);
            panel.stop().removeClass('compressed').addClass('expanded').animate({'width':'64%'},700);
            $('.panel-content', panel).stop(true,true).delay(400).fadeIn(400);
            panel.siblings('.panel').stop().removeClass('expanded').addClass('compressed').animate({'width':'12%'},700);
            panel.siblings('.panel').find('.panel-content').stop(true,true).fadeOut(400, function() {
                $(this).delay(500).removeAttr('style');
            });
            track_accordion('open', ($('.panel').index(panel) + 1), panel.attr('id'));
        },

        // Contract the accordion horizontally
        contractHorz: function() {
            $('.panel').stop().animate({'width':'25%'},700, function() {
                $('.panel-title').fadeIn(250);
            }).removeClass('expanded compressed');
            $('.panel-content').stop(true,true).delay(200).fadeOut(500);
        },

        // Expand the accordion vertically
        expandVert: function(panel) {
            $('.panel-title').stop(true,true).fadeOut(200);
            panel.stop().removeClass('compressed').addClass('expanded').animate({'height':'22em'},700);
            panel.siblings('.panel').stop().removeClass('expanded').addClass('compressed').animate({'height':'3em'},700);
            $('.panel-content', panel).stop(true,true).delay(400).fadeIn(400);
            panel.siblings('.panel').find('.panel-content').stop(true,true).fadeOut(400, function() {
                $(this).delay(500).removeAttr('style');
            });
            track_accordion('open', ($('.panel').index(panel) + 1), panel.attr('id'));
        },

        // Contract the accordion vertically
        contractVert: function() {
            $('.panel').stop().animate({'height':'4.5em'},700, function() {
                $('.panel-title').fadeIn(250);
            }).removeClass('expanded compressed');
            $('.panel-content').stop(true,true).fadeOut(500);
        },
    };

    var hoverDelay = 200;
    var hoverTimeout;

    $('.accordion').on('mouseleave', function() {
        clearTimeout(hoverTimeout);
        hoverDelay = 200;
    });

    // Expand onmouseover, contract onmouseout
    $('.panel').hover(
        function() {
            var self = $(this);
            clearTimeout(hoverTimeout);
            hoverTimeout = setTimeout(function() {
                if (wideMode) {
                    accordion.expandHorz(self);
                } else {
                    accordion.expandVert(self);
                }
                hoverDelay = 0;
            }, hoverDelay);
        },
        function() {
            if (wideMode) {
                accordion.contractHorz($(this));
            } else {
                accordion.contractVert();
            }
        }
    );

    // Expand on click or focus
    $('.panel').on('click focus', function(event) {
        if (!$(this).hasClass('expanded')) {
            if (wideMode) {
                accordion.expandHorz($(this));
            } else {
                accordion.expandVert($(this));
            }
        }
    });

    // Contract when the inner link loses focus
    // Assumes a single link in the panel
    $('.panel > a').on('blur', function() {
        if (wideMode) {
            accordion.contractHorz();
        } else {
            accordion.contractVert();
        }
    });

    // Add the next and previous control buttons
    function controlButtons() {
        var $buttonNext = $('<button type="button" class="btn-next">' + window.trans('news-next') + '</button>');
        var $buttonPrev = $('<button type="button" class="btn-prev">' + window.trans('news-prev') + '</button>');
        var $buttons = $('<span class="news-buttons"></span>');

        $buttonNext.prependTo($buttons);
        $buttonPrev.prependTo($buttons);
        $buttons.prependTo('.extra-news > .control');

        $('.news-buttons .btn-next').bind('click', function() {
            gaTrack(['_trackEvent', 'Mozilla in the News Interactions', 'Next', 'News Navigation Arrows']);
        });
        $('.news-buttons .btn-prev').bind('click', function() {
            gaTrack(['_trackEvent', 'Mozilla in the News Interactions', 'Previous', 'News Navigation Arrows']);
        });
    }
    controlButtons();

    // Track when/which accordion panels are opened
    var track_accordion = function(position, id) {
        gaTrack(['_trackEvent','Homepage Interactions', 'open', position+':'+id]);
    };

    // Track panel clicks
    $('.panel-content a').on('click', function(e) {
        e.preventDefault();
        var panel = $(this).parents('.panel');
        var href = this.href;
        var callback = function() {
            $(this).blur();
            window.location = href;
        };
        gaTrack(['_trackEvent','Homepage Interactions', 'click', (panel.index() + 1)+':'+panel.attr('id')], callback);
    });

    // Track donate clicks
    $('#home-promo-donate-form').submit(function(e) {
        e.preventDefault();

        var $form = $(this);
        $form.unbind('submit');

        var panel = $(this).parents('.panel');

        gaTrack(
            ['_trackEvent', 'Homepage Interactions', 'submit', (panel.index() + 1) + ':donate'],
            function (){ $form.submit(); }
        );
    });

    // Track news clicks
    $('.extra-news a').on('click', function(e) {
        e.preventDefault();
        var href = this.href;
        var callback = function() {
            window.location = href;
        };
        gaTrack(['_trackEvent', 'Mozilla in the News Interactions','click', href], callback);
    });

    // Track contribute clicks
    $('.extra-contribute a, .engage a').on('click', function(e) {
        e.preventDefault();
        var href = this.href;
        var callback = function() {
            window.location = href;
        };
        gaTrack(['_trackEvent', 'Get Involved Interactions','clicks', 'Get Involved Button'], callback);
    });

})(window.jQuery);
