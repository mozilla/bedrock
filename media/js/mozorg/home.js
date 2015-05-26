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
            var $this = $(this);
            var title = $this.attr('title');

            if (!title) {
                title = $.trim($this.text());
            }

            $this.text(title).ellipsis({
                row: 3,
                callback: function () {
                    var text = $.trim($this.text());

                    if (text.match('[.]{3}$')) {
                        $this.attr('title', title);
                    }
                }
            });
        });
    }

    var accordion = {
        // Expand the accordion horizontally
        expandHorz: function(panel) {
            $('.panel-title').stop(true,true).fadeOut(200);
            panel.stop().removeClass('compressed').addClass('expanded').animate({'width':'64%'}, 700, function() {
                track_accordion('open', ($('.panel').index(panel) + 1), panel.attr('id'));
            });
            $('.panel-content', panel).stop(true,true).delay(400).fadeIn(400);
            panel.siblings('.panel').stop().removeClass('expanded').addClass('compressed').animate({'width':'12%'},700);
            panel.siblings('.panel').find('.panel-content').stop(true,true).fadeOut(400, function() {
                $(this).delay(500).removeAttr('style');
            });
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
            panel.stop().removeClass('compressed').addClass('expanded').animate({'height':'22em'},700, function() {
                track_accordion('open', ($('.panel').index(panel) + 1), panel.attr('id'));
            });
            panel.siblings('.panel').stop().removeClass('expanded').addClass('compressed').animate({'height':'3em'},700);
            $('.panel-content', panel).stop(true,true).delay(400).fadeIn(400);
            panel.siblings('.panel').find('.panel-content').stop(true,true).fadeOut(400, function() {
                $(this).delay(500).removeAttr('style');
            });
        },

        // Contract the accordion vertically
        contractVert: function() {
            $('.panel').stop().animate({'height':'5.5em'},700, function() {
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
            window.dataLayer.push({
                event: 'mozilla-news-interaction',
                browserAction: 'Next'
            });
        });
        $('.news-buttons .btn-prev').bind('click', function() {
            window.dataLayer.push({
                event: 'mozilla-news-interaction',
                browserAction: 'Previous'
            });
        });
    }
    controlButtons();

    // Track when/which accordion panels are opened
    var track_accordion = function(position, id) {
        window.dataLayer.push({
            event: 'homepage-interaction',
            interaction: 'open',
            location: position + ':' + id});
    };

    // Track panel clicks
    $('.panel-content a').each(function() {
        var panel = $(this).parents('.panel');
        var location = (panel.index() + 1)+':'+panel.attr('id');
        $(this).attr({
            'data-tracking-flag': 'home',
            'data-interaction': 'click',
            'data-element-location': location
        });
    });

    // Track donate clicks
    $('#home-promo-donate-form').each(function() {
        var panel = $(this).parents('.panel');
        var location = (panel.index() + 1) + ':donate';
        $(this).attr({
            'data-tracking-flag': 'home',
            'data-interaction': 'submit',
            'data-element-location': location
        });
    });

    // Track news & contribute clicks
    $('.extra-news a, .extra-contribute a, .engage a').each(function() {
        var action = (/external/.test($(this).attr('rel'))) ? 'outbound link' : 'click';

        $(this).attr({
            'data-tracking-flag': 'home',
            'data-interaction': action,
            'data-element-location': this.href
        });
    });

    // Track Firefox downloads
    $('.download-link').each(function() {
        var platform;
        var $this = $(this);
        if ($this.parents('li').hasClass('os_android')) {
            platform = 'Firefox for Android';
        } else {
            platform = 'Firefox Desktop';
        }
        $this.attr({
            'data-interaction': 'download click',
            'data-download-version': platform
        });
    });

})(window.jQuery);
